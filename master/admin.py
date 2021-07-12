from django.contrib import admin

# Register your models here.
from mobility_apps.master.models import Project, Country, Visa_Purpose, Visa, Visa_Document_Checklist, Assignment_Type, \
    Department, Organization, Organization_Location, Vendor, Role,Assignment_Group, Request_Status, Activity_Log,Dial_Code

admin.site.register(Project)
admin.site.register(Country)
admin.site.register(Visa_Purpose)
admin.site.register(Visa)
admin.site.register(Visa_Document_Checklist)
admin.site.register(Assignment_Type)
admin.site.register(Department)
admin.site.register(Organization)
admin.site.register(Organization_Location)
admin.site.register(Vendor)
admin.site.register(Role)
admin.site.register(Assignment_Group)
admin.site.register(Request_Status)
admin.site.register(Activity_Log)
admin.site.register(Dial_Code)
