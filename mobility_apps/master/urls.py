from django.urls import include, path, re_path
from mobility_apps.master.views.country import *
from mobility_apps.master.views.project import *
from mobility_apps.master.views.department import *
from mobility_apps.master.views.dropdown import *
from mobility_apps.master.views.organization_location import *
from mobility_apps.master.views.organization import *
from mobility_apps.master.views.activity_log import *
from mobility_apps.master.views.request_status import *
from mobility_apps.master.views.role import *
from mobility_apps.master.views.vendor import *
from mobility_apps.master.views.visa import *
from mobility_apps.master.views.currency import *
from mobility_apps.master.views.assignment_group import *
from mobility_apps.master.views.assignment_type import *
from mobility_apps.master.views.visa_document_checklist import *
from mobility_apps.master.views.visa_purpose import *
from mobility_apps.master.views.approve_request import *
from mobility_apps.master.views.notification import *

urlpatterns = [
        path('get_delete/country/',get_delete_update_country.as_view(), name='get_delete_update_country'),
        path('get_add/country/', get_post_country.as_view(), name='get_post_country'),
        path('bulkupload/country/', bulk_upload_country.as_view(), name='bulk_upload_country'),
        path('bulkupload/currency/', bulk_upload_currency.as_view(), name='bulk_upload_currency'),
        path('get_add/currency/', get_post_currency.as_view(), name='get_post_currency'),
        path('bulkupload/currency_conversion/', bulk_upload_currency_conversion.as_view(), name='bulk_upload_currency_conversion'),
        path('get_country/', get_country.as_view(), name='get_country'),
        re_path('get_delete/project/',get_delete_update_project.as_view(), name='get_delete_update_project'),
        path('get_add/project/', get_post_project.as_view(), name='get_post_project'),
        path('bulkupload/project/', bulk_upload_project.as_view(), name='get_post_project'),
        re_path('get_delete/department/',get_delete_update_department.as_view(), name='get_delete_update_department'),
        path('get_add/department/', get_post_department.as_view(), name='get_post_department'),
        path('bulkupload/department/', bulk_upload_department.as_view(), name='get_post_department'),
        re_path('get_delete/organization/',get_delete_update_organization.as_view(), name='get_delete_update_organization'),
        path('get_add/organization/', get_post_organization.as_view(), name='get_post_organization'),
        path('bulkupload/organization/', bulk_upload_organization.as_view(), name='get_post_organization'),
        re_path('get_delete/organization_location/',get_delete_update_organization_location.as_view(), name='get_delete_update_organization_location'),
        path('get_add/organization_location/', get_post_organization_location.as_view(), name='get_post_organization_location'),
        path('bulkupload/organization_location/', bulk_upload_organization_location.as_view(), name='get_post_organization_location'),
        re_path('get_delete/activity_log/',get_delete_update_activity_log.as_view(), name='get_delete_update_activity_log'),
        path('get_add/activity_log/', get_post_activity_log.as_view(), name='get_post_activity_log'),
        path('bulkupload/activity_log/', bulk_upload_activity_type, name='get_post_activity_log'),
        re_path('get_delete/request_status',get_delete_update_reuest_status.as_view(), name='get_delete_update_request_status'),
        path('get_add/request_status/', get_post_reuest_status.as_view(), name='get_post_request_status'),
        path('bulkupload/request_status/', bulk_upload_request_status.as_view(), name='get_post_request_status'),
        re_path('get_delete/role/',get_delete_update_role.as_view(), name='get_delete_update_role'),
        path('get_add/role/', get_post_role.as_view(), name='get_post_role'),
        path('bulkupload/role/', bulk_upload_role.as_view(), name='get_post_role'),
        re_path('get_delete/vendor/', get_delete_update_vendor.as_view(), name='get_delete_update_vendor'),
        path('get_add/vendor/', get_post_vendor.as_view(), name='get_post_vendor'),
        path('bulkupload/vendor/', bulk_upload_Vendor.as_view(), name='get_post_vendor'),
        re_path('get_delete/visa/', get_delete_update_visa.as_view(), name='get_delete_update_visa'),
        path('get_add/visa/', get_post_visa.as_view(), name='get_post_visa'),
        path('get_visa_country/visa/', get_visa_country.as_view(), name='get_visa_country'),
        path('bulkupload/visa/', bulk_upload_visa.as_view(), name='get_post_visa'),
        #path(r'^get_delete/visa_document_checklist/', get_delete_update_visa_document_checklist.as_view(), name='get_delete_update_visa_document_checklist'),
        path('get_add/visa_document_checklist/', get_post_visa_document_checklist.as_view(), name='get_post_visa_document_checklist'),
        path('get_add/visa_che/', get_visa_country_checklist.as_view(), name='get_visa_country_checklist'),
        path('bulkupload/visa_document_checklist/', bulk_upload_visa_document_checklist.as_view(), name='get_post_visa_document_checklist'),
        re_path('get_delete/visa_purpose/', get_delete_update_visa_purpose.as_view(), name='get_delete_update_visa_purpose'),
        path('get_add/visa_purpose/', get_post_visa_purpose.as_view(), name='get_post_visa_purpose'),
        path('bulkupload/visa_purpose/', bulk_upload_visa_purpose.as_view(), name='get_post_visa_purpose'),
        path('get_add/group/', get_post_assignment_group.as_view(), name='get_post_assignment_group'),
        path('get_add/group_update/', get_delete_update_assignment_group.as_view(), name='get_delete_update_assignment_group'),
        path('bulkupload/visa_purpose/', bulk_upload_visa_purpose.as_view(), name='get_post_visa_purpose'),
        path('get_add/visa_purpose_list/', get_post_visa_purpose_list.as_view(), name='get_post_visa_purpose_list'),
        path('get_add/assignment_employee/', get_post_assignment_employee.as_view(), name='get_post_assignment_employee'),
        path('get_project/', get_project_list.as_view(), name='get_project_list'),
        path('get_project_list_user/', get_project_list_user.as_view(), name='get_project_list_user'),
        path('bulk_upload_city/', bulk_upload_city.as_view(), name='bulk_upload_city'),
        path('get_city/', get_city.as_view(), name='get_city'),
        path('bulk_upload_perdiem/', bulk_upload_perdiem.as_view(), name='bulk_upload_perdiem'),
        path('get_perdiem/', get_perdiem.as_view(), name='get_perdiem'),
        path('post_assignment_status/', get_post_assignment_status.as_view(), name='get_post_assignment_status'),
        path('approve_request/', get_post_approve_request.as_view(), name='get_post_approve_request'),
        path('dial_code/', dial_code.as_view(), name='dial_code'),
        path('get_dial_code/', get_dial_code.as_view(), name='get_dial_code'),
        path('get_country_master/', get_country_master.as_view(), name='get_country_master'),
        path('get_state_master/', get_state_master.as_view(), name='get_state_master'),
        path('bulk_upload_location/', bulk_upload_location.as_view(), name='bulk_upload_location'),
        path('get_post_location/', get_post_location.as_view(), name='get_post_location'),
        path('get_all_location/', get_all_location.as_view(), name='get_all_location'),
		path('get_active_currency/', get_active_currency.as_view(), name='get_active_currency'),
        path('get_currency_conversion/', get_currency_conversion.as_view(), name='get_currency_conversion'),
        path('bulk_upload_taxgrid/', bulk_upload_taxgrid.as_view(), name='bulk_upload_taxgrid'),
        path('get_taxgridmaster/', get_taxgridmaster.as_view(), name='get_taxgridmaster'),
        path('get_taxgridcountry/', get_taxgridcountry.as_view(), name='get_taxgridcountry'),
        path('add_taxgrid/', add_taxgrid.as_view(), name='add_taxgrid'),
		path('get_post_gender/', get_post_gender.as_view(), name='get_post_gender'),
        path('bulk_upload_Gender/', bulk_upload_Gender.as_view(), name='bulk_upload_Gender'),

        path('get_post_marital_status/', get_post_marital_status.as_view(), name='get_post_marital_status'),
        path('get_marital_status/', get_marital_status.as_view(), name='get_marital_status'),
        path('bulk_upload_marital_status/', bulk_upload_marital_status.as_view(), name='bulk_upload_marital_status'),

        path('get_post_salutation/', get_post_salutation.as_view(), name='get_post_salutation'),
        path('bulk_upload_salutation/', bulk_upload_salutation.as_view(), name='bulk_upload_salutation'),

        path('get_post_acedmic/', get_post_acedmic.as_view(), name='get_post_acedmic'),
        path('bulk_upload_acedmic/', bulk_upload_acedmic.as_view(), name='bulk_upload_acedmic'),

        path('get_post_suffix/', get_post_suffix.as_view(), name='get_post_suffix'),
        path('bulk_upload_suffix/', bulk_upload_suffix.as_view(), name='bulk_upload_suffix'),

        path('get_post_email/', get_post_email.as_view(), name='get_post_email'),
        path('bulk_upload_email/', bulk_upload_email.as_view(), name='bulk_upload_email'),

        path('get_post_phone/', get_post_phone.as_view(), name='get_post_phone'),
        path('bulk_upload_phone/', bulk_upload_phone.as_view(), name='bulk_upload_phone'),

        path('get_post_relation/', get_post_relation.as_view(), name='get_post_relation'),
        path('bulk_upload_relation/', bulk_upload_relation.as_view(), name='bulk_upload_relation'),

        path('get_post_termination/', get_post_termination.as_view(), name='get_post_termination'),
        path('bulk_upload_termination/', bulk_upload_termination.as_view(), name='bulk_upload_termination'),

        path('get_post_address/', get_post_address.as_view(), name='get_post_address'),
        path('bulk_upload_address/', bulk_upload_address.as_view(), name='bulk_upload_address'),
        

        path('get_post_language/', get_post_language.as_view(), name='get_post_language'),
        path('bulk_upload_language/', bulk_upload_language.as_view(), name='bulk_upload_language'),
        path('get_action_status/', get_action_status.as_view(), name='get_action_status'),
        path('get_post_visa_master/', get_post_visa_master.as_view(), name='get_post_visa_master'),
        path('visa_master_applicable/', get_post_visa_master_applicable.as_view(), name='get_post_visa_master_applicable'),
        path('get_vendors/', get_vendors.as_view(), name='get_vendors'),
        path('bulk_upload_national_id/', bulk_upload_national_id.as_view(), name='bulk_upload_national_id'),
        path('get_national_id/', get_national_id.as_view(), name='get_national_id'),
        path('get_vendors_type/', get_vendors_type.as_view(), name='get_vendors_type'),
        path('get_post_notification/', get_post_notification.as_view(), name='get_post_notification'),
        path('bulk_upload_country_master/', bulk_upload_country_master.as_view(), name='bulk_upload_country_master'),
        path('get_create_assignment/', get_create_assignment.as_view(), name='get_create_assignment'),
        path('get_assignments/', get_assignments.as_view(), name='get_assignments'),
        path('tax_grid_country_update/', tax_grid_country_update.as_view(), name='tax_grid_country_update'),
        path('get_projects/', get_projects.as_view(), name='get_projects'),
        
        path('get_designation/', get_designation.as_view(), name='get_designation'),
        path('bulk_upload_designation/', bulk_upload_designation.as_view(), name='bulk_upload_designation'),

        path('active_taxgrid/', active_taxgrid.as_view(), name='active_taxgrid'),
        path('get_update_project/', get_update_project.as_view(), name='get_update_project'),
        path('post_currency_conversion/', post_currency_conversion.as_view(), name='post_currency_conversion'),
        path('add_taxgrid_label/', add_taxgrid_label.as_view(), name='add_taxgrid_label'),
        path('currency_conversion_history/', currency_conversion_history.as_view(), name='currency_conversion_history'),
        path('get_post_country_policy/', get_post_country_policy.as_view(), name='get_post_country_policy'),
        path('bulk_upload_country_policy/', bulk_upload_country_policy.as_view(), name='bulk_upload_country_policy'),
        path('bulk_upload_vendor_category/', bulk_upload_vendor_category.as_view(), name='bulk_upload_vendor_category'),
        path('get_vendors_category/', get_vendors_category.as_view(), name='get_vendors_category'),
        path('bulk_upload_vendor_master/', bulk_upload_vendor_master.as_view(), name='bulk_upload_vendor_master'),
        path('get_post_per_diem/', get_post_per_diem.as_view(), name='get_post_per_diem'),
        path('post_country_policy/', post_country_policy.as_view(), name='post_country_policy'),



        path('json_upload/country/', json_upload_country.as_view(), name='json_upload_country'),
        path('json_upload_city/', json_upload_city.as_view(), name='json_upload_city'),
        path('json_upload/currency/', json_upload_currency.as_view(), name='json_upload_currency'),
        path('json_upload/currency_conversion/', json_upload_currency_conversion.as_view(), name='json_upload_currency_conversion'),
        path('json_upload/project/', json_upload_project.as_view(), name='json_upload_project'),
        path('json_upload/department/', json_upload_department.as_view(), name='json_upload_department'),
        path('json_upload/organization_location/', json_upload_organization_location.as_view(), name='json_upload_organization_location'),
        path('json_upload/role/', json_upload_role.as_view(), name='json_upload_role'),


        path('update_master_vendors_type/<int:pk>/', update_master_vendors_type.as_view(), name='update_post_master_vendors_type'),
        path('get_post_master_vendors_type/', get_post_master_vendors_type.as_view(), name='get_post_master_vendors_type'),
        path('update_purpose_of_travel/<int:pk>/', update_purpose_of_travel.as_view(), name='update_purpose_of_travel'),
        path('update_master_location/<int:pk>/', update_master_location.as_view(), name='update_master_location'),
        path('update_master_salutation/<int:pk>/', update_master_salutation.as_view(), name='update_master_salutation'),
        path('update_master_suffix/<int:pk>/', update_master_suffix.as_view(), name='update_master_suffix'),
        path('update_master_marital_status/<int:pk>/', update_master_marital_status.as_view(), name='update_master_marital_status'),
        path('update_master_address/<int:pk>/', update_master_address.as_view(), name='update_master_address'),
        path('update_master_email/<int:pk>/', update_master_email.as_view(), name='update_master_email'),
        path('update_master_phone_type/<int:pk>/', update_master_phone_type.as_view(), name='update_master_phone_type'),
        path('update_master_relation_type/<int:pk>/', update_master_relation_type.as_view(), name='update_master_relation_type'),
        path('update_master_national_id/<int:pk>/', update_master_national_id.as_view(), name='update_master_national_id'),
        path('currency_conversion_history_new/', currency_conversion_history_new.as_view(), name='currency_conversion_history'),


        path('get_post_vendor_income/', get_post_vendor_income.as_view(), name='get_post_vendor_income'),
        path('get_post_capital_gains_income/', get_post_capital_gains_income.as_view(), name='get_post_capital_gainsI_income'),
        path('get_post_Vendor_Status_history/', get_post_Vendor_Status_history.as_view(), name='get_post_Vendor_Status_history'),
        path('get_post_vendor_Service_List/', get_post_vendor_Service_List.as_view(), name='get_post_vendor_Service_List'),
        path('get_post_vendor_Service_List_status/', get_post_vendor_Service_List_status.as_view(), name='get_post_vendor_Service_List_status'),


        path('get_post_vaccine_autho_country/', GetPostVaccineAuthoCountry.as_view(), name='get_post_vaccine_autho_country'),





]