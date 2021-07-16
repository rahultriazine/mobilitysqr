from rest_framework import serializers
# from mobility_apps.master.models import Vendor,Vendor_Category,Vendor_Master
from mobility_apps.master.models import *

class VendorSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Vendor
        # fields = ('firstname','lastname')
        fields = '__all__'



class Vendor_CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model =  Vendor_Category
        # fields = ('firstname','lastname')
        fields = '__all__'




class Vendor_MasterSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Vendor_Master
        # fields = ('firstname','lastname')
        fields = '__all__'


class Vendor_IncomeSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Vendor_Income
        fields = '__all__'

class Capital_Gains_IncomeSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Capital_Gains_Income
        fields = '__all__'

class Vendor_StatusSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Vendor_Status
        fields = '__all__'


class vendor_Service_ListSerializers(serializers.ModelSerializer):
    class Meta:
        model =  vendor_Service_List
        fields = '__all__'

class vendor_Service_List_statusSerializers(serializers.ModelSerializer):
    class Meta:
        model =  vendor_Service_List_status
        fields = '__all__'