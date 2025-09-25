from rest_framework import serializers
from app.models import (
    AHJ,
    AHJRequirement,
    AHJRequirementRemark,
    AHJSpecificRequirement,
    AHJElectricalRequirement,
    AHJStructuralSetbackRequirement,
    AHJGroundMountRequirement,
)

class AHJRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AHJRequirement
        exclude = ('id', 'ahj', 'created_at', 'updated_at')

class AHJRequirementRemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AHJRequirementRemark
        #if id not needed add in exclude
        exclude = ('ahj_requirement', 'created_at', 'updated_at', 'created_by', 'updated_by')
        # exclude = ('id', 'ahj_requirement', 'created_at', 'updated_at', 'created_by', 'updated_by')

class AHJSpecificRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AHJSpecificRequirement
        exclude = ('id', 'ahj', 'created_at', 'updated_at')

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
        exclude = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by')
