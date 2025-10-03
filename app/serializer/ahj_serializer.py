from rest_framework import serializers
from app.models import (
    AHJ,
    AHJSolarRequirement,
    AHJRemark,
    AHJElectricalRequirement,
    AHJStructuralSetbackRequirement,
    AHJGroundMountRequirement,
    AHJSafetyInstructions,
    AHJLabel, 
    AHJEnvironmentalData,
    AHJStructuralRequirement,
    AHJRoofMountRequirement
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
        exclude = ('id',)


class AHJStructuralRequirementSerializer(serializers.ModelSerializer):

    class Meta:
        model = AHJStructuralRequirement
        exclude = ('id', 'ahj', 'created_at', 'updated_at',)

class AHJRoofMountRequirementSerializer(serializers.ModelSerializer):
    height_restriction = serializers.SerializerMethodField()
    installation_requirements = serializers.SerializerMethodField()
    restrictions = serializers.SerializerMethodField()

    class Meta:
        model = AHJRoofMountRequirement
        fields = ["permitted_zones", "height_restriction", "installation_requirements", "restrictions"]
    
    def get_height_restriction(self, object: AHJRoofMountRequirement):
        return {
            "maximum_above_roof": object.maximum_above_roof,
            "included_in_building_height": object.included_in_building_height
        }

    def get_installation_requirements(self, object: AHJRoofMountRequirement):
        return {
            "roof_boundary_setback": object.roof_boundary_setback,
            "manual_shutoff_required": object.manual_shutoff_required,
            "shutoff_location": object.shutoff_location,
            "nec_placard_required": object.nec_placard_required,
            "placard_location": object.placard_location
        }

    def get_restrictions(self, object: AHJRoofMountRequirement):
        return {
            "front_yard": object.front_yard
        }
