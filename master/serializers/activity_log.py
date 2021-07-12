from rest_framework import serializers
from mobility_apps.master.models import Activity_Log


class Activity_LogSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Activity_Log
        # fields = ('firstname','lastname')
        fields = '__all__'

