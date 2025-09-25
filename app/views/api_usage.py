from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from app.models import ApiUsage
from app.serializer import ApiUsageSerializer
from app.mixins import ApiTokenValidityCheckMixin

class ApiUsageHistoryView(ApiTokenValidityCheckMixin, APIView):
    def get(self, request):
        user = getattr(request.api_token, 'user', None)
        if not user:
            return Response({"error": "UNAUTHORIZED", "message": "Invalid or missing API token."}, status=status.HTTP_401_UNAUTHORIZED)
        
        api_name = request.GET.get('api_name', None)

        queryset = ApiUsage.objects.filter(user=user)
        if api_name:
            queryset = queryset.filter(api_name=api_name)

        distinct_usages = queryset.order_by('data_id', '-created_at').distinct('data_id')[:50]

        sorted_usages = sorted(distinct_usages, key=lambda x: x.created_at, reverse=True)

        serializer = ApiUsageSerializer(sorted_usages, many=True)
        return Response({
            "error": None,
            "message": "API usage history fetched successfully",
            "data": serializer.data
        })
