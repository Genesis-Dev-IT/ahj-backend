from rest_framework import serializers
from app.models import (
     ReferenceCodes, 
     PermitType, 
     StandardLabels
)

class ReferenceCodesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReferenceCodes
        exclude = ('id',)

class PermitTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermitType
        exclude = ('id',)

class StandardLabelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = StandardLabels
        exclude = ('id', 'ahj',)
        
