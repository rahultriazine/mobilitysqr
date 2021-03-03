from django.urls import include, path, re_path
from .views import *



urlpatterns = [

        path('visa_category_reports/', visa_category_reports.as_view(), name='visa_category_reports'),
        path('travel_country_reports/', travel_country_reports.as_view(), name='travel_country_reports'),
        path('visa_country_reports/', visa_country_reports.as_view(), name='visa_country_reports'),
        path('assignment_travel_tax_grid_reports/', assignment_travel_tax_grid_reports.as_view(), name='assignment_travel_tax_grid_reports'),
        path('all_assignment_travel_tax_grid_reports/', all_assignment_travel_tax_grid_reports.as_view(), name='all_assignment_travel_tax_grid_reports'),
]