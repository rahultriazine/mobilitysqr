from rest_framework import serializers
from . models import Vault_type,Vault_type_info



class Vault_typeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vault_type
        fields = '__all__'


class Vault_type_infoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vault_type_info
        fields = '__all__'