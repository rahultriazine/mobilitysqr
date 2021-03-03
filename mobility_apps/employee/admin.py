from django.contrib import admin

# Register your models here.
from mobility_apps.employee.models import Employee, Employee_Passport_Detail, Employee_Visa_Detail,Userinfo

admin.site.register(Userinfo)
admin.site.register(Employee)
admin.site.register(Employee_Passport_Detail)
admin.site.register(Employee_Visa_Detail)
