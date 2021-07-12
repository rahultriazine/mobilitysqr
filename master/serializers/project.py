from rest_framework import serializers
from mobility_apps.master.models import Project

class ProjectSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Project
        # fields = ('firstname','lastname')
        fields = '__all__'

