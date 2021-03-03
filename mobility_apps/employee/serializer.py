from rest_framework import serializers
from . models import Employee, Employee_Passport_Detail, Employee_Visa_Detail,Employee_Address,Employee_Emails,Employee_Phones,Employee_Nationalid,Employee_Emergency_Contact,Userinfo,Employee_Org_Info,Calender_Events


class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Employee
        fields = '__all__'


class UserinfoSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Userinfo
        fields = '__all__'

class Employee_Passport_DetailSerializers(serializers.ModelSerializer):
  
    class Meta:
        model =  Employee_Passport_Detail
        #fields = ('id','reporting_manager ','passport_number','passport_expiry_date', 'department', 'job_title photo')
        fields = '__all__'


class Employee_Visa_DetailSerializers(serializers.ModelSerializer):
   # employees = EmployeeSerializers()
    #employees_details = Employee_DetailSerializers()
    class Meta:
        model =  Employee_Visa_Detail
        #fields = ('id','visa_number','visa_expiry_date','visa_country' ,'employees','employees_details')
        fields = '__all__'

class Employee_AddressSerializers(serializers.ModelSerializer):
    # employees = EmployeeSerializers()
    #employees_details = Employee_DetailSerializers()
    class Meta:
        model =  Employee_Address
        #fields = ('id','visa_number','visa_expiry_date','visa_country' ,'employees','employees_details')
        fields = '__all__'



class Employee_EmailsSerializers(serializers.ModelSerializer):
    # employees = EmployeeSerializers()
    #employees_details = Employee_DetailSerializers()
    class Meta:
        model =  Employee_Emails
        #fields = ('id','visa_number','visa_expiry_date','visa_country' ,'employees','employees_details')
        fields = '__all__'

class Employee_NationalidSerializers(serializers.ModelSerializer):
    # employees = EmployeeSerializers()
    #employees_details = Employee_DetailSerializers()
    class Meta:
        model =  Employee_Nationalid
        #fields = ('id','visa_number','visa_expiry_date','visa_country' ,'employees','employees_details')
        fields = '__all__'


class Employee_Emergency_ContactSerializers(serializers.ModelSerializer):
    # employees = EmployeeSerializers()
    #employees_details = Employee_DetailSerializers()
    class Meta:
        model =  Employee_Emergency_Contact
        #fields = ('id','visa_number','visa_expiry_date','visa_country' ,'employees','employees_details')
        fields = '__all__'


class Employee_PhonesSerializers(serializers.ModelSerializer):
    # employees = EmployeeSerializers()
    #employees_details = Employee_DetailSerializers()
    class Meta:
        model =  Employee_Phones
        #fields = ('id','visa_number','visa_expiry_date','visa_country' ,'employees','employees_details')
        fields = '__all__'


class Employee_Org_InfoSerializers(serializers.ModelSerializer):
    # employees = EmployeeSerializers()
    #employees_details = Employee_DetailSerializers()
    class Meta:
        model =  Employee_Org_Info
        #fields = ('id','visa_number','visa_expiry_date','visa_country' ,'employees','employees_details')
        fields = '__all__'


class Calender_EventsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Calender_Events
        fields = '__all__'