from django.contrib import admin

# Register your models here.
from mobility_apps.visa.models import Visa_Request, Visa_Request_Document

admin.site.register(Visa_Request)
admin.site.register(Visa_Request_Document)
