from django.contrib import admin

# Register your models here.
from mobility_apps.travel.models import *

admin.site.register(Travel_Request)
admin.site.register(Travel_Request_Details)
