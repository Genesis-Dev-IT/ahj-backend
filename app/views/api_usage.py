from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import ApiUsage, AHJ, Utility
from app.mixins import ApiTokenValidityCheckMixin


class AHJSearchHistoryView(ApiTokenValidityCheckMixin, APIView):
    def get(self, request):
        user = getattr(request.api_token, 'user', None)
        if not user:
            return Response(
                {"error": "UNAUTHORIZED", "message": "Invalid or missing API token."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        queryset = (
            ApiUsage.objects
            .filter(user=user, api_name="getAHJInfoForAhjId")
            .order_by('data_id', '-created_at')
            .distinct('data_id')[:50]
        )

        # Sort by latest timestamp
        usages = sorted(queryset, key=lambda x: x.created_at, reverse=True)

        data = []
        for usage in usages:
            ahj = AHJ.objects.filter(id=usage.data_id).first()
            data.append({
                "data_id": usage.data_id,
                "search_ts": usage.created_at,
                "ahj_name": ahj.name if ahj else None,
            })

        return Response({"data": data})


class UtilitySearchHistoryView(ApiTokenValidityCheckMixin, APIView):
    def get(self, request):
        user = getattr(request.api_token, 'user', None)
        if not user:
            return Response(
                {"error": "UNAUTHORIZED", "message": "Invalid or missing API token."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        queryset = (
            ApiUsage.objects
            .filter(user=user, api_name="getUtilityInfoForUtilityId")
            .order_by('data_id', '-created_at')
            .distinct('data_id')[:50]
        )

        usages = sorted(queryset, key=lambda x: x.created_at, reverse=True)

        data = []
        for usage in usages:
            utility = Utility.objects.filter(id=usage.data_id).first()
            data.append({
                "data_id": usage.data_id,
                "search_ts": usage.created_at,
                "utility_name": utility.name if utility else None,
            })

        return Response({"data": data})
