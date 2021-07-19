from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from mobility_apps.superadmin.models import *
from mobility_apps.employee.models import Employee
from mobility_apps.base.models import TimeStampedModel, GeneratedByModel, Status


class Country(TimeStampedModel, GeneratedByModel, Status):
    country_code = models.CharField(max_length=10,default="231",unique=True)
    country_id = models.CharField(max_length=10, null=True, blank=True)
    country_name = models.CharField(max_length=100, null=True, blank=True)
    iso_code_duplet = models.CharField(max_length=100, null=True, blank=True)
    iso_code_triplet = models.CharField(max_length=100, null=True, blank=True)
    #organization  = models.ForeignKey('superadmin.Organizations',to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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

    class Meta:
        managed = True
        verbose_name = _('Country')
        verbose_name_plural = _('Country')

    def __str__(self):
        return self.country_name

    def __unicode__(self):
        return self.country_name


class Country_Policy(TimeStampedModel, GeneratedByModel, Status):
    country_id=models.CharField(max_length=100, null=True, blank=True)
    country_code = models.CharField(max_length=100, null=True, blank=True)
    country_name = models.CharField(max_length=100, null=True, blank=True)
    bv_threshold = models.CharField(max_length=100, null=True, blank=True)
    effective_date = models.CharField(max_length=100, null=True, blank=True)
    organization_id = models.ForeignKey(Organizations, to_field='org_id', null=True, blank=True, on_delete=models.CASCADE)
    home_country = models.CharField(max_length=100, null=True, blank=True)
    period = models.CharField(max_length=100, null=True, blank=True)
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
    # column11 = models.CharField(max_length=100, null=True, blank=True)
    # column12 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Country Policy')
        verbose_name_plural = _('Country Policy')

    def __str__(self):
        return self.country_name

    def __unicode__(self):
        return self.country_name

class Organization(TimeStampedModel, GeneratedByModel, Status):
    org_id = models.CharField(unique=True, max_length=20)
    org_name = models.CharField(max_length=100)
    org_info = models.CharField(max_length=200)
    org_ho_address = models.CharField(max_length=200)
    org_ho_phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100,default="231", blank=True)
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
        verbose_name = _('Organization')
        verbose_name_plural = _('Organization')

    def __str__(self):
        return self.org_name

    def __unicode__(self):
        return self.org_name


class Project(TimeStampedModel, GeneratedByModel):
    pid = models.CharField(max_length=50, unique=True)
    pid_disp = models.CharField(max_length=100, null=True, blank=True)
    project_name = models.CharField(max_length=100, blank=True)
    start_date = models.CharField(max_length=100, null=True, blank=True)
    End_Date = models.CharField(max_length=100, null=True, blank=True)  # plus the time for last date
    expense_approver= models.CharField(max_length=100, null=True, blank=True)
    project_manager = models.CharField(max_length=100, null=True, blank=True)
    business_lead = models.CharField(max_length=100, null=True, blank=True)
    client_executive_lead = models.CharField(max_length=100, null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Project')
        verbose_name_plural = _('Project')
        unique_together = ('pid_disp','organization')

    def __str__(self):
        return self.project_name


class Visa_Purpose(TimeStampedModel, GeneratedByModel, Status):
    VPID = models.CharField(max_length=50)
    country = models.CharField(max_length=100,default="231",blank=True)
    purpose_name = models.CharField(max_length=100)
    applicable_visa = models.CharField(max_length=15)
    organization  = models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = _('Visa Purpose')
        verbose_name_plural = _('Visa Purpose')
        unique_together = ('VPID','organization')

    def __str__(self):
        return self.VPID

    def __unicode__(self):
        return self.VPID
        


#
#
class Visa(TimeStampedModel, GeneratedByModel, Status):
    visa_id = models.CharField(max_length=100, unique=True)
    visa_name = models.CharField(max_length=100, null=True, blank=True)
    visa_type = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=100,default="231", blank=True)
    country_name = models.CharField(max_length=100, null=True, blank=True)
    visa_info = models.CharField(max_length=255, null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Visa')
        verbose_name_plural = _('Visa')

    def __str__(self):
        return self.visa_id

    def __unicode__(self):
        return self.visa_id


class Visa_Document_Checklist(TimeStampedModel, GeneratedByModel, Status):
    visa = models.ForeignKey(Visa, to_field="visa_id", null=True, blank=True, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, null=True,blank=True)
    country = models.CharField(max_length=100,default="231", blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Visa Document Checklist')
        verbose_name_plural = _('Visa Document Checklist')

    def __str__(self):
        return self.document_name

    def __unicode__(self):
        return self.document_name


class Assignment_Type(TimeStampedModel, GeneratedByModel, Status):
    assgment_type_id = models.CharField(unique=True, max_length=4)
    assigment_type_name = models.CharField(max_length=30)
    applicable_days = models.IntegerField()
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Assignment Type')
        verbose_name_plural = _('Assignment Type')

    def __str__(self):
        return self.assgment_type_id

    def __unicode__(self):
        return self.assgment_type_id


class Department(TimeStampedModel, GeneratedByModel, Status):
    department_id = models.CharField(unique=True, max_length=4)
    department_name = models.CharField(max_length=100)
    department_description = models.CharField(max_length=200)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Department')
        verbose_name_plural = _('Department')

    def __str__(self):
        return self.department_name

    def __unicode__(self):
        return self.department_name


class Organization_Location(TimeStampedModel, GeneratedByModel, Status):
    location_id = models.CharField(unique=True, max_length=4)
    location_name = models.CharField(max_length=100)
    lcoation_address = models.CharField(max_length=200)
    location_phone = models.CharField(max_length=20)
    country =models.CharField(max_length=100,default="231", blank=True)
    organization = models.ForeignKey(Organization, related_name="organization_locations", null=True, blank=True,
                                     on_delete=models.CASCADE)
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
        verbose_name = _('Organization Location')
        verbose_name_plural = _('Organization Location')

    def __str__(self):
        return self.location_name

    def __unicode__(self):
        return self.location_name


class Vendor(TimeStampedModel, GeneratedByModel, Status):
    vendor_id = models.CharField(unique=True, max_length=100)
    vendor_name = models.CharField(max_length=100, blank=True)
    vendor_type = models.CharField(max_length=200, blank=True)
    vendor_phone = models.CharField(max_length=20, blank=True)
    vendor_contact_person = models.CharField(max_length=100)
    country = models.CharField(max_length=100,default="231", blank=True)
    vendor_address = models.CharField(max_length=100, blank=True)
    vendor_details = models.CharField(max_length=100, blank=True)
    endDate = models.CharField(max_length=100,blank=True)
    vendor_email = models.CharField(max_length=100,blank=True)
    startDate = models.CharField(max_length=100, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = _('Vendor')
        verbose_name_plural = _('Vendor')
        unique_together = ('vendor_email','organization')

    def __str__(self):
        return self.vendor_name

    def __unicode__(self):
        return self.vendor_name


class Vendor_Category(TimeStampedModel, GeneratedByModel, Status):
    vendor_id = models.CharField(max_length=100, blank=True)
    vendor_name = models.CharField(max_length=100, blank=True)
    category_id = models.IntegerField(max_length=200, blank=True)
    category_name = models.CharField(max_length=200, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = _('Vendor Category')
        verbose_name_plural = _('Vendor Category')

    def __str__(self):
        return self.vendor_name

    def __unicode__(self):
        return self.vendor_name


class Vendor_Master(TimeStampedModel, GeneratedByModel, Status):
    vendor_id = models.IntegerField(max_length=100)
    vendor_type = models.CharField(max_length=100, blank=True)
    action=models.CharField(max_length=100, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = _('Vendor Master')
        verbose_name_plural = _('Vendor Master')
        unique_together = ('vendor_type','organization')

    def __str__(self):
        return self.vendor_id

    def __unicode__(self):
        return self.vendor_id


class Role(TimeStampedModel, GeneratedByModel, Status):
    role_id = models.CharField(unique=True, max_length=4)
    role_name = models.CharField(max_length=100, blank=True, )
    role_description = models.CharField(max_length=200, blank=True, )
    organization = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    def __str__(self):
        return self.role_name

    def __unicode__(self):
        return self.role_name


class Request_Status(TimeStampedModel, GeneratedByModel, Status):
    status_id = models.CharField(unique=True, blank=True, max_length=4)
    status = models.CharField(unique=True, max_length=20)
    request_type = models.CharField(max_length=10, blank=True, )
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Request Status')
        verbose_name_plural = _('Request Status')

    def __str__(self):
        return self.status_id

    def __unicode__(self):
        return self.status_id


class Activity_Log(TimeStampedModel, GeneratedByModel, Status):
    action = models.CharField(max_length=200, blank=True)
    action_type = models.CharField(max_length=50, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Activity Log')
        verbose_name_plural = _('Activity Log')

    def __str__(self):
        return self.action

    def __unicode__(self):
        return self.action


class Assignment_Group(TimeStampedModel, GeneratedByModel, Status):
    emp_email= models.ForeignKey(Employee,to_field="emp_code", default="Emp002",related_name="Employee", null=True, blank=True,
                                 on_delete=models.CASCADE)
    emp_code = models.CharField(max_length=100, null=True, blank=True)
    emp_name = models.CharField(max_length=100, null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Assignment Group')
        verbose_name_plural = _('Assignment Group')

    def __str__(self):
        return self.emp_name

    def __unicode__(self):
        return self.emp_name

class Currency_Conversion(TimeStampedModel, GeneratedByModel, Status):
    from_currency= models.CharField(max_length=10, null=True,blank=True)
    to_currency = models.CharField(max_length=100,null=True, blank=True)
    conversion_date=  models.DateTimeField(max_length=10,null=True, blank=True)
    conversion_rate = models.CharField(max_length=200, null=True, blank=True)
    status_code = models.CharField(max_length=200,null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Currency Conversion')
        verbose_name_plural = _('Currency Conversion')

    def __str__(self):
        return self.from_currency

    def __unicode__(self):
        return self.from_currency


class Currency_Conversion_History(TimeStampedModel, GeneratedByModel, Status):
    from_currency= models.CharField(max_length=10, null=True,blank=True)
    to_currency = models.CharField(max_length=100,null=True, blank=True)
    conversion_date=  models.DateTimeField(max_length=10,null=True, blank=True)
    conversion_rate = models.CharField(max_length=200, null=True, blank=True)
    status_code = models.CharField(max_length=200,null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Currency Conversion')
        verbose_name_plural = _('Currency Conversion')

    def __str__(self):
        return self.from_currency

    def __unicode__(self):
        return self.from_currency

class Currency(TimeStampedModel, GeneratedByModel, Status):
    currency_code = models.CharField(max_length=4,unique=True)
    currency_name = models.CharField(max_length=100, blank=True)
    currency_description = models.CharField(max_length=200, blank=True)
    status_type = models.CharField(max_length=200, blank=True)
    organization = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Currency')
        verbose_name_plural = _('Currency')
        # unique_together = ('currency_code','organization')

    def __str__(self):
        return self.currency_name

    def __unicode__(self):
        return self.currency_name

class Approval_Hierarchy(TimeStampedModel, GeneratedByModel, Status):
    request_id= models.CharField(max_length=100, null=True, blank=True)
    approver= models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Approval Hierarchy')
        verbose_name_plural = _('Approval Hierarchy')

    def __str__(self):
        return self.approver

    def __unicode__(self):
        return self.approver




class City(TimeStampedModel, GeneratedByModel, Status):
    airport_id = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    airport_name = models.CharField(max_length=100, null=True, blank=True)
    iata_code = models.CharField(max_length=100, null=True, blank=True)
    icao_code = models.CharField(max_length=100, null=True, blank=True)
    #organization  = models.ForeignKey('superadmin.Organizations',to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
    country = models.CharField(max_length=100,default="231", null=True, blank=True)
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
        verbose_name = _('City')
        verbose_name_plural = _('City')

    def __str__(self):
        return self.city

    def __unicode__(self):
        return self.city


class Per_Diem(TimeStampedModel, GeneratedByModel, Status):
    country = models.CharField(max_length=100,default="231", null=True, blank=True)
    currency = models.CharField(max_length=100, null=True, blank=True)
    currency_code = models.CharField(max_length=100, null=True, blank=True)
    per_diem = models.CharField(max_length=100, null=True, blank=True)
    accommodation_limit = models.CharField(max_length=100, null=True, blank=True)
    transportation = models.CharField(max_length=100, null=True, blank=True)
    other = models.CharField(max_length=100, null=True, blank=True)
    effective_date = models.CharField(max_length=100, null=True, blank=True)
    organization = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
    band = models.CharField(max_length=100, null=True, blank=True)
    home_country = models.CharField(max_length=100, null=True, blank=True)
    column1 = models.CharField(max_length=100, null=True, blank=True)
    column2 = models.CharField(max_length=100, null=True, blank=True)
    column3 = models.CharField(max_length=100, null=True, blank=True)
    column4= models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = _('Per Diem')
        verbose_name_plural = _('Per Diem')

    def __str__(self):
        return self.country

    def __unicode__(self):
        return self.country


class Assignment_Status(TimeStampedModel, GeneratedByModel, Status):
    request = models.CharField(max_length=100, null=True, blank=True)
    request_status = models.CharField(max_length=100, null=True, blank=True)
    status_type=models.CharField(max_length=100, null=True, blank=True)
    vendor_fees = models.CharField(max_length=100, null=True, blank=True)
    govt_fees = models.CharField(max_length=100, null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
    column1 = models.CharField(max_length=100, null=True, blank=True)
    column2 = models.CharField(max_length=100, null=True, blank=True)
    column3 = models.CharField(max_length=100, null=True, blank=True)
    column4= models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = _('Assignment Status')
        verbose_name_plural = _('Assignment Status')

    def __str__(self):
        return self.status_type

    def __unicode__(self):
        return self.status_type

class Request_Approvals(TimeStampedModel, GeneratedByModel, Status):
    request_id = models.CharField(max_length=100, null=True, blank=True)
    request_type = models.CharField(max_length=100, null=True, blank=True)
    action_status=models.CharField(max_length=100, null=True, blank=True)
    action_taken = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    order = models.CharField(max_length=100, null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
    column1 = models.CharField(max_length=100, null=True, blank=True)
    column2 = models.CharField(max_length=100, null=True, blank=True)
    column3 = models.CharField(max_length=100, null=True, blank=True)
    column4= models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = _('Request Approvals')
        verbose_name_plural = _('Request Approvals')

    def __str__(self):
        return self.action_taken

    def __unicode__(self):
        return self.action_taken

class Dial_Code(TimeStampedModel, GeneratedByModel, Status):
    name = models.CharField(max_length=100, null=True, blank=True)
    dial_code = models.CharField(max_length=100, null=True, blank=True)
    code=models.CharField(max_length=100, null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
    class Meta:
        managed = True
        verbose_name = _('Dial Code')
        verbose_name_plural = _('Dial Code')

    def __str__(self):
        return self.dial_code

    def __unicode__(self):
        return self.dial_code

class Country_Master(TimeStampedModel, GeneratedByModel, Status):
    country_id= models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    sortname = models.CharField(max_length=100, null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
    class Meta:
        managed = True
        verbose_name = _('Country Master')
        verbose_name_plural = _('Country Master')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class State_Master(TimeStampedModel, GeneratedByModel, Status):
    state_id= models.CharField(max_length=100, null=True, blank=True)
    country_id= models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
    class Meta:
        managed = True
        verbose_name = _('State Master')
        verbose_name_plural = _('State Master')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Location_Master(TimeStampedModel, GeneratedByModel, Status):
    location_code= models.CharField(max_length=100,null=True, blank=True)
    location_name= models.CharField(max_length=100,null=True, blank=True)
    description= models.CharField(max_length=500,null=True, blank=True)
    status = models.CharField(max_length=100,null=True, blank=True)
    group= models.CharField(max_length=100,null=True, blank=True)
    timezone= models.CharField(max_length=100,null=True, blank=True)
    effective_start_date= models.CharField(max_length=100,null=True, blank=True)
    effective_end_date= models.CharField(max_length=100,null=True, blank=True)
    address_line_1= models.CharField(max_length=100,null=True, blank=True)
    address_line_1= models.CharField(max_length=100,null=True, blank=True)
    address_line_1= models.CharField(max_length=100,null=True, blank=True)
    city= models.CharField(max_length=100,null=True, blank=True)
    county= models.CharField(max_length=100,null=True, blank=True)
    state= models.CharField(max_length=100,null=True, blank=True)
    zip= models.CharField(max_length=100,null=True, blank=True)
    country= models.CharField(max_length=100,null=True, blank=True)
    primary_phone= models.CharField(max_length=100,null=True, blank=True)
    secondary_phone= models.CharField(max_length=100,null=True, blank=True)
    fax= models.CharField(max_length=100,null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Location Master')
        verbose_name_plural = _('Location Master')

    def __str__(self):
        return self.location_code

    def __unicode__(self):
        return self.location_code



class Taxgrid_Master(TimeStampedModel, GeneratedByModel, Status):
    tax_label= models.CharField(max_length=100,null=True, blank=True)
    group_by= models.CharField(max_length=100,null=True, blank=True)
    organization  = models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = _('Taxgrid Master')
        verbose_name_plural = _('Taxgrid Master')

    def __str__(self):
        return self.tax_label

    def __unicode__(self):
        return self.tax_label


class Taxgrid(TimeStampedModel, GeneratedByModel, Status):
    tax_label= models.CharField(max_length=100,null=True, blank=True)
    tax_country= models.CharField(max_length=100,null=True, blank=True)
    group_by= models.CharField(max_length=100,null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = _('Taxgrid Country')
        verbose_name_plural = _('Taxgrid Country')

    def __str__(self):
        return self.tax_label

    def __unicode__(self):
        return self.tax_label


class Taxgrid_Country(TimeStampedModel, GeneratedByModel, Status):
    tax_country= models.CharField(unique=True,max_length=500,null=True, blank=True)
    organization  = models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = _('Taxgrid Country')
        verbose_name_plural = _('Taxgrid Country')

    def __str__(self):
        return self.tax_country

    def __unicode__(self):
        return self.tax_country


class Gender(TimeStampedModel, GeneratedByModel, Status):
    code= models.CharField(max_length=100,null=True, blank=True)
    description= models.CharField(max_length=100,null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Gender')
        verbose_name_plural = _('Gender')

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code


class Marital_Status(TimeStampedModel, GeneratedByModel, Status):
    code= models.CharField(max_length=100,null=True, blank=True)
    description= models.CharField(max_length=100,null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Marital Status')
        verbose_name_plural = _('Marital Status')

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code


class Salutation(TimeStampedModel, GeneratedByModel, Status):
    code= models.CharField(max_length=100,null=True, blank=True)
    description= models.CharField(max_length=100,null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Salutation')
        verbose_name_plural = _('Salutation')

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code



class Acedmic_Title(TimeStampedModel, GeneratedByModel, Status):
    code= models.CharField(max_length=100,null=True, blank=True)
    description= models.CharField(max_length=100,null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Acedmic Title')
        verbose_name_plural = _('Acedmic Title')

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code


class Name_Suffix(TimeStampedModel, GeneratedByModel, Status):
    code= models.CharField(max_length=100,null=True, blank=True)
    description= models.CharField(max_length=100,null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Name Suffix')
        verbose_name_plural = _('Name Suffix')

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code


class Email_Type(TimeStampedModel, GeneratedByModel, Status):
    code= models.CharField(max_length=100,null=True, blank=True)
    description= models.CharField(max_length=100,null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Email Type')
        verbose_name_plural = _('Email Type')

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code


class Phone_Type(TimeStampedModel, GeneratedByModel, Status):
    code= models.CharField(max_length=100,null=True, blank=True)
    description= models.CharField(max_length=100,null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Phone Type')
        verbose_name_plural = _('Phone Type')

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code

class Relation(TimeStampedModel, GeneratedByModel, Status):
    code= models.CharField(max_length=100,null=True, blank=True)
    description= models.CharField(max_length=100,null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Relation')
        verbose_name_plural = _('Relation')

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code


class Termination_Reasons(TimeStampedModel, GeneratedByModel, Status):
    code= models.CharField(max_length=100,null=True, blank=True)
    description= models.CharField(max_length=100,null=True, blank=True)
    organization  = models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = _('Termination Reasons')
        verbose_name_plural = _('Termination Reasons')

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code



class Address_Type(TimeStampedModel, GeneratedByModel, Status):
    code= models.CharField(max_length=100,null=True, blank=True)
    description= models.CharField(max_length=100,null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Address Type')
        verbose_name_plural = _('Address Type')

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code


class Language(TimeStampedModel, GeneratedByModel, Status):
    code= models.CharField(max_length=100,null=True, blank=True)
    description= models.CharField(max_length=100,null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Language')
        verbose_name_plural = _('Language')

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code

class Ticket_Status_Master(TimeStampedModel, GeneratedByModel, Status):
    name= models.CharField(max_length=100,null=True, blank=True)
    value= models.CharField(max_length=100,null=True, blank=True)
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
        verbose_name = _('Ticket Status Master')
        verbose_name_plural = _('Ticket Status Master')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Status_Master(TimeStampedModel, GeneratedByModel, Status):
    name= models.CharField(max_length=100,null=True, blank=True)
    value= models.CharField(max_length=100,null=True, blank=True)
    module= models.CharField(max_length=100,null=True, blank=True)
    action= models.CharField(max_length=100,null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Action Status Master')
        verbose_name_plural = _('Action Status Master')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
		
		
class Visa_Master(TimeStampedModel, GeneratedByModel, Status):
    document_name= models.CharField(max_length=100,null=True, blank=True)
    document_type= models.CharField(max_length=100,null=True, blank=True)
    parent_id= models.CharField(max_length=100,null=True, blank=True)
    visa_type= models.CharField(max_length=100,null=True, blank=True)
    host_type= models.CharField(max_length=100,null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = _('Visa Master')
        verbose_name_plural = _('Visa Master')

    def __str__(self):
        return self.document_name

    def __unicode__(self):
        return self.document_name



class Visa_Master_Applicable(TimeStampedModel, GeneratedByModel, Status):
    document_id= models.CharField(max_length=100,null=True, blank=True)
    parent_id= models.CharField(max_length=100,null=True, blank=True)
    applicable_country= models.CharField(max_length=2000,null=True, blank=True)
    visa_type= models.CharField(max_length=2000,null=True, blank=True)
    document_type= models.CharField(max_length=100,null=True, blank=True)
    host_type= models.CharField(max_length=100,null=True, blank=True)
    organization = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Visa Master Applicable')
        verbose_name_plural = _('Visa Master Applicable')

    def __str__(self):
        return self.document_id

    def __unicode__(self):
        return self.document_id
		
class National_Id(TimeStampedModel, GeneratedByModel, Status):
    Id_Name= models.CharField(max_length=100,null=True, blank=True)
    Id_Name2= models.CharField(max_length=100,null=True, blank=True)
    country= models.CharField(max_length=100,null=True, blank=True)
    organization = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('National Id')
        verbose_name_plural = _('National Id')

    def __str__(self):
        return self.country

    def __unicode__(self):
        return self.country
		
class Notification(TimeStampedModel, GeneratedByModel, Status):
    Notification_ID= models.CharField(unique=True, max_length=20)
    Message= models.CharField(max_length=200,null=True, blank=True)
    Entity_Type= models.CharField(max_length=100,null=True, blank=True)
    Entity_ID= models.CharField(max_length=100,null=True, blank=True)
    Notification_Date= models.CharField(max_length=100,null=True, blank=True)
    Action_taken_by= models.CharField(max_length=100,null=True, blank=True)
    organization = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
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
        verbose_name = _('Notification')
        verbose_name_plural = _('Notification')

    def __str__(self):
        return self.Notification_ID

    def __unicode__(self):
        return self.Notification_ID
		
class Create_Assignment(TimeStampedModel, GeneratedByModel, Status):
    Assignment_ID=models.CharField(unique=True, max_length=20)
    Ticket_ID = models.CharField(max_length=100, null=True, blank=True)
    Employee_ID = models.CharField(max_length=100, null=True, blank=True)
    Entity_Type = models.CharField(max_length=100, null=True, blank=True)
    Tentative_Assignment_Start_Date = models.CharField(max_length=100, null=True, blank=True)
    Tentative_Assignment_End_Date = models.CharField(max_length=100, null=True, blank=True)
    Actual_Start_Date = models.CharField(max_length=100, null=True, blank=True)
    Actual_End_Date = models.CharField(max_length=100, null=True, blank=True)
    Assignment_Extended_to = models.CharField(max_length=100, null=True, blank=True)
    Family_Size = models.CharField(max_length=100, null=True, blank=True)
    Assignment_Type = models.CharField(max_length=100, null=True, blank=True)
    Payroll_Type = models.CharField(max_length=100, null=True, blank=True)
    Home_Country= models.CharField(max_length=100, null=True, blank=True)
    Host_Country = models.CharField(max_length=100, null=True, blank=True)
    Host_State = models.CharField(max_length=100, null=True, blank=True)
    Host_City = models.CharField(max_length=100, null=True, blank=True)
    Tax_Equalization = models.CharField(max_length=100, null=True, blank=True)
    Accommodation_Type = models.CharField(max_length=100, null=True, blank=True)
    Add_Assignment_Attachment =models.CharField(max_length=100, null=True, blank=True)
    visa_details =models.CharField(max_length=100, null=True, blank=True)
    home_compensation =models.CharField(max_length=100, null=True, blank=True)
    host_compensation =models.CharField(max_length=100, null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = _('Create Assignment')
        verbose_name_plural = _('Create Assignment')

    def __str__(self):
        return self.Assignment_ID

    def __unicode__(self):
        return self.Assignment_ID


class Secondory_Assignment(TimeStampedModel, GeneratedByModel, Status):
    Secondory_Assignment_ID=models.CharField(unique=True, max_length=20)
    Assignment_ID=models.CharField(max_length=100, null=True, blank=True)
    Ticket_ID = models.CharField(max_length=100, null=True, blank=True)
    Employee_ID = models.CharField(max_length=100, null=True, blank=True)
    Entity_Type = models.CharField(max_length=100, null=True, blank=True)
    Tentative_Assignment_Start_Date = models.CharField(max_length=100, null=True, blank=True)
    Tentative_Assignment_End_Date = models.CharField(max_length=100, null=True, blank=True)
    Actual_Start_Date = models.CharField(max_length=100, null=True, blank=True)
    Actual_End_Date = models.CharField(max_length=100, null=True, blank=True)
    Assignment_Extended_to = models.CharField(max_length=100, null=True, blank=True)
    Family_Size = models.CharField(max_length=100, null=True, blank=True)
    Assignment_Type = models.CharField(max_length=100, null=True, blank=True)
    Payroll_Type = models.CharField(max_length=100, null=True, blank=True)
    Home_Country= models.CharField(max_length=100, null=True, blank=True)
    Host_Country = models.CharField(max_length=100, null=True, blank=True)
    Host_State = models.CharField(max_length=100, null=True, blank=True)
    Host_City = models.CharField(max_length=100, null=True, blank=True)
    Tax_Equalization = models.CharField(max_length=100, null=True, blank=True)
    Accommodation_Type = models.CharField(max_length=100, null=True, blank=True)
    Add_Assignment_Attachment =models.CharField(max_length=100, null=True, blank=True)
    visa_details =models.CharField(max_length=100, null=True, blank=True)
    home_compensation =models.CharField(max_length=100, null=True, blank=True)
    host_compensation =models.CharField(max_length=100, null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = _('Secondory Assignment')
        verbose_name_plural = _('Secondory Assignment')

    def __str__(self):
        return self.Assignment_ID

    def __unicode__(self):
        return self.Assignment_ID


class Assignment_Extension(TimeStampedModel, GeneratedByModel, Status):
    Extension_Assignment_ID=models.CharField(unique=True, max_length=20)
    Assignment_ID=models.CharField(max_length=100, null=True, blank=True)
    Ticket_ID = models.CharField(max_length=100, null=True, blank=True)
    Employee_ID = models.CharField(max_length=100, null=True, blank=True)
    Entity_Type = models.CharField(max_length=100, null=True, blank=True)
    Tentative_Assignment_Start_Date = models.CharField(max_length=100, null=True, blank=True)
    Tentative_Assignment_End_Date = models.CharField(max_length=100, null=True, blank=True)
    Actual_Start_Date = models.CharField(max_length=100, null=True, blank=True)
    Actual_End_Date = models.CharField(max_length=100, null=True, blank=True)
    Assignment_Extended_to = models.CharField(max_length=100, null=True, blank=True)
    Family_Size = models.CharField(max_length=100, null=True, blank=True)
    Assignment_Type = models.CharField(max_length=100, null=True, blank=True)
    Payroll_Type = models.CharField(max_length=100, null=True, blank=True)
    Home_Country= models.CharField(max_length=100, null=True, blank=True)
    Host_Country = models.CharField(max_length=100, null=True, blank=True)
    Host_State = models.CharField(max_length=100, null=True, blank=True)
    Host_City = models.CharField(max_length=100, null=True, blank=True)
    Tax_Equalization = models.CharField(max_length=100, null=True, blank=True)
    Accommodation_Type = models.CharField(max_length=100, null=True, blank=True)
    Add_Assignment_Attachment =models.FileField(upload_to='visaimage/', null=True, blank=True,max_length=255)
    visa_details =models.CharField(max_length=100, null=True, blank=True)
    home_compensation =models.CharField(max_length=100, null=True, blank=True)
    host_compensation =models.CharField(max_length=100, null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = _('Assignment Extension')
        verbose_name_plural = _('Assignment Extension')

    def __str__(self):
        return self.Assignment_ID

    def __unicode__(self):
        return self.Assignment_ID


class Designation(TimeStampedModel, GeneratedByModel, Status):
    name= models.CharField(max_length=100,null=True, blank=True)
    code= models.CharField(max_length=100,null=True, blank=True)
    organization = models.CharField(max_length=100,null=True, blank=True)
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
        verbose_name = _('Designation')
        verbose_name_plural = _('Designation')

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code
from mobility_apps.travel.models import Travel_Request 
TYPE_CHOICES = (('Tax Payer','Tax Payer'),('Spouse','Spouse'),('Joint','Joint'))

class Vendor_Income(TimeStampedModel, GeneratedByModel, Status):
    income_type = models.CharField(max_length=100,null=True, blank=True)
    amount = models.CharField(max_length=100, null=True,blank=True)
    owner = models.CharField(max_length=100, choices=TYPE_CHOICES,null=True,blank=True)
    attachment = models.CharField(max_length=300, null=True,blank=True)
    tax_year = models.CharField(max_length=100, null=True,blank=True)
    vendor = models.ForeignKey(Vendor,null=True, blank=True,on_delete=models.CASCADE)
    organization = models.ForeignKey(Organizations,null=True, blank=True,on_delete=models.CASCADE)
    travel_req = models.ForeignKey(Travel_Request,null=True, blank=True,  on_delete=models.CASCADE)
    employee= models.ForeignKey(Employee,null=True, blank=True, on_delete=models.CASCADE) 
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
        verbose_name = _('income_type')
        verbose_name_plural = _('income_type')


class Employee_Address_Vendor(TimeStampedModel, GeneratedByModel, Status):
    pickup_address = models.TextField(null=True, blank=True)
    delivery_address = models.TextField(null=True,blank=True)
    move_date  = models.CharField(max_length=100, null=True,blank=True)
    delivery_date  = models.CharField(max_length=100, null=True,blank=True)
    vendor = models.ForeignKey(Vendor,null=True, blank=True,on_delete=models.CASCADE)
    organization = models.ForeignKey(Organizations,null=True, blank=True,on_delete=models.CASCADE,related_name="organization")
    employee= models.ForeignKey(Employee,related_name="Employee_name", null=True, blank=True,on_delete=models.CASCADE)
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

class Capital_Gains_Income(TimeStampedModel, GeneratedByModel, Status):
    company_name = models.CharField(max_length=200,null=True, blank=True)
    class_of_share = models.CharField(max_length=100, null=True,blank=True)
    share_sold = models.CharField(max_length=100, choices=TYPE_CHOICES,null=True,blank=True)
    date_purchased = models.CharField(max_length=100, null=True,blank=True)
    date_sold = models.CharField(max_length=100, null=True,blank=True)
    purchase_price = models.CharField(max_length=100, null=True,blank=True)
    sale_price = models.CharField(max_length=100, null=True,blank=True)
    sale_expenses = models.CharField(max_length=100, null=True,blank=True)
    tex_paid = models.CharField(max_length=100, null=True,blank=True)
    currency = models.ForeignKey(Currency,null=True, blank=True,on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor,null=True, blank=True,on_delete=models.CASCADE)
    organization = models.ForeignKey(Organizations,null=True, blank=True,on_delete=models.CASCADE)
    travel_req = models.ForeignKey(Travel_Request,null=True, blank=True,  on_delete=models.CASCADE)
    employee= models.ForeignKey(Employee,null=True, blank=True, on_delete=models.CASCADE)
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
        verbose_name = _('company_name')
        verbose_name_plural = _('company_name')


class Vendor_Status(TimeStampedModel, GeneratedByModel, Status):
    status = models.CharField(max_length=200,null=True, blank=True)
    selecting_status = models.CharField(max_length=200, null=True,blank=True)
    histry = models.TextField(null=True,blank=True)
    vendor = models.ForeignKey(Vendor,null=True, blank=True,on_delete=models.CASCADE)
    organization = models.ForeignKey(Organizations,null=True, blank=True,on_delete=models.CASCADE)
    # travel_req = models.ForeignKey(Travel_Request,null=True, blank=True,  on_delete=models.CASCADE)
    employee= models.ForeignKey(Employee,null=True, blank=True, on_delete=models.CASCADE) 
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
        verbose_name = _('status')
        verbose_name_plural = _('status')


class vendor_Service_List(TimeStampedModel, GeneratedByModel, Status):
    services_list = models.CharField(max_length=200,null=True, blank=True)
    status_audit_history = models.CharField(max_length=200, null=True,blank=True)
    histry = models.TextField(null=True,blank=True)
    date = models.CharField(max_length=100,null=True, blank=True)
    estimated_visa_approve_date=models.CharField(max_length=100,null=True, blank=True)
    vendor = models.ForeignKey(Vendor,null=True, blank=True,on_delete=models.CASCADE)
    vendor_status = models.ForeignKey(Vendor_Status,null=True, blank=True,on_delete=models.CASCADE)
    organization = models.ForeignKey(Organizations,null=True, blank=True,on_delete=models.CASCADE)
    # travel_req = models.ForeignKey(Travel_Request,null=True, blank=True,  on_delete=models.CASCADE)
    employee= models.ForeignKey(Employee,null=True, blank=True, on_delete=models.CASCADE) 
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




class vendor_Service_List_status(TimeStampedModel, GeneratedByModel, Status):
    status_name = models.CharField(max_length=200,null=True, blank=True)
    date_status = models.CharField(max_length=200, null=True,blank=True)
    organization = models.ForeignKey(Organizations,null=True, blank=True,on_delete=models.CASCADE)
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


class Vaccine_Master(TimeStampedModel, GeneratedByModel, Status):
    vaccine_name = models.CharField(max_length=200,null=True, blank=True)
    vaccine_company_name = models.CharField(max_length=200, null=True,blank=True)

    class Meta:
        managed = True
        verbose_name = _('Vaccine Master')
        verbose_name_plural = _('Vaccine Master')



class Vaccine_Autho_Country(TimeStampedModel, GeneratedByModel, Status):
    vaccine_master = models.ForeignKey(Vaccine_Master, null=True, blank=True, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organizations,to_field='org_id', null=True, blank=True, on_delete=models.CASCADE)
    country_id = models.CharField(max_length=10,null=True, blank=True)
    authorization_type = models.BooleanField(default=False)
    access_type = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Vaccine Autho Country')
        verbose_name_plural = _('Vaccine Autho Country')

