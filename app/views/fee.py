from rest_framework import generics
from app.models import Fee
from app.serializer import FeeSerializer
from app.mixins import ApiTokenValidityCheckMixin


class FeeListView(ApiTokenValidityCheckMixin, generics.ListAPIView):
    """
    Returns all Fee records.
    Supports optional filtering by AHJ ID and fee type.
    Example:
      /v1/fees?ahj_id=7
      /v1/fees?type=fire
    """

    serializer_class = FeeSerializer

    def get_queryset(self):
        queryset = Fee.objects.all().order_by("type", "id")

        # Filter by AHJ ID
        ahj_id = self.request.query_params.get("ahj_id")
        if ahj_id:
            queryset = queryset.filter(ahj_id=ahj_id)

        # Filter by Fee type (building, fire, electric, etc.)
        fee_type = self.request.query_params.get("type")
        if fee_type:
            queryset = queryset.filter(type=fee_type)

        # Optional text search by item name
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(item__icontains=search)

        return queryset


class FeeDetailView(ApiTokenValidityCheckMixin, generics.RetrieveAPIView):
    """
    Returns a single Fee record by ID.
    Example:
      /v1/fees/42
    """

    queryset = Fee.objects.all()
    serializer_class = FeeSerializer
    lookup_field = "id"
