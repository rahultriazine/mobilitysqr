from django.urls import include, path, re_path
from .views import *

urlpatterns = [
        re_path('get_delete/travel_request/',get_delete_update_travel_request.as_view(), name='get_delete_update_travel_request'),
        path('get_add/travel_request/', get_post_travel_request.as_view(), name='get_post_travel_request'),
        path('employee_travel_request/', get_count_travel_request.as_view(), name='get_count_travel_request'),
        path('count_travel_requests/', get_count_travel_requests.as_view(), name='get_count_travel_requests'),
        path('org_travel_request/', get_org_travel_request.as_view(), name='get_org_travel_request'),
        path('get_view_travel_request/', get_view_travel_request.as_view(), name='get_view_travel_request'),
        path('get_post_travel_request_draft/', get_post_travel_request_draft.as_view(), name='get_post_travel_request_draft'),
        path('get_travel_request_approver/', get_travel_request_approver.as_view(), name='get_travel_request_approver'),
        path('get_travel_request_history/', get_travel_request_history.as_view(), name='get_travel_request_history'),
        path('get_travel_status_summary/', get_travel_status_summary.as_view(), name='get_travel_status_summary'),
        path('get_post_approve_travelvisa_request/', get_post_approve_travelvisa_request.as_view(), name='get_post_approve_travelvisa_request'),
        path('assignment_travel_request_status/', assignment_travel_request_status.as_view(), name='assignment_travel_request_status'),
        path('assignment_travel_tax_grid/', assignment_travel_tax_grid.as_view(), name='assignment_travel_tax_grid'),
        path('get_org_count_travel_requests/', get_org_count_travel_requests.as_view(), name='get_org_count_travel_requests'),
        path('org_travel_requests/', org_travel_requests.as_view(), name='org_travel_requests'),
        path('get_view_travel_request_draft/', get_view_travel_request_draft.as_view(), name='get_view_travel_request_draft'),
        path('assignment_post_approve_travelvisa_request/', assignment_post_approve_travelvisa_request.as_view(), name='assignment_post_approve_travelvisa_request'),
        path('delete_save/', delete_save.as_view(), name='delete_save'),
        path('get_upcoming_travel_request/', get_upcoming_travel_request.as_view(), name='get_upcoming_travel_request'),
        
        path('get_approve_reject_request_by_mail/', approved_Reject_TravelRequestByMail.as_view(), name='get_approve_reject_request_by_mail'),
        re_path(r'^get_travel_count_user/$', getTravelCountUser.as_view(), name='get_travel_count_user'),
        path('get_travel_request_approver_top/', get_travel_request_approver_top.as_view(), name='get_travel_request_approver_top'),
        path('travel_request_priority/', travel_request_priority.as_view(),
             name='travel_request_priority'),

]