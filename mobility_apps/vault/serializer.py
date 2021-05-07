from rest_framework import serializers
from . models import Vault_type,Vault_type_info, Compliance, Employee_compliance



class Vault_typeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vault_type
        fields = '__all__'


class Vault_type_infoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vault_type_info
        fields = '__all__'


class ComplianceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Compliance
        fields = '__all__'


class Employee_complianceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee_compliance
        fields ='__all__'