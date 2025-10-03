from rest_framework import serializers
from app.models import (
    AHJ,
    AHJSolarRequirement,
    AHJRemark,
    AHJElectricalRequirement,
    AHJStructuralSetbackRequirement,
    AHJGroundMountRequirement,
)

class AHJSolarRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AHJSolarRequirement
        exclude = ('ahj', 'created_at', 'updated_at')

class AHJRemarkSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="created_by.full_name", read_only=True)
    class Meta:
        model = AHJRemark
        exclude = ('ahj', 'updated_at', 'updated_by','created_by')

class AHJElectricalRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AHJElectricalRequirement
        exclude = ('id', 'ahj', 'created_at', 'updated_at')

class AHJStructuralSetbackRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AHJStructuralSetbackRequirement
        exclude = ('id', 'ahj', 'created_at', 'updated_at')

class AHJGroundMountRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AHJGroundMountRequirement
        exclude = ('id', 'ahj', 'created_at', 'updated_at')


class AHJDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AHJ
        exclude = ('created_at', 'updated_at', 'created_by', 'updated_by')
