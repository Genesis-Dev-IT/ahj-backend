from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
from django.db import transaction
from app.models import (
    Vertical, RequirementBlock, VerticalBlockMapping
)
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.http import Http404
from app.mixins import ApiTokenValidityCheckMixin
import logging
logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class Verticals(ApiTokenValidityCheckMixin, View):
    def get(self, request):
        name_filter = request.GET.get('filter', '')

        try:
            verticals = Vertical.objects.all()
            if name_filter:
                verticals = verticals.filter(name__icontains=name_filter)

                if not verticals.exists():
                    raise Http404("No verticals found")

            data = []
            for v in verticals:
                mappings = VerticalBlockMapping.objects.filter(vertical=v).select_related("requirement_block")
                blocks = [m.requirement_block.name for m in mappings]

                data.append({
                    "vertical": v.name,
                    "description": v.description,
                    "blocks": blocks
                })

            return JsonResponse(
                {
                    "error": None, 
                    "message": "Verticals fetched successfully",
                    "data": data
                },
                status=status.HTTP_200_OK
            )

        except Http404:
            return JsonResponse({
                "error": "NOT_FOUND",
                "message": "Vertical does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Failed to get vertical info: {e}", exc_info=True)
            return JsonResponse({
                "error": "SERVER_ERROR",
                "message": "Something went wrong while fetching verticals. Please try again later."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
