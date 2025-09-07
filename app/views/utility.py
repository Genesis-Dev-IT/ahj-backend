from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from app.models import (
    Utility, ProjectLevel, SolarUtility, SolarUtilityPart1Requirement, 
    SolarUtilityPart2Requirement, ApiUsage
)
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404
from app.serializer import (
    ProjectLevelSerializer, SolarUtilitySerializer, SolarUtilityPart1RequirementSerializer,
    SolarUtilityPart2RequirementSerializer, UtilitySerializer
)
from app.mixins import ApiTokenValidityCheckMixin
import logging
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name="dispatch")
class UtilityDetailView(ApiTokenValidityCheckMixin, View):
    def get(self, request, id):
        try:
            utility = get_object_or_404(Utility, id=id)
            utility_serializer = UtilitySerializer(utility)
            data={
                "baisc_info":utility_serializer.data,
                "solar_info":None,
                "requirements":{}
            }

            solar_utility = SolarUtility.objects.filter(utility_id=id).first()
            if solar_utility:
                solar_utility_serializer = SolarUtilitySerializer(solar_utility)
                data["solar_info"] = solar_utility_serializer.data

            solar_utility_part1_requirement = SolarUtilityPart1Requirement.objects.filter(solar_utility=solar_utility.id).first()
            if solar_utility_part1_requirement:
                solar_utility_part1_requirement_serializer = SolarUtilityPart1RequirementSerializer(solar_utility_part1_requirement)
                data["requirements"]["part1"]=solar_utility_part1_requirement_serializer.data
            
            solar_utility_part2_requirement = SolarUtilityPart2Requirement.objects.filter(solar_utility=solar_utility.id).first()
            if solar_utility_part2_requirement:
                solar_utility_part2_requirement_serializer = SolarUtilityPart2RequirementSerializer(solar_utility_part2_requirement)
                data["requirements"]["part2"] = solar_utility_part2_requirement_serializer.data
            
            project_level = ProjectLevel.objects.get(id = solar_utility.project_level_id)
            project_level_serializer = ProjectLevelSerializer(project_level)
            data["solar_info"]["project_level"] = project_level_serializer.data


            # create entry in api_usage after successfull api hit
            try:
                ApiUsage.objects.create(
                    user=request.api_token.user,
                    api_name="getUtilityInfoForUtilityId",
                    data_id=id,
                )
            except Exception as e:
                logger.error(f"Failed to log API usage: {e}", exc_info=True)

            return JsonResponse(
                {
                    "error":None,
                    "message":"Utility data fetched successfully",
                    "data":data
                }
                ,status=status.HTTP_200_OK
            )
        except Http404:
            return JsonResponse({
                "error": "NOT_FOUND",
                "message": f"Utility with id {id} does not exist."
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Failed to get Utility info: {e}", exc_info=True)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while fetching user. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    