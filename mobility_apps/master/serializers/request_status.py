from rest_framework import serializers
from mobility_apps.master.models import Request_Status


class Request_StatusSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Request_Status
        # fields = ('firstname','lastname')
        fields = '__all__'

