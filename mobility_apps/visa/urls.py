from django.urls import include, path, re_path
from .views import *

urlpatterns = [
        re_path('get_delete/visa_request/',get_delete_update_visa_request.as_view(), name='get_delete_update_visa_request'),
        path('get_add/visa_request/', get_post_visa_request.as_view(), name='get_post_visa_request'),
        path('get_add/visa_request_document/', get_post_visa_document.as_view(), name='get_post_visa_document'),
        path('employee_visa_request/', get_count_visa_request.as_view(), name='get_count_visa_request'),
        path('count_visa_requests/', get_count_visa_requests.as_view(), name='get_count_visa_requests'),
        path('org_visa_request/', get_org_visa_request.as_view(), name='get_org_visa_request'),
        path('get_view_visa_request/', get_view_visa_request.as_view(), name='get_view_visa_request'),
        path('get_visa_request/', get_visa_request.as_view(), name='get_visa_request'),
        path('get_visa_action/', get_visa_action.as_view(), name='get_visa_action'),
        path('get_visa_status_summary/', get_visa_status_summary.as_view(), name='get_visa_status_summary'),
        path('document_request_update/', get_post_visa_document_request_update.as_view(), name='get_post_visa_document_request_update'),
        path('get_org_count_visa_requests/', get_org_count_visa_requests.as_view(), name='get_org_count_visa_requests'),
        path('org_visa_requests/', org_visa_requests.as_view(), name='org_visa_requests'),
        #path('bulkupload/employee/', bulk_upload_employee.as_view(), name='bulk_upload_employee'),


]