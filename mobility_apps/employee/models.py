from django.db import models
from api.models import User
from django.db.models.signals import post_delete,post_save,pre_save
# Create your models here.
from mobility_apps.base.models import TimeStampedModel, GeneratedByModel, Status
from django.utils.translation import ugettext_lazy as _
from mobility_apps.superadmin.models import *

class Userinfo(TimeStampedModel, GeneratedByModel, Status, ):
    emp_code = models.CharField(unique=True,default="emp001", max_length=100)
    person_id = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    login_method = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    termandcondtion = models.CharField(max_length=100, null=True, blank=True)
    istemporary= models.CharField(max_length=100, null=True, blank=True)
    org_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Userinfo')
        verbose_name_plural = _('Userinfo')

    def __str__(self):
        return self.emp_code

    def __unicode__(self):
        return self.emp_code


# def Remove_Userinfo_to_User(sender,instance,*args,**kwargs):
    # User.objects.filter(username=instance.email).delete()



# def Add_Userinfo_to_User(sender,instance,*args,**kwargs):
    # if instance._state.adding is True:
        # User.objects.create_user(username=instance.email,email=instance.email,password=instance.password)
    # else:
        # pass


# pre_save.connect(Add_Userinfo_to_User,sender=Userinfo)
# post_delete.connect(Remove_Userinfo_to_User,sender=Userinfo)

class Employee(TimeStampedModel, GeneratedByModel, Status, ):
    emp_code = models.CharField(max_length=50,default="emp001", unique=True)
    person_id = models.CharField(max_length=50)
    role = models.CharField(max_length=50, null=True, blank=True)
    #email = models.EmailField(max_length=100, unique=True)
    login_method = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    termandcondtion = models.CharField(max_length=100, null=True, blank=True)
    istemporary= models.CharField(max_length=100, null=True, blank=True)
    user_name = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100,null=True, blank=True)
    preferred_first_name = models.CharField(max_length=100,null=True,blank=True)
    preferred_last_name = models.CharField(max_length=100, null=True,blank=True)
    salutation = models.CharField(max_length=100, blank=True,null=True)
    initials = models.CharField(max_length=100,null=True, blank=True)
    title = models.CharField(max_length=100,null=True, blank=True)
    suffix = models.CharField(max_length=100,null=True, blank=True)
    suffix = models.CharField(max_length=100,null=True, blank=True)
    display_name = models.CharField(max_length=100, null=True, blank=True)
    formal_name = models.CharField(max_length=100, null=True, blank=True)
    birth_name = models.CharField(max_length=100, null=True, blank=True)
    name_prefix = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    marital_status = models.CharField(max_length=100, null=True, blank=True)
    marital_status_since = models.CharField(max_length=100,null=True, blank=True)
    country_of_birth = models.CharField(max_length=100, null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    second_nationality = models.CharField(max_length=100, null=True, blank=True)
    native_preferred_lang = models.CharField(max_length=100, null=True, blank=True)
    partner_name= models.CharField(max_length=100, null=True, blank=True)
    partner_name_prefix= models.CharField(max_length=100, null=True, blank=True)
    note= models.CharField(max_length=100, null=True, blank=True)
    dob = models.CharField(max_length=100,null=True, blank=True)
    place_of_birth = models.CharField(max_length=100, null=True, blank=True)
    active_start_date = models.CharField(max_length=100,default="", blank=True)
    active_end_date = models.CharField(max_length=100,default="", blank=True)
    email= models.EmailField(max_length=100, unique=True, null=True, blank=True)
    password= models.CharField(max_length=100,null=True,blank=True)
    department = models.CharField(max_length=100,null=True,blank=True)
    role = models.CharField(max_length=100,null=True,blank=True)
    photo = models.CharField(max_length=255, null=True, blank=True)
    assignment_role = models.CharField(max_length=100,null=True,blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
    supervisor= models.CharField(max_length=100, null=True, blank=True)
    last_login = models.CharField(max_length=100, null=True, blank=True)
    recent_login= models.CharField(max_length=100, null=True, blank=True)
    column1 = models.CharField(max_length=100,null=True,blank=True)
    column2 = models.CharField(max_length=100,null=True,blank=True)
    column3 = models.CharField(max_length=100,null=True,blank=True)
    column4 = models.CharField(max_length=100,null=True,blank=True)
    column5 = models.CharField(max_length=100,null=True,blank=True)
    column6 = models.CharField(max_length=100,null=True,blank=True)
    column7 = models.CharField(max_length=100,null=True,blank=True)
    column8 = models.CharField(max_length=100,null=True,blank=True)
    column9 = models.CharField(max_length=100,null=True,blank=True)
    column10 = models.CharField(max_length=100,null=True,blank=True)
    column11 = models.CharField(max_length=100,null=True,blank=True)
    column12 = models.CharField(max_length=100,null=True,blank=True)
    is_visa_denied = models.BooleanField(default=False)
    visa_denied_country = models.CharField(max_length=100, null=True, blank=True)



    class Meta:
        managed = True
        verbose_name = _('Employee')
        verbose_name_plural = _('Employee')
        models.Index(fields=['first_name', 'last_name', 'emp_code','email'])

    def __str__(self):
        return self.emp_code

    def __unicode__(self):
        return self.emp_code

def Remove_Employee_to_User(sender,instance,*args,**kwargs):
    User.objects.filter(username=instance.user_name).delete()



def Add_Employee_to_User(sender,instance,*args,**kwargs):
    if instance._state.adding is True:
        User.objects.create_user(username=instance.user_name,email=instance.email,password=instance.password)
    else:
        pass


pre_save.connect(Add_Employee_to_User,sender=Employee)
post_delete.connect(Remove_Employee_to_User,sender=Employee)

class Employee_Address(TimeStampedModel, GeneratedByModel, Status):
    emp_code = models.ForeignKey(Employee,to_field="emp_code",default="emp001",on_delete=models.CASCADE)
    address1 = models.CharField(max_length=100,null=True, blank=True)
    address2 = models.CharField(max_length=100,null=True, blank=True)
    address3 = models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=100,null=True, blank=True)
    address_type= models.CharField(max_length=100,null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    zip = models.CharField(max_length=100,null=True, blank=True)
    organization = models.ForeignKey(Organizations,to_field='org_id', null=True, blank=True, on_delete=models.CASCADE)
    column1 = models.CharField(max_length=100, null=True, blank=True)
    column2 = models.CharField(max_length=100, null=True, blank=True)
    column3 = models.CharField(max_length=100, null=True, blank=True)
    column4 = models.CharField(max_length=100, null=True, blank=True)
    column5 = models.CharField(max_length=100, null=True, blank=True)
    column6 = models.CharField(max_length=100, null=True, blank=True)
    column7 = models.CharField(max_length=100, null=True, blank=True)
    column8 = models.CharField(max_length=100, null=True, blank=True)
    column9 = models.CharField(max_length=100, null=True, blank=True)
    column10 = models.CharField(max_length=100, null=True, blank=True)
    column11 = models.CharField(max_length=100, null=True, blank=True)
    column12 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Employee Address')
        verbose_name_plural = _('Employee Address')

    def __str__(self):
        return self.emp_code

    def __unicode__(self):
        return self.emp_code
#
class Employee_Emails(TimeStampedModel, GeneratedByModel, Status):
    emp_code = models.ForeignKey(Employee,to_field="emp_code",default="emp001",on_delete=models.CASCADE)
    email_type = models.CharField(max_length=100,null=True, blank=True)
    email_address = models.EmailField(max_length=100, unique=True)
    isPrimary = models.BooleanField(default=False)
    organization = models.ForeignKey(Organizations,to_field='org_id', null=True, blank=True, on_delete=models.CASCADE)
    column1 = models.CharField(max_length=100, null=True, blank=True)
    column2 = models.CharField(max_length=100, null=True, blank=True)
    column3 = models.CharField(max_length=100, null=True, blank=True)
    column4 = models.CharField(max_length=100, null=True, blank=True)
    column5 = models.CharField(max_length=100, null=True, blank=True)
    column6 = models.CharField(max_length=100, null=True, blank=True)
    column7 = models.CharField(max_length=100, null=True, blank=True)
    column8 = models.CharField(max_length=100, null=True, blank=True)
    column9 = models.CharField(max_length=100, null=True, blank=True)
    column10 = models.CharField(max_length=100, null=True, blank=True)
    column11 = models.CharField(max_length=100, null=True, blank=True)
    column12 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Employee Emails')
        verbose_name_plural = _('Employee Emails')

    def __str__(self):
        return self.emp_code

    def __unicode__(self):
        return self.emp_code
#
class Employee_Phones(TimeStampedModel, GeneratedByModel, Status):
    emp_code = models.ForeignKey(Employee,to_field="emp_code",default="emp001",on_delete=models.CASCADE)
    phone_type = models.CharField(max_length=100,null=True, blank=True)
    country_code = models.CharField(max_length=100,null=True, blank=True)
    area_code = models.CharField(max_length=100,null=True, blank=True)
    phone_number = models.CharField(max_length=100,null=True, blank=True)
    extension = models.CharField(max_length=100,null=True, blank=True)
    isprimary =  models.BooleanField(default=False)
    organization = models.ForeignKey(Organizations,to_field='org_id', null=True, blank=True, on_delete=models.CASCADE)
    column1 = models.CharField(max_length=100, null=True, blank=True)
    column2 = models.CharField(max_length=100, null=True, blank=True)
    column3 = models.CharField(max_length=100, null=True, blank=True)
    column4 = models.CharField(max_length=100, null=True, blank=True)
    column5 = models.CharField(max_length=100, null=True, blank=True)
    column6 = models.CharField(max_length=100, null=True, blank=True)
    column7 = models.CharField(max_length=100, null=True, blank=True)
    column8 = models.CharField(max_length=100, null=True, blank=True)
    column9 = models.CharField(max_length=100, null=True, blank=True)
    column10 = models.CharField(max_length=100, null=True, blank=True)
    column11 = models.CharField(max_length=100, null=True, blank=True)
    column12 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Employee Address')
        verbose_name_plural = _('Employee Address')

    def __str__(self):
        return self.emp_code

    def __unicode__(self):
        return self.emp_code

class Employee_Nationalid(TimeStampedModel, GeneratedByModel, Status):
    emp_code = models.ForeignKey(Employee,to_field="emp_code",default="emp001",on_delete=models.CASCADE)
    country_code = models.CharField(max_length=100,null=True, blank=True)
    card_type = models.CharField(max_length=100,null=True, blank=True)
    national_id = models.CharField(max_length=100,null=True, blank=True)
    attachment_id = models.CharField(max_length=255, null=True, blank=True)
    isprimary =  models.BooleanField(default=False)
    organization = models.ForeignKey(Organizations,to_field='org_id', null=True, blank=True, on_delete=models.CASCADE)
    column1 = models.CharField(max_length=100, null=True, blank=True)
    column2 = models.CharField(max_length=100, null=True, blank=True)
    column3 = models.CharField(max_length=100, null=True, blank=True)
    column4 = models.CharField(max_length=100, null=True, blank=True)
    column5 = models.CharField(max_length=100, null=True, blank=True)
    column6 = models.CharField(max_length=100, null=True, blank=True)
    column7 = models.CharField(max_length=100, null=True, blank=True)
    column8 = models.CharField(max_length=100, null=True, blank=True)
    column9 = models.CharField(max_length=100, null=True, blank=True)
    column10 = models.CharField(max_length=100, null=True, blank=True)
    column11 = models.CharField(max_length=100, null=True, blank=True)
    column12 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Employee Nationalid')
        verbose_name_plural = _('Employee Nationalid')

    def __str__(self):
        return self.emp_code

    def __unicode__(self):
        return self.emp_code



class Employee_Emergency_Contact(TimeStampedModel, GeneratedByModel, Status):
    emp_code = models.ForeignKey(Employee,to_field="emp_code",default="emp001",on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True, blank=True)
    relationship = models.CharField(max_length=100,null=True, blank=True)
    primary_flag = models.BooleanField(default=False)
    country_code = models.CharField(max_length=100,null=True, blank=True)
    second_country_code = models.CharField(max_length=100,null=True, blank=True)
    phone = models.CharField(max_length=100,null=True, blank=True)
    second_phone =  models.CharField(max_length=100,null=True, blank=True)
    isDependent =  models.BooleanField(default=False)
    isEmergencyContact =models.BooleanField(default=False)
    gender =  models.CharField(max_length=100,null=True, blank=True)
    email =  models.CharField(max_length=100,null=True, blank=True)
    isAddSameAsEmployee =  models.BooleanField(default=False)
    address1 = models.CharField(max_length=100,null=True, blank=True)
    address2 = models.CharField(max_length=100,null=True, blank=True)
    address3 = models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=100,null=True, blank=True)
    address_type= models.CharField(max_length=100,null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=100,null=True, blank=True)
    organization = models.ForeignKey(Organizations,to_field='org_id', null=True, blank=True, on_delete=models.CASCADE)
    column1 = models.CharField(max_length=100, null=True, blank=True)
    column2 = models.CharField(max_length=100, null=True, blank=True)
    column3 = models.CharField(max_length=100, null=True, blank=True)
    column4 = models.CharField(max_length=100, null=True, blank=True)
    column5 = models.CharField(max_length=100, null=True, blank=True)
    column6 = models.CharField(max_length=100, null=True, blank=True)
    column7 = models.CharField(max_length=100, null=True, blank=True)
    column8 = models.CharField(max_length=100, null=True, blank=True)
    column9 = models.CharField(max_length=100, null=True, blank=True)
    column10 = models.CharField(max_length=100, null=True, blank=True)
    column11 = models.CharField(max_length=100, null=True, blank=True)
    column12 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Employee Emergency Contact')
        verbose_name_plural = _('Employee Emergency Contact')

    def __str__(self):
        return self.emp_code

    def __unicode__(self):
        return self.emp_code



class Employee_Passport_Detail(TimeStampedModel, GeneratedByModel, Status):
    emp_code = models.ForeignKey(Employee,to_field="emp_code",default="emp001",on_delete=models.CASCADE)
    passport_status = models.BooleanField(default=False)
    passport_number = models.CharField(max_length=20, null=True, blank=True)
    passport_expiry_date = models.CharField(max_length=50, null=True, blank=True)
    isdependent =models.BooleanField(default=False)
    relation =models.CharField(max_length=50, null=True, blank=True)
    nationality =models.CharField(max_length=50, null=True, blank=True)
    nationality =models.CharField(max_length=50, null=True, blank=True)
    country_of_issue = models.CharField(max_length=50, null=True, blank=True)
    place_of_issue = models.CharField(max_length=50, null=True, blank=True)
    date_of_issue = models.CharField(max_length=50, null=True, blank=True)
    date_of_expiration = models.CharField(max_length=50, null=True, blank=True)
    duplicate_passport= models.BooleanField(default=False)
    pages_passport= models.CharField(max_length=50, null=True, blank=True)
    photo = models.CharField(max_length=255, null=True, blank=True)
    organization = models.ForeignKey(Organizations,to_field='org_id', null=True, blank=True, on_delete=models.CASCADE)
    column1 = models.CharField(max_length=100, null=True, blank=True)
    column2 = models.CharField(max_length=100, null=True, blank=True)
    column3 = models.CharField(max_length=100, null=True, blank=True)
    column4 = models.CharField(max_length=100, null=True, blank=True)
    column5 = models.CharField(max_length=100, null=True, blank=True)
    column6 = models.CharField(max_length=100, null=True, blank=True)
    column7 = models.CharField(max_length=100, null=True, blank=True)
    column8 = models.CharField(max_length=100, null=True, blank=True)
    column9 = models.CharField(max_length=100, null=True, blank=True)
    column10 = models.CharField(max_length=100, null=True, blank=True)
    column11 = models.CharField(max_length=100, null=True, blank=True)
    column12 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Employee Passport Detail')
        verbose_name_plural = _('Employee Passport Detail')

    def __str__(self):
        return self.passport_number

    def __unicode__(self):
        return self.passport_number


#
#
class Employee_Visa_Detail(models.Model):
    emp_code = models.ForeignKey(Employee,to_field="emp_code",default="emp001",on_delete=models.CASCADE)
    country_code = models.CharField(max_length=100,null=True, blank=True)
    document_type = models.CharField(max_length=100,null=True, blank=True)
    document_title = models.CharField(max_length=100,null=True, blank=True)
    isdependent = models.BooleanField(default=False)
    relation = models.CharField(max_length=100,null=True, blank=True)
    document_number = models.CharField(max_length=100,null=True, blank=True)
    issue_date = models.CharField(max_length=100,null=True, blank=True)
    issue_place = models.CharField(max_length=100,null=True, blank=True)
    issuing_authority = models.CharField(max_length=100,null=True, blank=True)
    expiration_date = models.CharField(max_length=100,null=True, blank=True)
    is_validated = models.BooleanField(default=False)
    valid_from = models.CharField(max_length=100,null=True, blank=True)
    attachment_id = models.CharField(max_length=255, null=True, blank=True)
    organization = models.ForeignKey(Organizations,to_field='org_id', null=True, blank=True, on_delete=models.CASCADE)
    column1 = models.CharField(max_length=100, null=True, blank=True)
    column2 = models.CharField(max_length=100, null=True, blank=True)
    column3 = models.CharField(max_length=100, null=True, blank=True)
    column4 = models.CharField(max_length=100, null=True, blank=True)
    column5 = models.CharField(max_length=100, null=True, blank=True)
    column6 = models.CharField(max_length=100, null=True, blank=True)
    column7 = models.CharField(max_length=100, null=True, blank=True)
    column8 = models.CharField(max_length=100, null=True, blank=True)
    column9 = models.CharField(max_length=100, null=True, blank=True)
    column10 = models.CharField(max_length=100, null=True, blank=True)
    column11 = models.CharField(max_length=100, null=True, blank=True)
    column12 = models.CharField(max_length=100, null=True, blank=True)
    visa_entry_type = models.CharField(max_length=100, null=True, blank=True)


    class Meta:
        managed = True
        verbose_name = _('Employee Visa Detail')
        verbose_name_plural = _('Employee Visa Detail')

    def __str__(self):
        return self.emp_code

    def __unicode__(self):
        return self.emp_code


class Employee_Org_Info(models.Model):
    emp_code = models.ForeignKey(Employee,to_field="emp_code",default="emp001",on_delete=models.CASCADE)
    org1 = models.CharField(max_length=100,null=True, blank=True)
    org2 = models.CharField(max_length=100,null=True, blank=True)
    org3 = models.CharField(max_length=100,null=True, blank=True)
    org1ID = models.CharField(max_length=100,null=True, blank=True)
    org2ID = models.CharField(max_length=100,null=True, blank=True)
    org3ID = models.CharField(max_length=100,null=True, blank=True)

    home_office_location = models.CharField(max_length=100,null=True, blank=True)
    host_office_location = models.CharField(max_length=100,null=True, blank=True)
    client_office_location = models.CharField(max_length=100,null=True, blank=True)
    home_country_designation = models.CharField(max_length=100,null=True, blank=True)
    host_country_designation = models.CharField(max_length=100,null=True, blank=True)
    organization = models.ForeignKey(Organizations,to_field='org_id', null=True, blank=True, on_delete=models.CASCADE)
    column1 = models.CharField(max_length=100, null=True, blank=True)
    column2 = models.CharField(max_length=100, null=True, blank=True)
    column3 = models.CharField(max_length=100, null=True, blank=True)
    column4 = models.CharField(max_length=100, null=True, blank=True)
    column5 = models.CharField(max_length=100, null=True, blank=True)
    column6 = models.CharField(max_length=100, null=True, blank=True)
    column7 = models.CharField(max_length=100, null=True, blank=True)
    column8 = models.CharField(max_length=100, null=True, blank=True)
    column9 = models.CharField(max_length=100, null=True, blank=True)
    column10 = models.CharField(max_length=100, null=True, blank=True)
    column11 = models.CharField(max_length=100, null=True, blank=True)
    column12 = models.CharField(max_length=100, null=True, blank=True)
    current_working_country = models.CharField(max_length=100, null=True, blank=True)
    current_working_city = models.CharField(max_length=100, null=True, blank=True)
    home_country_band = models.CharField(max_length=100, null=True, blank=True)
    host_country_band = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Employee Visa Detail')
        verbose_name_plural = _('Employee Visa Detail')

    def __str__(self):
        return self.emp_code

    def __unicode__(self):
        return self.emp_code



class Calender_Events(TimeStampedModel, GeneratedByModel, Status):
    emp_code = models.ForeignKey(Employee,to_field="emp_code",default="emp001",on_delete=models.CASCADE)
    from_date = models.CharField(max_length=50,null=True, blank=True)
    to_date = models.CharField(max_length=50,null=True, blank=True)
    country_code = models.CharField(max_length=50,null=True, blank=True)
    country_name = models.CharField(max_length=100,null=True, blank=True)
    city_code = models.CharField(max_length=50,null=True, blank=True)
    city_name = models.CharField(max_length=100, null=True, blank=True)
    activity = models.CharField(max_length=100, null=True, blank=True)
    is_visible = models.CharField(max_length=50, default=True)
    is_deleted = models.CharField(max_length=50, default=False)
    column1 = models.CharField(max_length=100, null=True, blank=True)
    column2 = models.CharField(max_length=100, null=True, blank=True)
    column3 = models.CharField(max_length=100, null=True, blank=True)
    column4 = models.CharField(max_length=100, null=True, blank=True)
    column5 = models.CharField(max_length=100, null=True, blank=True)
    column6 = models.CharField(max_length=100, null=True, blank=True)
    column7 = models.CharField(max_length=100, null=True, blank=True)
    column8 = models.CharField(max_length=100, null=True, blank=True)
    column9 = models.CharField(max_length=100, null=True, blank=True)
    column10 = models.CharField(max_length=100, null=True, blank=True)
    column11 = models.CharField(max_length=100, null=True, blank=True)
    column12 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Calender Events')
        verbose_name_plural = _('Calender Events')

    def __str__(self):
        return self.emp_code

    def __unicode__(self):
        return self.emp_code


class Calender_Activity(models.Model):
    activity_name = models.CharField(max_length=100, null=True, blank=True)
    activity_sort_name = models.CharField(max_length=100, null=True, blank=True)
    is_visible = models.CharField(max_length=50, default=True)
    column1 = models.CharField(max_length=100, null=True, blank=True)
    column2 = models.CharField(max_length=100, null=True, blank=True)
    column3 = models.CharField(max_length=100, null=True, blank=True)
    column4 = models.CharField(max_length=100, null=True, blank=True)
    column5 = models.CharField(max_length=100, null=True, blank=True)
    column6 = models.CharField(max_length=100, null=True, blank=True)
    column7 = models.CharField(max_length=100, null=True, blank=True)
    column8 = models.CharField(max_length=100, null=True, blank=True)
    column9 = models.CharField(max_length=100, null=True, blank=True)
    column10 = models.CharField(max_length=100, null=True, blank=True)
    column11 = models.CharField(max_length=100, null=True, blank=True)
    column12 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Calender Activity')
        verbose_name_plural = _('Calender Activity')

    def __str__(self):
        return self.activity_name

    def __unicode__(self):
        return self.activity_name