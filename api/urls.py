from django.urls import path
from api import views


urlpatterns=[

    path('hello/', views.Helloview.as_view(), name='hello'),
]