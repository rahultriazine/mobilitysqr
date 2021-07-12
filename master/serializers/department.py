from rest_framework import serializers
from mobility_apps.master.models import Department


class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Department
        # fields = ('firstname','lastname')
        fields = '__all__'

