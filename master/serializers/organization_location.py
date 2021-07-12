from rest_framework import serializers
from mobility_apps.master.models import Organization_Location


class Organization_LocationSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Organization_Location
        # fields = ('firstname','lastname')
        fields = '__all__'

