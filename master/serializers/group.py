from rest_framework import serializers
from mobility_apps.master.models import Assignment_Group


class Assignment_GroupSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Assignment_Group
        # fields = ('firstname','lastname')
        fields = '__all__'
