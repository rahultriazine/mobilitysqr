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


# class Vendor_IncomeSerializers(serializers.ModelSerializer):
#     class Meta:
#         model =  Vendor_Income
#         fields = '__all__'

# class Capital_Gains_IncomeSerializers(serializers.ModelSerializer):
#     class Meta:
#         model =  Capital_Gains_Income
#         fields = '__all__'

# class Vendor_StatusSerializers(serializers.ModelSerializer):
#     class Meta:
#         model =  Vendor_Status
#         fields = '__all__'


# class vendor_Service_ListSerializers(serializers.ModelSerializer):
#     class Meta:
#         model =  vendor_Service_List
#         fields = '__all__'

class vendor_Service_List_statusSerializers(serializers.ModelSerializer):
    class Meta:
        model =  vendor_Service_List_status
        fields = '__all__'


class Vaccine_Autho_CountrySerializers(serializers.ModelSerializer):
    class Meta:
        model =  Vaccine_Autho_Country
        fields = '__all__'

class Vaccine_MasterSerializers(serializers.ModelSerializer):
    vaccine_contry_detail = serializers.SerializerMethodField()
    class Meta:
        model = Vaccine_Master
        fields = ['id','vaccine_name','vaccine_company_name','vaccine_contry_detail']


    def get_vaccine_contry_detail(self, instance):
        # print('instance',instance)
        # organization =self.context['request'].organization
        data = Vaccine_Autho_Country.objects.filter(vaccine_master=instance.id)
        return Vaccine_Autho_CountryGETSerializers(data, many=True).data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["vaccine_contry_detail"] = sorted(response["vaccine_contry_detail"], key=lambda x: x["country_name"])
        return response


class Vaccine_Autho_CountryGETSerializers(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField()

    class Meta:
        model = Vaccine_Autho_Country
        fields = ['id','date_created','date_modified', 'organization', 'authorization_type', 'access_type', 'vaccine_master','country_id','country_name']

    def get_country_name(self, instance):
        data = Country_Master.objects.filter(country_id=instance.country_id).last()
        if data is not None:
            return data.name
        else:
            return None
# class Vendor_Authorized_Service_ListSerializers(serializers.ModelSerializer):
#     class Meta:
#         model =  Vendor_Authorized_Service_List
#         fields = '__all__'