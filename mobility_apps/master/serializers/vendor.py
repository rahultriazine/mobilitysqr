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