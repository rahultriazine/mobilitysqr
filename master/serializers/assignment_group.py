from rest_framework import serializers
from mobility_apps.master.models import Assignment_Group,Assignment_Status

class Assignment_GroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = Assignment_Group
        # fields = ('firstname','lastname')
        fields = '__all__'

class Assignment_StatusSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Assignment_Status
        # fields = ('firstname','lastname')
        fields = '__all__'
