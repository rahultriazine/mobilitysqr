from rest_framework import serializers
from mobility_apps.master.models import Visa,Visa_Master,Visa_Master_Applicable

class VisaSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Visa
        # fields = ('firstname','lastname')
        fields = '__all__'


class Visa_MasterSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Visa_Master
        # fields = ('firstname','lastname')
        fields = '__all__'


class Visa_Master_ApplicableSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Visa_Master_Applicable
        # fields = ('firstname','lastname')
        fields = '__all__'