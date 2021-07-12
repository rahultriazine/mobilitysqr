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
    compl_ans = serializers.SerializerMethodField()
    emp_code = serializers.SerializerMethodField()
    date_created = serializers.SerializerMethodField()

    class Meta:
        model = Compliance
        fields = ['id','emp_code','question_id','compl_ques','compl_ans','date_created']

    def get_compl_ans(self, instance):
        return False

    def get_emp_code(self, instance):
        return ''
    def get_date_created(selfs, instance):
        return ''



class Employee_complianceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee_compliance
        # fields ='__all__'
        fields = ['id', 'emp_code', 'question_id', 'compl_ques', 'compl_ans','date_created']