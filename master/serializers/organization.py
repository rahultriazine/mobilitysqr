from rest_framework import serializers
from mobility_apps.master.models import Organization


class OrganizationSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Organization
        # fields = ('firstname','lastname')
        fields = '__all__'

