from django.db import models

# Create your models here.
from mobility_apps.base.models import TimeStampedModel, GeneratedByModel, Status
# from mobility_apps.employee.models import Country
#from mobility_apps.master.models import Project, Organization
from mobility_apps.superadmin.models import Organizations
from mobility_apps.employee.models import Employee
from mobility_apps.master.models import Project
from django.utils.translation import ugettext_lazy as _


class Visa_Request(TimeStampedModel, GeneratedByModel, Status):
    visa_req_id = models.CharField(max_length=200,null=True, blank=True, unique=True)
    travel_req_id=  models.CharField(max_length=100,null=True, blank=True)
    req_id=  models.CharField(max_length=100,null=True, blank=True)
    emp_email= models.ForeignKey(Employee,to_field="emp_code", null=True, blank=True, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project,to_field="pid", null=True, blank=True, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200,null=True, blank=True)
    is_billable = models.BooleanField(blank=True,default=False)
    is_dependent = models.BooleanField(blank=True,default=False)
    vendor_fees = models.IntegerField(null=True,blank=True)
    govt_fees = models.IntegerField(null=True,blank=True)
    country = models.CharField(max_length=100,null=True, blank=True)
    dependent_name = models.CharField(max_length=100,null=True, blank=True)
    dependent_relation = models.CharField(max_length=100,null=True, blank=True)
    from_city = models.CharField(max_length=100,null=True, blank=True)
    to_city= models.CharField(max_length=100,null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id', null=True, blank=True, on_delete=models.CASCADE)
    travel_start_date = models.DateTimeField(null=True, blank=True)
    travel_end_date = models.DateTimeField( null=True,blank=True)
    visa_purpose = models.CharField(max_length=100,null=True,blank=True)
    applied_visa = models.CharField(max_length=20,null=True, blank=True)
    remark = models.CharField(max_length=200,null=True, blank=True)
    request_notes = models.CharField(max_length=200,null=True, blank=True)
    visa_status = models.CharField(max_length=50,null=True, blank=True)
    visa_status_notes = models.CharField(max_length=200,null=True, blank=True)
    current_ticket_owner = models.CharField(max_length=100,null=True, blank=True)
    supervisor= models.CharField(max_length=100, null=True, blank=True)
    expense_approver= models.CharField(max_length=100, null=True, blank=True)
    project_manager = models.CharField(max_length=100, null=True, blank=True)
    business_lead = models.CharField(max_length=100, null=True, blank=True)
    client_executive_lead = models.CharField(max_length=100, null=True, blank=True)
    approval_level = models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = _('Visa Request')
        verbose_name_plural = _('Visa Request')

    def __str__(self):
        return self.visa_req_id

    def __unicode__(self):
        return self.visa_req_id
#
#
class Visa_Request_Document(TimeStampedModel, GeneratedByModel, Status):
    req_id=  models.CharField(max_length=100,null=True, blank=True)
    visa_request = models.ForeignKey(Visa_Request,to_field="visa_req_id",max_length=255, related_name="visa_request_document", null=True, blank=True, on_delete=models.CASCADE)
    uploaded_document_name = models.FileField(upload_to='visaimage/', null=True, max_length=255)
    document_name= models.CharField(max_length=100, null=True, blank=True)
    document_type= models.CharField(max_length=100, null=True, blank=True)
    host_type= models.CharField(max_length=100, null=True, blank=True)
    request_note= models.CharField(max_length=100, null=True, blank=True)
    organization = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
    remark= models.CharField(max_length=10, null=True, blank=True)
    request_status= models.CharField(max_length=10, null=True, blank=True)
    visa_main_id= models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = _('Visa Request Document')
        verbose_name_plural = _('Visa Request Document')

    def __str__(self):
        return self.visa_request

    def __unicode__(self):
        return self.visa_request



class Visa_Request_Draft(TimeStampedModel, GeneratedByModel, Status):
    visa_req_id = models.CharField(max_length=200,null=True, blank=True, unique=True)
    travel_req_id= models.CharField(max_length=100,null=True, blank=True)
    emp_email= models.ForeignKey(Employee,to_field="email", null=True, blank=True, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project,to_field="pid", null=True, blank=True, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200,null=True, blank=True)
    is_billable = models.BooleanField(blank=True,default=False)
    vendor_fees = models.IntegerField(null=True,blank=True)
    govt_fees = models.IntegerField(null=True,blank=True)
    country = models.CharField(max_length=100,null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id', null=True, blank=True, on_delete=models.CASCADE)
    travel_start_date = models.DateTimeField(null=True, blank=True)
    travel_end_date = models.DateTimeField( null=True,blank=True)
    visa_purpose = models.CharField(max_length=100,null=True,blank=True)
    applied_visa = models.CharField(max_length=20,null=True, blank=True)
    request_notes = models.CharField(max_length=200,null=True, blank=True)
    visa_status = models.CharField(max_length=50,null=True, blank=True)
    visa_status_notes = models.CharField(max_length=200,null=True, blank=True)
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
        verbose_name = _('Visa Request Draft')
        verbose_name_plural = _('Visa Request Draft')

    def __str__(self):
        return self.visa_req_id

    def __unicode__(self):
        return self.visa_req_id


#
#

class Visa_Request_Document_Draft(TimeStampedModel, GeneratedByModel, Status):
    visa_request = models.ForeignKey(Visa_Request,to_field="visa_req_id",max_length=255, null=True, blank=True, on_delete=models.CASCADE)
    uploaded_document_name = models.ImageField(upload_to='visaimage/', null=True, max_length=255)
    document_name= models.CharField(max_length=100, null=True, blank=True)
    document_type= models.CharField(max_length=100, null=True, blank=True)
    organization = models.ForeignKey(Organizations,to_field='org_id', null=True, blank=True,on_delete=models.CASCADE)
    column1 = models.CharField(max_length=100, null=True, blank=True)
    column2 = models.CharField(max_length=100, null=True, blank=True)
    column3 = models.CharField(max_length=100, null=True, blank=True)
    column4 = models.CharField(max_length=100, null=True, blank=True)
    column5 = models.CharField(max_length=100, null=True, blank=True)
    column6 = models.CharField(max_length=100, null=True, blank=True)
    column7 = models.CharField(max_length=100, null=True, blank=True)
    column8 = models.CharField(max_length=100, null=True, blank=True)
    # column9 = models.CharField(max_length=100, null=True, blank=True)
    # column10 = models.CharField(max_length=100, null=True, blank=True)
    # column11 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Visa Request Document Draft')
        verbose_name_plural = _('Visa Request Document Draft')

    def __str__(self):
        return self.visa_request

    def __unicode__(self):
        return self.visa_request

