from rest_framework import serializers
from app.models import (
    Utility, ProjectLevel, SolarUtility, SolarUtilityPart1Requirement, SolarUtilityPart2Requirement,
)

class ProjectLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLevel
        exclude = ('id',)

class SolarUtilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarUtility
        exclude = ("id", "utility", "created_at", "updated_at")

class SolarUtilityPart1RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarUtilityPart1Requirement
        exclude = ("id", "solar_utility", "created_at", "updated_at",)

class SolarUtilityPart2RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarUtilityPart2Requirement
        exclude = ("id", "solar_utility","created_at", "updated_at",)

class UtilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Utility
        exclude = ("id", "created_at", "updated_at", "created_by", "updated_by")
