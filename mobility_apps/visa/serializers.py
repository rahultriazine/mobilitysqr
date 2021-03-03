from rest_framework import serializers
from .models import Visa_Request ,Visa_Request_Document,Visa_Request_Draft,Visa_Request_Document_Draft

class Visa_RequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Visa_Request
        fields = '__all__'

class Visa_Request_DocumentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Visa_Request_Document
        fields = '__all__'


class Visa_Request_DraftSerializers(serializers.ModelSerializer):
    class Meta:
        model = Visa_Request_Draft
        fields = '__all__'

class Visa_Request_Document_DraftSerializers(serializers.ModelSerializer):
    class Meta:
        model = Visa_Request_Document_Draft
        fields = '__all__'