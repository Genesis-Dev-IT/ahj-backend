from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from app.models import (ZipcodeAHJMapping, ZipcodeUtilityMapping)
from rest_framework import status

@method_decorator(csrf_exempt, name="dispatch")
class ZipCodeAHJUtilityMappingDetailView(View):
    def get(self, request, id):
        try:
            zipcode_ahjs_mapping = ZipcodeAHJMapping.objects.filter(zipcode=id).select_related("ahj")
            ahjs = [
                {"id": z.ahj.id, "name": z.ahj.name}
                for z in zipcode_ahjs_mapping if z.ahj is not None
            ]

            zipcode_utility_mapping = ZipcodeUtilityMapping.objects.filter(zipcode=id).select_related("utility")
            utilities = [
                {"id": z.utility.id, "name": z.utility.name}
                for z in zipcode_utility_mapping if z.utility is not None
            ]

            return JsonResponse({
                "error":None,
                "message":"AHJs, Utility fetched successfully",
                "data": {
                    "ahjs": ahjs,
                    "utilities": utilities
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while fetching user. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)