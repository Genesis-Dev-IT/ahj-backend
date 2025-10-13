from rest_framework import serializers
from app.models import (
    AHJ,
    AHJSolarRequirement,
    AHJRemark,
    AHJElectricalRequirement,
    AHJGroundMountRequirement,
    AHJSafetyInstructions,
    AHJLabel, 
    AHJEnvironmentalData,
    AHJStructuralRequirement,
    AHJRoofMountRequirement,
    AHJPermits
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
        exclude = ('id', 'ahj', 'created_at', 'updated_at', 'pv_meter_required_remarks')

# class AHJSetbackRequirementSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AHJSetbackRequirement
#         exclude = ('id', 'ahj', 'created_at', 'updated_at')

class AHJGroundMountRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AHJGroundMountRequirement
        exclude = ('id', 'ahj', 'created_at', 'updated_at')


class AHJDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AHJ
        exclude = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by', 'data_source', 'structural_and_electrical_stamp', 'generic_forms_allowed')

class AHJSafetyInstructionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AHJSafetyInstructions
        exclude = ('id', 'ahj')

class AHJLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AHJLabel
        exclude = ('id', 'ahj')


class AHJEnvironmentalDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = AHJEnvironmentalData
        exclude = ('ahj', 'id',)


class AHJStructuralRequirementSerializer(serializers.ModelSerializer):

    class Meta:
        model = AHJStructuralRequirement
        exclude = ('id', 'ahj', 'created_at', 'updated_at',)

class AHJRoofMountRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AHJRoofMountRequirement
        exclude = ('id', 'ahj', 'created_at', 'updated_at',)
    

# class AHJSolarFireRequirementsSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = AHJSolarFireRequirements
#         exclude = ('id','ahj', 'created_at', 'updated_at', )


class AHJPermitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AHJPermits
        exclude = ('id','ahj', 'created_at', 'updated_at', )