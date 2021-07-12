from rest_framework import serializers
from mobility_apps.master.models import Role

class RoleSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Role
        # fields = ('firstname','lastname')
        fields = '__all__'

