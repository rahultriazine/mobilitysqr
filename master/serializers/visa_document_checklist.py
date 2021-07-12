from rest_framework import serializers
from mobility_apps.master.models import Visa_Document_Checklist


class Visa_Document_ChecklistSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Visa_Document_Checklist
        # fields = ('firstname','lastname')
        fields = '__all__'

