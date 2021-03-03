from django.db import models
# Create your models here.
from mobility_apps.base.models import TimeStampedModel, GeneratedByModel, Status
# from mobility_apps.employee.models import Country
#from mobility_apps.master.models import Project, Organization
from django.utils.translation import ugettext_lazy as _

class Organizations(TimeStampedModel, GeneratedByModel, Status):
    org_id = models.CharField(max_length=100,null=True,blank=True,unique=True)
    org_name = models.CharField(max_length=100,null=True,blank=True)
    year_founded= models.IntegerField(max_length=4,blank=True, null=True)
    org_type = models.CharField(max_length=50, null=True, blank=True)
    HQ_add = models.TextField( null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    fax = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    org_info = models.TextField( null=True, blank=True)
    web_url =models.CharField(max_length=250, null=True, blank=True)
    pan_no = models.CharField(max_length=50, null=True, blank=True)
    tan_no = models.CharField(max_length=50, null=True, blank=True)
    contact_person_name = models.CharField(max_length=250, null=True, blank=True)
    contact_person_email = models.CharField(max_length=250, null=True, blank=True)
    contact_person_phone = models.CharField(max_length=250, null=True, blank=True)
    org_pass = models.CharField(max_length=250, null=True, blank=True)
    start_date = models.DateField(max_length=50, null=True, blank=True)
    end_date = models.DateField(max_length=50, null=True, blank=True) 



    ## Compulsory fields #
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
    column13 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Organization')
        verbose_name_plural = _('Organizations')


class Organization_branches(TimeStampedModel, GeneratedByModel, Status):
    org_id_id = models.CharField(max_length=100, null=True, blank=True)
    org_name = models.CharField(max_length=100,null=True,blank=True)
    address = models.TextField(blank=True, null=True, )
    country = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    fax = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    gst_no = models.CharField(max_length=50, null=True, blank=True)
    contact_person_name = models.CharField(max_length=250, null=True, blank=True)
    contact_person_email = models.CharField(max_length=250, null=True, blank=True)
    contact_person_phone = models.CharField(max_length=250, null=True, blank=True)

    ## Compulsory fields #
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
    column13 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Organization Branch')
        verbose_name_plural = _('Organizations Branch')

class Sub_Organization_branches(TimeStampedModel, GeneratedByModel, Status):
    org_id_id = models.CharField(max_length=100, null=True, blank=True)
    org_name = models.CharField(max_length=100,null=True,blank=True)
    branch_id= models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(blank=True, null=True, )
    country = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    fax = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    gst_no = models.CharField(max_length=50, null=True, blank=True)
    contact_person_name = models.CharField(max_length=250, null=True, blank=True)
    contact_person_email = models.CharField(max_length=250, null=True, blank=True)
    contact_person_phone = models.CharField(max_length=250, null=True, blank=True)

    ## Compulsory fields #
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
    column13 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Organization Branch')
        verbose_name_plural = _('Organizations Branch')
 
class Organization_users(TimeStampedModel, GeneratedByModel, Status):
    org_id_id = models.IntegerField(max_length=100, null=True, blank=True)
    org_id = models.CharField(max_length=100, null=False, blank=False)
    user_type = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=250, null=True, blank=True)
    password = models.CharField(max_length=250, null=True, blank=True)

    ## Compulsory fields #
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
    column13 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Organization User')
        verbose_name_plural = _('Organizations User')
