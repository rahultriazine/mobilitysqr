
from rest_framework import serializers
from mobility_apps.master.models import Assignment_Type,Create_Assignment,Secondory_Assignment,Assignment_Extension

class Assignment_TypeSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Assignment_Type
        # fields = ('firstname','lastname')
        fields = '__all__'

class Create_AssignmentSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Create_Assignment
        # fields = ('firstname','lastname')
        fields = '__all__'


class Secondory_AssignmentSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Secondory_Assignment
        # fields = ('firstname','lastname')
        fields = '__all__'


class Assignment_ExtensionSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Assignment_Extension
        # fields = ('firstname','lastname')
        fields = '__all__'