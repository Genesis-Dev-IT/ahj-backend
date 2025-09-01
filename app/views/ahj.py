from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from app.models import (
        AHJ, AHJElectricalRequirement, AHJGroundMountRequirement, 
        AHJRequirement, AHJSpecificRequirement, AHJStructuralSetbackRequirement, ApiUsage, State, StateSpecificInformation
    )
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404
from app.serializer import (
    AHJDetailSerializer, AHJRequirementSerializer, AHJElectricalRequirementSerializer, AHJGroundMountRequirementSerializer,
    AHJSpecificRequirementSerializer, AHJStructuralSetbackRequirementSerializer, StateSpecificInformationSerializer
)
from app.mixins import ApiTokenValidityCheckMixin
import logging
logger = logging.getLogger(__name__)

# ApiTokenValidityCheckMixin,
@method_decorator(csrf_exempt, name="dispatch")
class AHJDetailView(View):
    def get(self, request, id):
        try:
            ahj = get_object_or_404(AHJ, id=id)
            ahj_serializer = AHJDetailSerializer(ahj)
            data={
                "ahj":ahj_serializer.data,
                "ahj_requirement":None,
                "ahj_specific_requirement":None,
                "ahj_electrical_requirement":None,
                "ahj_structural_setback_requirement":None,
                "ahj_ground_mount_requirement":None,
                "state_specific_ic_codes": None
            }
            ahj_requirement = AHJRequirement.objects.filter(ahj_id=id).first()
            state = State.objects.get(code=ahj.state_code)
            state_specific_ic_codes = state.specific_information.all()

            if state_specific_ic_codes:
                state_specific_ic_codes_serializer = StateSpecificInformationSerializer(state_specific_ic_codes, many=True)
                data["state_specific_ic_codes"] = state_specific_ic_codes_serializer.data

            if ahj_requirement:
                ahj_requirement_serializer = AHJRequirementSerializer(ahj_requirement)
                data["ahj_requirement"] = ahj_requirement_serializer.data

            ahj_specific_requirement = AHJSpecificRequirement.objects.filter(ahj_id=id).first()
            if ahj_specific_requirement:
                ahj_specific_requirement_serializer = AHJSpecificRequirementSerializer(ahj_specific_requirement)
                data["ahj_specific_requirement"]=ahj_specific_requirement_serializer.data
            
            ahj_electrical_requirement = AHJElectricalRequirement.objects.filter(ahj_id=id).first()
            if ahj_electrical_requirement:
                ahj_electrical_requirement_serializer = AHJElectricalRequirementSerializer(ahj_electrical_requirement)
                data["ahj_electrical_requirement"] = ahj_electrical_requirement_serializer.data
            
            ahj_structural_setback_requirement = AHJStructuralSetbackRequirement.objects.filter(ahj_id=id).first()
            if ahj_structural_setback_requirement:
                ahj_structural_setback_requirement_serialzer = AHJStructuralSetbackRequirementSerializer(ahj_structural_setback_requirement)
                data["ahj_structural_setback_requirement"] = ahj_structural_setback_requirement_serialzer.data 
            
            ahj_ground_mount_requirement = AHJGroundMountRequirement.objects.filter(ahj_id=id).first()
            if ahj_ground_mount_requirement:
                ahj_ground_mount_requirement_serializer = AHJGroundMountRequirementSerializer(ahj_ground_mount_requirement)
                data["ahj_ground_mount_requirement"] = ahj_ground_mount_requirement_serializer.data
            
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
                "message": "Something went wrong while fetching user. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    