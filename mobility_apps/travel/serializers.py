from rest_framework import serializers
from .models import Travel_Vendor_Immigration, Travel_Request ,Travel_Request_Details,Travel_Request_Dependent,Travel_Request_Draft,Travel_Request_Details_Draft,Travel_Request_Dependent_Draft,Travel_Request_Action_History,Visa_Request_Action_History,Assignment_Travel_Request_Status,Assignment_Travel_Tax_Grid

class Travel_RequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Travel_Request
        fields = '__all__'

class Travel_Request_DetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Travel_Request_Details
        fields = '__all__'



class Travel_Request_DependentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Travel_Request_Dependent
        fields = '__all__'


class Travel_Request_DraftSerializers(serializers.ModelSerializer):
    class Meta:
        model = Travel_Request_Draft
        fields = '__all__'



class Travel_Request_Details_DraftSerializers(serializers.ModelSerializer):
    class Meta:
        model = Travel_Request_Details_Draft
        fields = '__all__'



class Travel_Request_Dependent_DraftSerializers(serializers.ModelSerializer):
    class Meta:
        model = Travel_Request_Dependent_Draft
        fields = '__all__'


class Travel_Request_Action_HistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Travel_Request_Action_History
        fields = '__all__'

class Visa_Request_Action_HistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Visa_Request_Action_History
        fields = '__all__'
		
		
class Assignment_Travel_Request_StatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = Assignment_Travel_Request_Status
        fields = '__all__'


class Assignment_Travel_Tax_GridSerializers(serializers.ModelSerializer):
    class Meta:
        model = Assignment_Travel_Tax_Grid
        fields = '__all__'

class Travel_Vendor_ImmigrationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Travel_Vendor_Immigration
        fields = '__all__'