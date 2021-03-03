from rest_framework import serializers
from mobility_apps.master.models import Gender,Marital_Status,Salutation,Acedmic_Title,Name_Suffix,Email_Type,Phone_Type,Relation,Termination_Reasons,Address_Type,Language


class GenderSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Gender
        # fields = ('firstname','lastname')
        fields = '__all__'

class Marital_StatusSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Marital_Status
        # fields = ('firstname','lastname')
        fields = '__all__'

class SalutationSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Salutation
        # fields = ('firstname','lastname')
        fields = '__all__'


class Acedmic_TitleSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Acedmic_Title
        # fields = ('firstname','lastname')
        fields = '__all__'


class Name_SuffixSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Name_Suffix
        # fields = ('firstname','lastname')
        fields = '__all__'


class Email_TypeSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Email_Type
        # fields = ('firstname','lastname')
        fields = '__all__'


class Phone_TypeSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Phone_Type
        # fields = ('firstname','lastname')
        fields = '__all__'


class RelationSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Relation
        # fields = ('firstname','lastname')
        fields = '__all__'

class Termination_ReasonsSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Termination_Reasons
        # fields = ('firstname','lastname')
        fields = '__all__'

class Address_TypeSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Address_Type
        # fields = ('firstname','lastname')
        fields = '__all__'

class LanguageSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Language
        # fields = ('firstname','lastname')
        fields = '__all__'

