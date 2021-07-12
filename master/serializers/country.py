# from rest_framework import serializers
# from retail.core.models import Brand

from rest_framework import serializers
from mobility_apps.master.models import Country,City,Per_Diem,Dial_Code,Country_Master,State_Master,Location_Master,Taxgrid_Master,Taxgrid_Country,Taxgrid,National_Id,Designation,Country_Policy
class CountrySerializers(serializers.ModelSerializer):
    class Meta:
        model =  Country
        # fields = ('firstname','lastname')
        fields = '__all__'

class CitySerializers(serializers.ModelSerializer):
    class Meta:
        model =  City
        # fields = ('firstname','lastname')
        fields = '__all__'

class Per_DiemSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Per_Diem
        # fields = ('firstname','lastname')
        fields = '__all__'

class Dial_CodeSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Dial_Code
        # fields = ('firstname','lastname')
        fields = '__all__'

class Country_MasterSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Country_Master
        # fields = ('firstname','lastname')
        fields = '__all__'

class State_MasterSerializers(serializers.ModelSerializer):
    class Meta:
        model =  State_Master
        # fields = ('firstname','lastname')
        fields = '__all__'


class Location_MasterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Location_Master
        # fields = ('firstname','lastname')
        fields = '__all__'



class Taxgrid_MasterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Taxgrid_Master
        # fields = ('firstname','lastname')
        fields = '__all__'


class Taxgrid_CountrySerializers(serializers.ModelSerializer):
    class Meta:
        model = Taxgrid_Country
        # fields = ('firstname','lastname')
        fields = '__all__'


class TaxgridSerializers(serializers.ModelSerializer):
    class Meta:
        model = Taxgrid
        # fields = ('firstname','lastname')
        fields = '__all__'
		
class National_IdSerializers(serializers.ModelSerializer):
    class Meta:
        model = National_Id
        # fields = ('firstname','lastname')
        fields = '__all__'


class DesignationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Designation
        # fields = ('firstname','lastname')
        fields = '__all__'


class Country_PolicySerializers(serializers.ModelSerializer):
    class Meta:
        model = Country_Policy
        # fields = ('firstname','lastname')
        fields = '__all__'