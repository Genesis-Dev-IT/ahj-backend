from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from django.db import transaction
from app.models import (
        AHJ, AHJElectricalRequirement, AHJGroundMountRequirement, 
        AHJSolarRequirement, AHJRemark, ApiUsage, State, StateSpecificInformation, AHJLabel, AHJSafetyInstructions, AHJCodeMapping, 
        AHJEnvironmentalData, PermitType, AHJPermitMapping, AHJStructuralRequirement, AHJRoofMountRequirement, AHJPermits
    )
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404
from app.serializer import (
    AHJDetailSerializer, AHJSolarRequirementSerializer, AHJRemarkSerializer, AHJElectricalRequirementSerializer, AHJGroundMountRequirementSerializer,
    StateSpecificInformationSerializer, AHJSafetyInstructionsSerializer, AHJLabelSerializer, AHJSafetyInstructionsSerializer,
    ReferenceCodesSerializer, AHJEnvironmentalDataSerializer, PermitTypeSerializer, AHJStructuralRequirementSerializer, AHJRoofMountRequirementSerializer,
    AHJPermitsSerializer
)
from app.mixins import ApiTokenValidityCheckMixin
import logging
logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class AHJDetailView(ApiTokenValidityCheckMixin, View):
    def get(self, request, id=None):
        try:
            if not id:
                name_filter = request.GET.get('name', '')
                ahjs = AHJ.objects.filter(name__icontains=name_filter).values('id', 'name')

                return JsonResponse(
                    {
                        "error":None,
                        "message":"AHJs fetched successfully!",
                        "data": list(ahjs)
                    }
                    ,status=status.HTTP_200_OK
                )
        except Exception as e:
            logger.error(f"Failed to get AHJ info: {e}", exc_info=True)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while fetching ahjs. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            ahj = get_object_or_404(AHJ, id=id)
            ahj_serializer = AHJDetailSerializer(ahj)
            data={
                "ahj":ahj_serializer.data,
                # "ahj_solar_requirement":None,
                "ahj_environmental_data":None,
                "ahj_structural_requirement":None,
                "ahj_electrical_requirement":None,
                # "ahj_setback_requirement":None,
                "ahj_ground_mount_requirement":None,
                # "ahj_roof_mount_requirement": None,
                # "ahj_solar_fire_requirement": None,
                "state_specific_ic_codes": None,
                "permit_required": None,
                "ahj_permits": None,
                "ahj_label": None,
                "ahj_safety_instructions":None,
                "reference_codes": [],
                
                # "remarks": []
            }
            ahj_solar_requirement = AHJSolarRequirement.objects.filter(ahj_id=id).first()
            state = State.objects.get(code=ahj.state_code)
            state_specific_ic_codes = state.specific_information.all()

            # ahj_remarks = AHJRemark.objects.filter(ahj_id=ahj.id).all()
            # ahj_remarks_serializer = AHJRemarkSerializer(ahj_remarks, many=True)
            # data["remarks"] = ahj_remarks_serializer.data

            if state_specific_ic_codes:
                state_specific_ic_codes_serializer = StateSpecificInformationSerializer(state_specific_ic_codes, many=True)
                data["state_specific_ic_codes"] = [item["state_specific_ic_code"] for item in state_specific_ic_codes_serializer.data]

            # if ahj_solar_requirement: 
            #     ahj_solar_requirement_serializer = AHJSolarRequirementSerializer(ahj_solar_requirement)
            #     data["ahj_solar_requirement"] = ahj_solar_requirement_serializer.data
            
            ahj_electrical_requirement = AHJElectricalRequirement.objects.filter(ahj_id=id).first()
            if ahj_electrical_requirement:
                ahj_electrical_requirement_serializer = AHJElectricalRequirementSerializer(ahj_electrical_requirement)
                data["ahj_electrical_requirement"] = ahj_electrical_requirement_serializer.data
            
            # ahj_setback_requirement = AHJSetbackRequirement.objects.filter(ahj_id=id).first()
            # if ahj_setback_requirement:
            #     ahj_setback_requirement_serialzer = AHJSetbackRequirementSerializer(ahj_setback_requirement)
            #     data["ahj_setback_requirement"] = ahj_setback_requirement_serialzer.data 
            
            ahj_ground_mount_requirement = AHJGroundMountRequirement.objects.filter(ahj_id=id).first()
            if ahj_ground_mount_requirement:
                ahj_ground_mount_requirement_serializer = AHJGroundMountRequirementSerializer(ahj_ground_mount_requirement)
                data["ahj_ground_mount_requirement"] = ahj_ground_mount_requirement_serializer.data

            ahj_label = AHJLabel.objects.filter(ahj_id=id).all()
            if ahj_label.exists():
                data["ahj_label"] = [label.label_name for label in ahj_label]


            ahj_safety_instructions = AHJSafetyInstructions.objects.filter(ahj_id=id).all()
            if ahj_safety_instructions:
                ahj_safety_instructions_serializer = AHJSafetyInstructionsSerializer(ahj_safety_instructions, many=True)
                data["ahj_safety_instructions"] = ahj_safety_instructions_serializer.data

            ahj_code_mappings = AHJCodeMapping.objects.filter(ahj_id = id).all()
            
            reference_codes = [mapping.code for mapping in ahj_code_mappings]
            code_serializer = ReferenceCodesSerializer(reference_codes, many=True)
            data["reference_codes"] = code_serializer.data

            ahj_environmental_data = AHJEnvironmentalData.objects.filter(ahj_id=id).first()
            if ahj_environmental_data:
                ahj_environmental_data_serializer = AHJEnvironmentalDataSerializer(ahj_environmental_data)
                data["ahj_environmental_data"] = ahj_environmental_data_serializer.data


            ahj_permit_mappings = AHJPermitMapping.objects.filter(ahj_id = id).all()
            
            permits = [mapping.ahj_permit_type.type for mapping in ahj_permit_mappings]
            data["permit_required"] = permits

            ahj_structural_requirement = AHJStructuralRequirement.objects.filter(ahj_id=id).first()
            if ahj_structural_requirement:
                ahj_structural_requirement_serializer = AHJStructuralRequirementSerializer(ahj_structural_requirement)
                data["ahj_structural_requirement"] = ahj_structural_requirement_serializer.data
            
            # ahj_roof_mount_requirement = AHJRoofMountRequirement.objects.filter(ahj_id=id).first()
            # if ahj_roof_mount_requirement:
            #     ahj_roof_mount_requirement_serializer = AHJRoofMountRequirementSerializer(ahj_roof_mount_requirement)
            #     data["ahj_roof_mount_requirement"] = ahj_roof_mount_requirement_serializer.data

            # ahj_solar_fire_requirement = AHJSolarFireRequirements.objects.filter(ahj_id=id).first()
            # if ahj_solar_fire_requirement:
            #     ahj_environmental_data_serializer = AHJSolarFireRequirementsSerializer(ahj_solar_fire_requirement)
            #     data["ahj_solar_fire_requirement"] = ahj_environmental_data_serializer.data

            ahj_permits = AHJPermits.objects.filter(ahj_id=id).first()
            if ahj_permits:
                ahj_permits_serializer = AHJPermitsSerializer(ahj_permits)
                data["ahj_permits"] = ahj_permits_serializer.data


            # create entry in api_usage after successfull api hit
            try:
                ApiUsage.objects.create(
                    user=request.api_token.user,
                    api_name="getAHJInfoForAhjId",
                    data_id=id,
                )
            except Exception as e:
                logger.error(f"Failed to log API usage: {e}", exc_info=True)

            return JsonResponse(
                {
                    "error":None,
                    "message":"AHJ data fetched successfully",
                    "data":data
                }
                ,status=status.HTTP_200_OK
            )
        except Http404:
            return JsonResponse({
                "error": "NOT_FOUND",
                "message": f"AHJ with id {id} does not exist."
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Failed to get AHJ info: {e}", exc_info=True)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while fetching ahj. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name="dispatch")
class AHJRemarkView(ApiTokenValidityCheckMixin, View):
    def get(self, request, id, remark_id=None):
        try:
            if not remark_id:
                ahj = get_object_or_404(AHJ, id=id)
                remarks = AHJRemark.objects.filter(ahj_id=ahj.id)
                remarks_serializer = AHJRemarkSerializer(remarks, many=True)

                return JsonResponse(
                    {
                        "error":None,
                        "message":"AHJ Remarks fetched successfully!",
                        "data": remarks_serializer.data
                    }
                    ,status=status.HTTP_200_OK
                )
        except Http404:
            return JsonResponse({
                "error": "NOT_FOUND",
                "message": f"AHJ with id {id} does not exist."
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Failed to get AHJ info: {e}", exc_info=True)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while fetching ahjs. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            ahj = get_object_or_404(AHJ, id=id)
            remark = get_object_or_404(AHJRemark, id=remark_id, ahj_id=ahj.id)
            remarks_serializer = AHJRemarkSerializer(remark)

            return JsonResponse(
                {
                    "error":None,
                    "message":"AHJ Remark fetched successfully!",
                    "data": remarks_serializer.data
                }
                ,status=status.HTTP_200_OK
            )
        except Http404:
            return JsonResponse({
                "error": "NOT_FOUND",
                "message": f"Remark {remark_id} for AHJ with id {id} does not exist."
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Failed to get AHJ info: {e}", exc_info=True)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while fetching ahj. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request, id):
        try:
            body = JSONParser().parse(request)
            remark_text = body.get("remark", None)

            if not remark_text:
                return JsonResponse({
                    "error": "REMARK_TEXT_REQUIRED",
                    "message": "The remark text must be present and not empty."
                }, status=400)

            ahj = get_object_or_404(AHJ, id=id)

            with transaction.atomic():
                remark = AHJRemark.objects.create(
                    remark = remark_text,
                    created_by = request.api_token.user,
                    ahj = ahj
                )

                remark.save()

            return JsonResponse(
                {
                    "error":None,
                    "message":"AHJ Remark created successfully!",
                }
                ,status=status.HTTP_201_CREATED
            )
        except Http404:
            return JsonResponse({
                "error": "NOT_FOUND",
                "message": f"AHJ with id {id} does not exist."
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Failed to get AHJ info: {e}", exc_info=True)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while fetching ahjs. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request, id, remark_id):
        try:
            body = JSONParser().parse(request)
            remark_text = body.get("remark", None)

            if not remark_text:
                return JsonResponse({
                    "error": "REMARK_TEXT_REQUIRED",
                    "message": "The remark text must be present and not empty."
                }, status=400)

            ahj = get_object_or_404(AHJ, id=id)
            remark = get_object_or_404(AHJRemark, id=remark_id, ahj_id=ahj.id)

            with transaction.atomic():
                remark.remark = remark_text
                remark.updated_by = request.api_token.user
                remark.save()

            return JsonResponse(
                {
                    "error":None,
                    "message":"AHJ Remark updated successfully!",
                }
                ,status=status.HTTP_200_OK
            )
        except Http404:
            return JsonResponse({
                "error": "NOT_FOUND",
                "message": f"Remark {remark_id} for AHJ with id {id} does not exist."
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Failed to get AHJ info: {e}", exc_info=True)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while fetching ahjs. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
