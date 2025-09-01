from rest_framework import serializers
from app.models import(
    StateSpecificInformation
)

class StateSpecificInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateSpecificInformation
        exclude =('id',)