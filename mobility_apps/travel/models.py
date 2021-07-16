from django.db import models

# Create your models here.
from mobility_apps.base.models import TimeStampedModel, GeneratedByModel, Status
from mobility_apps.employee.models import Employee
from mobility_apps.master.models import Project,Assignment_Type
from mobility_apps.superadmin.models import *
from mobility_apps.visa.models import Visa_Request
#from mobility_apps.master.models import Project, Country, Assignment_Type, Organization
from django.utils.translation import ugettext_lazy as _


class Travel_Request(TimeStampedModel, GeneratedByModel, Status):
    travel_req_id = models.CharField(max_length=200,null=True, blank=True, unique=True)
    emp_email= models.ForeignKey(Employee,to_field="emp_code", null=True, blank=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project,to_field="pid", related_name="travel_request", null=True, blank=True,  on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200,null=True, blank=True)
    policy_violations=models.CharField(max_length=200,null=True, blank=True)
    is_billable = models.BooleanField(default=False)
    is_travel_multi_country = models.BooleanField(default=False)
    is_travel_multi_city = models.BooleanField(default=False)
    request_notes = models.CharField(max_length=200,null=True, blank=True)
    remark = models.CharField(max_length=200,null=True, blank=True)
    #agenda = models.CharField(max_length=200,null=True, blank=True)
    home_contact_name = models.CharField(max_length=100,null=True, blank=True)
    home_phone_ext = models.CharField(max_length=20,null=True, blank=True)
    home_phone_number = models.CharField(max_length=20,null=True, blank=True)
    is_laptop_required = models.BooleanField(default=False)
    travel_req_status = models.CharField(max_length=50,null=True, blank=True)
    travel_req_status_notes = models.CharField(max_length=200,null=True, blank=True)
    current_ticket_owner = models.CharField(max_length=100,null=True, blank=True)
    organization = models.ForeignKey(Organizations,to_field='org_id', null=True, blank=True, on_delete=models.CASCADE)
    supervisor= models.CharField(max_length=100, null=True, blank=True)
    expense_approver= models.CharField(max_length=100, null=True, blank=True)
    project_manager = models.CharField(max_length=100, null=True, blank=True)
    business_lead = models.CharField(max_length=100, null=True, blank=True)
    client_executive_lead = models.CharField(max_length=100, null=True, blank=True)
    have_laptop = models.BooleanField(default=True)
    approval_level = models.CharField(max_length=100, null=True, blank=True)
    expence_cureency = models.CharField(max_length=100, null=True, blank=True)
    expence_departureDate = models.CharField(max_length=100, null=True, blank=True)
    expence_estimatedCost = models.CharField(max_length=100, null=True, blank=True)
    expence_fromCountry = models.CharField(max_length=100, null=True, blank=True)
    expence_returnDate = models.CharField(max_length=100, null=True, blank=True)
    expence_toCountry = models.CharField(max_length=100, null=True, blank=True)
    attachments = models.CharField(max_length=1000, null=True, blank=True)
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
    pri_type_req = models.CharField(max_length=70, null=True, blank=True)



    class Meta:
        managed = True
        verbose_name = _('Travel Request')
        verbose_name_plural = _('Travel Request')

    def __str__(self):
        return self.travel_req_id

    def __unicode__(self):
        return self.travel_req_id

class Travel_Request_Details(TimeStampedModel, GeneratedByModel, Status):
    travel_req_id = models.ForeignKey(Travel_Request,to_field="travel_req_id",related_name="travel_request_details",null=True, blank=True,  on_delete=models.CASCADE)
    travelling_country = models.CharField(max_length=100,null=True, blank=True)
    travelling_country_to = models.CharField(max_length=100,null=True, blank=True)
    office_location = models.CharField(max_length=100,null=True, blank=True)
    client_number_ext = models.CharField(max_length=100,null=True, blank=True)
    client_number = models.CharField(max_length=100,null=True, blank=True)
    organization = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
    source_city = models.CharField(max_length=100, blank=True, null=True)
    destination_city = models.CharField(max_length=150, blank=True, null=True)
    departure_date = models.DateTimeField(null=True,blank=True)
    return_date = models.DateTimeField(null=True,blank=True)
    is_accmodation_required = models.BooleanField(default=True)
    accmodation_start_date = models.CharField(max_length=100, null=True, blank=True)
    accmodation_end_date = models.CharField(max_length=100, null=True, blank=True)
    travel_purpose = models.CharField(max_length=100, blank=True, null=True)
    assignment_type = models.ForeignKey(Assignment_Type, related_name="travel_request_details", null=True, blank=True,  on_delete=models.CASCADE)
    applicable_visa = models.CharField(max_length=20, blank=True, null=True)
    visa_number = models.CharField(max_length=100, blank=True, null=True)
    visa_expiry_date = models.CharField(max_length=100, null=True, blank=True)
    host_hr_name = models.CharField(max_length=100, blank=True, null=True)
    host_country_head = models.CharField(max_length=100, blank=True, null=True)
    host_attorney = models.CharField(max_length=100, blank=True, null=True)
    host_phone_ext = models.CharField(max_length=20, blank=True, null=True)
    host_phone_no = models.CharField(max_length=20, blank=True, null=True)
    is_client_location = models.BooleanField(default=True)
    client_name = models.CharField(max_length=100, blank=True, null=True)
    client_address = models.CharField(max_length=200, blank=True, null=True)
    hotel_cost = models.FloatField(max_length=200, blank=True, null=True)
    per_diem_cost = models.FloatField(max_length=200, blank=True, null=True)
    airfare_cost = models.FloatField(max_length=200, blank=True, null=True)
    transportation_cost = models.FloatField(max_length=200, blank=True, null=True)
    total_cost = models.FloatField(max_length=200, blank=True, null=True)
    currency = models.CharField(max_length=50, blank=True, null=True)
    reporting_currency = models.CharField(max_length=50, blank=True, null=True)
    travel_request_status = models.CharField(max_length=50, blank=True, null=True)
    travel_request_status_notes = models.CharField(max_length=200, blank=True, null=True)
    is_dependent = models.BooleanField(default=True)
    
    agenda = models.CharField(max_length=1000, null=True, blank=True)
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
        verbose_name = _('Travel Request Detail')
        verbose_name_plural = _('Travel Request Detail')

    def __str__(self):
        return self.destination_city

    def __unicode__(self):
        return self.destination_city


class Travel_Request_Dependent(TimeStampedModel, GeneratedByModel, Status):
    travel_req_id = models.ForeignKey(Travel_Request,to_field="travel_req_id",null=True, blank=True,  on_delete=models.CASCADE)
    req_id= models.CharField(max_length=100,null=True, blank=True)
    dependent_relation = models.CharField(max_length=100,null=True, blank=True)
    dependent_name = models.CharField(max_length=100,null=True, blank=True)
    dependent_passport = models.CharField(max_length=100,null=True, blank=True)
    dependent_visa = models.CharField(max_length=100, blank=True, null=True)
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
        verbose_name = _('Travel Request Dependent')
        verbose_name_plural = _('Travel Request Dependent')

    def __str__(self):
        return self.travel_req_id

    def __unicode__(self):
        return self.travel_req_id



class Travel_Request_Draft(TimeStampedModel, GeneratedByModel, Status):
    travel_req_id = models.CharField(max_length=200,null=True, blank=True, unique=True)
    emp_email= models.ForeignKey(Employee,to_field="emp_code", null=True, blank=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project,to_field="pid", related_name="Travel_Request_Draft", null=True, blank=True,  on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200,null=True, blank=True)
    is_billable = models.BooleanField(default=False)
    is_travel_multi_country = models.BooleanField(default=False)
    is_travel_multi_city = models.BooleanField(default=False)
    request_notes = models.CharField(max_length=200,null=True, blank=True)
    remark = models.CharField(max_length=200,null=True, blank=True)
    #agenda = models.CharField(max_length=200,null=True, blank=True)
    home_contact_name = models.CharField(max_length=100,null=True, blank=True)
    home_phone_ext = models.CharField(max_length=40,null=True, blank=True)
    home_phone_number = models.CharField(max_length=20,null=True, blank=True)
    is_laptop_required = models.BooleanField(default=False)
    travel_req_status = models.CharField(max_length=50,null=True, blank=True)
    travel_req_status_notes = models.CharField(max_length=200,null=True, blank=True)
    current_ticket_owner = models.CharField(max_length=100,null=True, blank=True)
    organization = models.ForeignKey(Organizations,to_field='org_id', null=True, blank=True, on_delete=models.CASCADE)
    supervisor= models.CharField(max_length=100, null=True, blank=True)
    expense_approver= models.CharField(max_length=100, null=True, blank=True)
    project_manager = models.CharField(max_length=100, null=True, blank=True)
    business_lead = models.CharField(max_length=100, null=True, blank=True)
    client_executive_lead = models.CharField(max_length=100, null=True, blank=True)
    have_laptop = models.BooleanField(default=True)
    vpKeys = models.CharField(max_length=1000, null=True, blank=True)
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
        verbose_name = _('Travel Request Draft')
        verbose_name_plural = _('Travel Request Draft')

    def __str__(self):
        return self.travel_req_id

    def __unicode__(self):
        return self.travel_req_id

class Travel_Request_Details_Draft(TimeStampedModel, GeneratedByModel, Status):
    travel_req_id = models.ForeignKey(Travel_Request_Draft,to_field="travel_req_id",related_name="travel_request_details",null=True, blank=True,  on_delete=models.CASCADE)
    travelling_country = models.CharField(max_length=100,null=True, blank=True)
    travelling_country_to = models.CharField(max_length=100,null=True, blank=True)
    office_location = models.CharField(max_length=100,null=True, blank=True)
    client_number_ext = models.CharField(max_length=100,null=True, blank=True)
    client_number = models.CharField(max_length=100,null=True, blank=True)
    organization = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)
    source_city = models.CharField(max_length=100, blank=True, null=True)
    destination_city = models.CharField(max_length=100, blank=True, null=True)
    departure_date = models.CharField(max_length=100, null=True, blank=True)
    return_date = models.CharField(max_length=100, null=True, blank=True)
    is_accmodation_required = models.BooleanField(default=True)
    accmodation_start_date = models.CharField(max_length=100, null=True, blank=True)
    accmodation_end_date = models.CharField(max_length=100, null=True, blank=True)
    travel_purpose = models.CharField(max_length=100, blank=True, null=True)
    assignment_type = models.ForeignKey(Assignment_Type, related_name="travel_request_details_draft", null=True, blank=True,  on_delete=models.CASCADE)
    applicable_visa = models.CharField(max_length=20, blank=True, null=True)
    visa_number = models.CharField(max_length=100, blank=True, null=True)
    visa_expiry_date = models.CharField(max_length=100, null=True, blank=True)
    host_hr_name = models.CharField(max_length=100, blank=True, null=True)
    host_country_head = models.CharField(max_length=100, blank=True, null=True)
    host_attorney = models.CharField(max_length=100, blank=True, null=True)
    host_phone_ext = models.CharField(max_length=20, blank=True, null=True)
    host_phone_no = models.CharField(max_length=20, blank=True, null=True)
    is_client_location = models.BooleanField(default=True)
    client_name = models.CharField(max_length=100, blank=True, null=True)
    client_address = models.CharField(max_length=200, blank=True, null=True)
    hotel_cost = models.FloatField(max_length=200, blank=True, null=True)
    per_diem_cost = models.FloatField(max_length=200, blank=True, null=True)
    airfare_cost = models.FloatField(max_length=200, blank=True, null=True)
    transportation_cost = models.FloatField(max_length=200, blank=True, null=True)
    total_cost = models.FloatField(max_length=200, blank=True, null=True)
    currency = models.CharField(max_length=50, blank=True, null=True)
    reporting_currency = models.CharField(max_length=50, blank=True, null=True)
    travel_request_status = models.CharField(max_length=50, blank=True, null=True)
    travel_request_status_notes = models.CharField(max_length=200, blank=True, null=True)
    is_dependent = models.BooleanField(default=True)
    
    agenda = models.CharField(max_length=1000, null=True, blank=True)
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
        verbose_name = _('Travel Request Detail Draft')
        verbose_name_plural = _('Travel Request Detail Draft')

    def __str__(self):
        return self.destination_city

    def __unicode__(self):
        return self.destination_city


class Travel_Request_Dependent_Draft(TimeStampedModel, GeneratedByModel, Status):
    travel_req_id = models.ForeignKey(Travel_Request_Draft,to_field="travel_req_id",null=True, blank=True,  on_delete=models.CASCADE)
    req_id= models.CharField(max_length=100,null=True, blank=True)
    dependent_relation = models.CharField(max_length=100,null=True, blank=True)
    dependent_name = models.CharField(max_length=100,null=True, blank=True)
    dependent_passport = models.CharField(max_length=100,null=True, blank=True)
    dependent_visa = models.CharField(max_length=100, blank=True, null=True)
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
        verbose_name = _('Travel Request Dependent')
        verbose_name_plural = _('Travel Request Dependent')



class Travel_Request_Action_History(TimeStampedModel, GeneratedByModel, Status):
    email=models.ForeignKey(Employee,to_field="emp_code", null=True, blank=True, on_delete=models.CASCADE)
    travel_req_id = models.ForeignKey(Travel_Request,to_field="travel_req_id",null=True, blank=True,  on_delete=models.CASCADE)
    action = models.CharField(max_length=100,null=True, blank=True)
    module = models.CharField(max_length=100,null=True, blank=True)
    action_notes  = models.CharField(max_length=100,null=True, blank=True)
    approval_level = models.CharField(max_length=100, null=True, blank=True)
    organization  = models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = _('Travel Request Action History')
        verbose_name_plural = _('Travel Request Action History')



class Visa_Request_Action_History(TimeStampedModel, GeneratedByModel, Status):
    email=models.ForeignKey(Employee,to_field="emp_code", null=True, blank=True, on_delete=models.CASCADE)
    visa_req_id = models.ForeignKey(Visa_Request,to_field="visa_req_id",null=True, blank=True,  on_delete=models.CASCADE)
    action = models.CharField(max_length=100,null=True, blank=True)
    action_notes  = models.CharField(max_length=200,null=True, blank=True)
    module  = models.CharField(max_length=100,null=True, blank=True)
    approval_level = models.CharField(max_length=100, null=True, blank=True)
    
    organization= models.ForeignKey(Organizations,to_field='org_id',null=True, blank=True,on_delete=models.CASCADE)

    class Meta:
        managed = True
        verbose_name = _('Visa Request Action History')
        verbose_name_plural = _('Visa Request Action History')
		
class Assignment_Travel_Request_Status(TimeStampedModel, GeneratedByModel, Status):
    travel_req_id = models.ForeignKey(Travel_Request,to_field="travel_req_id",null=True, blank=True,  on_delete=models.CASCADE)
    statusAction = models.CharField(max_length=100,null=True, blank=True)
    travel_req_status = models.CharField(max_length=100,null=True, blank=True)
    current_ticket_owner = models.CharField(max_length=100,null=True, blank=True)
    vendor = models.CharField(max_length=100, blank=True, null=True)
    vendor_type = models.CharField(max_length=100, blank=True, null=True)
    travel_req_status_vendor = models.CharField(max_length=50, null=True, blank=True)
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
    currency = models.CharField(max_length=100, null=True, blank=True)
    invoice_amount = models.CharField(max_length=100, null=True, blank=True)
    po_number = models.CharField(max_length=100, null=True, blank=True)
    invoice_number = models.CharField(max_length=100, null=True, blank=True)
    invoice_date = models.CharField(max_length=100, null=True, blank=True)
    services = models.CharField(max_length=250, null=True, blank=True)
    file_attachments = models.TextField(null=True, blank=True)
    vendor_status = models.CharField(max_length=100, null=True, blank=True)
    vendor_remark = models.CharField(max_length=200, null=True, blank=True)
    pickup_address = models.TextField(null=True, blank=True)
    delivery_address = models.TextField(null=True,blank=True)
    tent_move_date  = models.CharField(max_length=100, null=True,blank=True)
    tent_delivery_date  = models.CharField(max_length=100, null=True,blank=True)


    employment_income_amount  = models.CharField(max_length=100, null=True,blank=True)
    interest_income_amount  = models.CharField(max_length=100, null=True,blank=True)
    dividend_income_amount  = models.CharField(max_length=100, null=True,blank=True)
    rent_and_royalty_income_amount  = models.CharField(max_length=100, null=True,blank=True)
    self_employment_income_amount  = models.CharField(max_length=100, null=True,blank=True)
    income_from_partnership_amount  = models.CharField(max_length=100, null=True,blank=True)
    retirement_income_amount  = models.CharField(max_length=100, null=True,blank=True)
    capital_gains_amount  = models.CharField(max_length=100, null=True,blank=True)


    employment_income_owner  = models.CharField(max_length=100, null=True,blank=True)
    interest_income_owner  = models.CharField(max_length=100, null=True,blank=True)
    dividend_income_owner  = models.CharField(max_length=100, null=True,blank=True)
    rent_and_royalty_income_owner  = models.CharField(max_length=100, null=True,blank=True)
    self_employment_income_owner  = models.CharField(max_length=100, null=True,blank=True)
    income_from_partnership_owner  = models.CharField(max_length=100, null=True,blank=True)
    retirement_income_owner  = models.CharField(max_length=100, null=True,blank=True)
    capital_gains_owner  = models.CharField(max_length=100, null=True,blank=True)



    class Meta:
        managed = True
        verbose_name = _('Assignment Travel Request Status')
		
class Assignment_Travel_Tax_Grid(TimeStampedModel, GeneratedByModel, Status):
    travel_req_id = models.ForeignKey(Travel_Request,to_field="travel_req_id",null=True, blank=True,  on_delete=models.CASCADE)
    tax_label_id = models.CharField(max_length=100,null=True, blank=True)
    amount = models.CharField(max_length=100, blank=True, null=True)
    annual_ammount = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=100,null=True, blank=True)
    report_currency = models.CharField(max_length=100,null=True, blank=True)
    report_currency_ammount = models.CharField(max_length=100,null=True, blank=True)
    frequency = models.CharField(max_length=100,null=True, blank=True)
    group_by = models.CharField(max_length=100,null=True, blank=True)
    tax_label = models.CharField(max_length=100,null=True, blank=True)
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
        verbose_name = _('Assignment Travel Tax Grid')


class Travel_Vendor_Immigration(TimeStampedModel, GeneratedByModel, Status):
    travel_req = models.ForeignKey(Travel_Request, to_field="travel_req_id", null=True, blank=True,
                                      on_delete=models.CASCADE)
    organization = models.ForeignKey(Organizations, to_field='org_id', null=True, blank=True, on_delete=models.CASCADE)
    emp_code = models.ForeignKey(Employee, to_field="emp_code", null=True, blank=True, on_delete=models.CASCADE)
    Host_job_code = models.CharField(max_length=100,null=True, blank=True)
    Host_job_description = models.CharField(max_length=100, null=True, blank=True)


    class Meta:
        managed = True
        verbose_name = _('Travel Vendor Immigration')

