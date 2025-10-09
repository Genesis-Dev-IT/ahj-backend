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
        exclude = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by', 'data_source')

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
    height_restriction = serializers.SerializerMethodField()
    restrictions = serializers.SerializerMethodField()

    class Meta:
        model = AHJRoofMountRequirement
        fields = ["permitted_zones", "height_restriction", "restrictions"]
    
    def get_height_restriction(self, object: AHJRoofMountRequirement):
        return {
            "height_restriction_remarks": object.height_restriction_remarks,
        }

    def get_restrictions(self, object: AHJRoofMountRequirement):
        return {
            "restriction_remarks": object.restriction_remarks
        }
    

# class AHJSolarFireRequirementsSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = AHJSolarFireRequirements
#         exclude = ('id','ahj', 'created_at', 'updated_at', )


class AHJPermitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AHJPermits
        exclude = ('id','ahj', 'created_at', 'updated_at', )