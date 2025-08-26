from rest_framework import serializers
from app.models import (
    Utility, UtilityRequirement, UtilityICApplicationRequirement,
    UtilityData, UtilityProductionMeterRequirement
)


class UtilityRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityRequirement
        exclude = ("id", "utility", "created_at", "updated_at")


class UtilityICApplicationRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityICApplicationRequirement
        exclude = ("id", "utility", "created_at", "updated_at")


class UtilityDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityData
        exclude = ("id", "utility", "created_at", "updated_at")


class UtilityProductionMeterRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityProductionMeterRequirement
        exclude = ("id", "utility", "created_at", "updated_at")


class UtilityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utility
        exclude = ("id", "created_at", "updated_at", "created_by", "updated_by")
