from rest_framework import serializers
from mobility_apps.master.models import Visa_Purpose

class Visa_PurposeSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Visa_Purpose
        # fields = ('firstname','lastname')
        fields = '__all__'

