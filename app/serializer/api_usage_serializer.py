from rest_framework import serializers
from app.models import ApiUsage

class ApiUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiUsage
        fields = ['id', 'user', 'api_name', 'data_id', 'created_at']

