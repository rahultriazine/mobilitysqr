from django.urls import include, path, re_path
from .views import *
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
        path('get_delete/employee/',get_delete_update_employee.as_view(), name='get_delete_update_employee'),
        path('get_add/employee/', get_post_employee.as_view(), name='get_post_employee'),
        path('get_employee_passport/', get_employee_passport.as_view(), name='get_employee_passport'),
        path('get_add/employee_passport/', get_post_employee_passport.as_view(), name='get_post_employee_passport'),
        path('get_add/employee_visa/', get_post_employee_visa.as_view(), name='get_post_employee_visa'),
        path('bulkupload/employee/', bulk_upload_employee.as_view(), name='bulk_upload_employee'),
        path('get_delete_update_employee/',get_delete_update_employee.as_view(), name='get_delete_update_employee'),
        path('get_add/employee_detail/', get_post_employee_details.as_view(), name='get_post_employee_details'),
        re_path(r'^get_delete/employee/(?P<pk>\d+)/$',get_delete_update_employee.as_view(), name='get_delete_update_employee'),
        path('get_add/employee_visa_detail/', get_post_employee_visa_details.as_view(), name='get_post_employee_visa_details'),
        #path('get_approver_details/', get_approver_details.as_view(), name='get_approver_details'),
        path('get_employee_visa/', get_post_visa_country.as_view(), name='get_post_visa_country'),
        #path('get_employee_visa_dependent/', get_post_visa_country_dependent.as_view(), name='get_post_visa_country_dependent'),
        path('get_employee_group/', get_post_employee_group.as_view(), name='get_post_employee_group'),
        path('emoloyeeinfo/', emoloyeeinfo.as_view(), name='emoloyeeinfo'),
        path('get_add/employee_address/', get_post_employee_address.as_view(), name='get_post_employee_address'),
        path('get_add/employee_emails/', get_post_employee_emails.as_view(), name='get_post_employee_emails'),
        #need to tested
        path('get_add/employee_phoneinfo/', get_post_employee_phoneinfo.as_view(), name='get_post_employee_phoneinfo'),
        path('get_add/employee_nationalid/', get_post_employee_nationalid.as_view(), name='get_post_employee_nationalid'),
        path('get_add/employee_emergencycontact/', get_post_employee_emergencycontact.as_view(), name='get_post_employee_emergencycontact'),
        path('emoloyeedetails/', emoloyeedetails.as_view(), name='emoloyeedetails'),
        path('get_post_employee_passport/', get_post_employee_passport.as_view(), name='get_post_employee_passport'),
        path('get_post_employee_visa/', get_post_employee_visa.as_view(), name='get_post_employee_visa'),
        path('userinfo/', get_post_employee_info.as_view(), name='get_post_employee_info'),
        path('employee_oficeaddress/', get_post_employee_officeaddress.as_view(), name='get_post_employee_officeaddress'),
        path('emoloyeedependent/', emoloyeedependent.as_view(), name='emoloyeedependent'),
        path('getemoloyeedata/', getemoloyeedata.as_view(), name='getemoloyeedata'),
        path('emoloyee_search_info/', emoloyee_search_info.as_view(), name='emoloyee_search_info'),
        path('forget_password/', forget_password.as_view(), name='forget_password'),
        path('is_termandcondtion/', is_termandcondtion.as_view(), name='is_termandcondtion'),
        path('reset_password/', reset_password.as_view(), name='reset_password'),
        path('uploadDoc/', uploadDoc.as_view(), name='upload Doc'),
        path('checkemployeeuser/', checkemployeeuser.as_view(), name='checkemployeeuser'),
        path('checkemployeeempcode/', checkemployeeempcode.as_view(), name='checkemployeeempcode'),
        path('checkemployeeemail/', checkemployeeemail.as_view(), name='checkemployeeemail'),
        path('transfer_emoloyeedetails/', transfer_emoloyeedetails.as_view(), name='transfer_emoloyeedetails'),
        path('get_post_employee_orginfo/', get_post_employee_orginfo.as_view(), name='get_post_employee_orginfo'),
        path('FileUploadView/', FileUploadView.as_view(), name='FileUploadView'),
        path('GETData/', GETData.as_view(), name='GETData'),
        path('import_employee/', import_employee.as_view(), name='import_employee'),
        path('Otp_Generate/', Otp_Generate.as_view(), name='Otp_Generate'),
        path('access_token/', access_token.as_view(), name='access_token'),
        re_path(r'^post_get_calender_event/$', calender_event_get_post.as_view(), name="post_get_calender_event"),
        path('delete_update_calender_event/<int:pk>/', calender_event_update_delete.as_view(), name="delete_update_calender_event"),
        path('get_calender_activity/',calender_activity.as_view(),name="get_calender_activity"),


        path('getemployee_personal_info/', getEmployeePersonalInfo.as_view(), name="getemployee_personal_info"),
        path('getemployee_org_info/', getEmployeeOrgInfo.as_view(), name="getemployee_org_info"),
        path('getemployee_address_info/', getEmployeeAddressInfo.as_view(), name="getemployee_address_info"),
        path('getemployee_email_info/', getEmployeeEmailInfo.as_view(), name="getemployee_email_info"),
        path('getemployee_phone_info/', getEmployeePhoneInfo.as_view(), name="getemployee_phone_info"),
        path('getemployee_national_id/', getEmployeeNationalId.as_view(), name="getemployee_national_id"),
        path('getemployee_emergency_contact/', getEmployeeEmergencyContact.as_view(), name="getemployee_emergency_contact"),
        path('getemployee_passport_info/', getEmployeePassportInfo.as_view(), name="getemployee_passport_info"),
        path('getemployee_visa_info/', getEmployeeVisaInfo.as_view(), name="getemployee_visa_info"),


        path('bulk_json_upload/employee/', bulk_json_upload_employee.as_view(), name='bulk_json_upload_employee'),
        path('bulk_json_upload/employee_orginfo/', bulk_json_upload_employee_orginfo.as_view(), name='bulk_json_upload_employee_orginfo'),
        path('bulk_json_upload/employee_address/', bulk_json_upload_employee_address.as_view(), name='bulk_json_upload_employee_address'),
        path('bulk_json_upload/employee_emails/', bulk_json_upload_employee_emails.as_view(), name='bulk_json_upload_employee_emails'),
        path('bulk_json_upload/employee_phoneinfo/', bulk_json_upload_phoneinfo.as_view(), name='bulk_json_upload_employee_phoneinfo'),
        path('bulk_json_upload/employee_nationalid/', bulk_json_upload_employee_nationalid.as_view(), name='bulk_json_upload_employee_nationalid'),
        path('bulk_json_upload/employee_visa/', bulk_json_upload_employee_visa.as_view(), name='get_post_employee_visa'),
        path('bulk_json_upload/employee_emergencycontact/', bulk_json_upload_employee_emergencycontact.as_view(), name='bulk_json_upload_employee_emergencycontact'),
        path('bulk_json_upload/employee_passport/', bulk_json_upload_employee_passport.as_view(), name='bulk_json_upload_employee_passport'),


        path('employee_chat/', employee_chat.as_view(), name='employee_chat'),



           ]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)