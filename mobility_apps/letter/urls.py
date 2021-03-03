from django.urls import include, path, re_path
from .views import *



urlpatterns = [
        path('getassignmentletter/', getassignmentletter.as_view(), name='getassignmentletter'),
        path('getinviteletter/', getinviteletter.as_view(), name='getinviteletter'),
        path('getvisaletter/', getvisaletter.as_view(), name='getvisaletter'),
        path('assignmentletterkeys/', assignmentletterkeys.as_view(), name='assignmentletterkeys'),
        path('uploadletters/', uploadletters.as_view(), name='uploadletters'),
        path('getSavedTemplate/', getSavedTemplate.as_view(), name='getSavedTemplate'),

]