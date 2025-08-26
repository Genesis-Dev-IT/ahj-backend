from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from app.models import (
        Utility, UtilityData, UtilityICApplicationRequirement, UtilityProductionMeterRequirement, UtilityRequirement
    )
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404
from app.serializer import (
    UtilityDataSerializer, UtilityDetailSerializer, UtilityICApplicationRequirementSerializer, UtilityProductionMeterRequirementSerializer,
    UtilityRequirementSerializer
)
@method_decorator(csrf_exempt, name="dispatch")
class UtilityDetailView(View):
    def get(self, request, id):
        try:
            utility = get_object_or_404(Utility, id=id)
            utility_serializer = UtilityDetailSerializer(utility)
            data={
                "utility":utility_serializer.data,
                "utility_requirement":None,
                "utility_ic_application_requirement":None,
                "utility_data":None,
                "utility_production_meter_requirement":None,
            }

            utility_requirement = UtilityRequirement.objects.filter(utility_id=id).first()
            if utility_requirement:
                utility_requirement_serializer = UtilityRequirementSerializer(utility_requirement)
                data["utility_requirement"] = utility_requirement_serializer.data

            utility_ic_application_requirement = UtilityICApplicationRequirement.objects.filter(utility_id=id).first()
            if utility_ic_application_requirement:
                utility_ic_application_requirement_serializer = UtilityICApplicationRequirementSerializer(utility_ic_application_requirement)
                data["utility_ic_application_requirement"]=utility_ic_application_requirement_serializer.data
            
            utility_data = UtilityData.objects.filter(utility_id=id).first()
            if utility_data:
                utility_data_serializer = UtilityDataSerializer(utility_data)
                data["utility_data"] = utility_data_serializer.data
            
            utility_production_meter_requirement = UtilityProductionMeterRequirement.objects.filter(utility_id=id).first()
            if utility_production_meter_requirement:
                utility_production_meter_requirement_serialzer = UtilityProductionMeterRequirementSerializer(utility_production_meter_requirement)
                data["utility_production_meter_requirement"] = utility_production_meter_requirement_serialzer.data 
            
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
            print("Unexpected error:", e)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while fetching user. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    