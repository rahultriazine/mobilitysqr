from django.shortcuts import render
#Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import settings
from api.models import User
from mobility_apps.master.models import Project, Vendor
from mobility_apps.employee.models import Employee,Message_Chat, Employee_Passport_Detail, Employee_Visa_Detail,Employee_Address,Employee_Emails,Employee_Phones,Employee_Nationalid,Employee_Emergency_Contact,Userinfo,Employee_Org_Info,Calender_Events,Calender_Activity
from mobility_apps.employee.serializer import EmployeeSerializers,Message_ChatSerializers, Employee_Passport_DetailSerializers, Employee_Visa_DetailSerializers,Employee_AddressSerializers,Employee_EmailsSerializers,Employee_PhonesSerializers,Employee_NationalidSerializers,Employee_Emergency_ContactSerializers,UserinfoSerializers,Employee_Org_InfoSerializers,Calender_EventsSerializers,Calender_ActivitySerializers
from mobility_apps.travel.models import Travel_Request ,Travel_Request_Details,Travel_Request_Dependent,Travel_Request_Draft ,Travel_Request_Details_Draft,Travel_Request_Dependent_Draft,Travel_Request_Action_History,Visa_Request_Action_History,Assignment_Travel_Request_Status,Assignment_Travel_Tax_Grid
from mobility_apps.travel.serializers import Travel_RequestSerializers ,Travel_Request_DetailsSerializers,Travel_Request_DependentSerializers,Travel_Request_DraftSerializers ,Travel_Request_Details_DraftSerializers,Travel_Request_Dependent_DraftSerializers,Travel_Request_Action_HistorySerializers,Visa_Request_Action_HistorySerializers,Assignment_Travel_Request_StatusSerializers,Assignment_Travel_Tax_GridSerializers
from mobility_apps.employee.serializer import *
from mobility_apps.master.models import Assignment_Group
from mobility_apps.master.serializers.assignment_group import Assignment_GroupSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
from django.core.mail import send_mail
from django.db import connection
from django.conf import settings
import pandas as pd
import uuid
import json
from mobility_apps.response_message import *
from django.contrib.auth.hashers import make_password ,check_password
import itertools
from django.db.models import Q
from collections import Counter
import pprint
from django.contrib.auth.hashers import make_password
from django.db import connection
from collections import namedtuple
from rest_framework.parsers import FileUploadParser,MultiPartParser,FormParser
from django.core.files.storage import FileSystemStorage
from datetime import date
from datetime import datetime, timedelta
from sqlalchemy import create_engine,Table, MetaData, Column, Integer
import pyodbc
import urllib
from contextlib import closing
from django.core.mail import EmailMultiAlternatives
#from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import string
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pagination import CustomPagination
from django.db.models.signals import pre_delete
import logging
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import exceptions
from mobility_apps.employee.tests import generate_access_token, generate_refresh_token
from django.db.models import F
import datetime
import jwt
from django.conf import settings
from mobility_apps.master.models import *

logger = logging.getLogger(__name__)
class employeeList(APIView):
    def get(self, request):
        # import ipdb;ipdb.set_trace()
        employees1 = Employee.objects.all()
        serializer = EmployeeSerializers(employees1, many=True)
        return Response(serializer.data)

class emoloyeeinfo(APIView):
    serializer_class = UserinfoSerializers
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        t = date.today()
        logindata={}
        recent_login=str(date.today())

        employees=Employee.objects.filter(Q(emp_code__iexact=request.data['email'])|Q(user_name__iexact=request.data['email'])).values("active_start_date","active_end_date")
        cursor = connection.cursor()

        employees_recent = Employee.objects.filter(Q(emp_code__iexact=request.data['email'])|Q(user_name__iexact=request.data['email'])).values("last_login","recent_login")
        if employees_recent:
            if not employees_recent[0]['last_login']:
                sql = "UPDATE employee_employee SET last_login='"+str(employees_recent[0]['recent_login'])+"' WHERE email='"+request.data['email']+"'"
                cursor.execute(sql)
            else:
                sql = "UPDATE employee_employee SET recent_login='" + recent_login + "' WHERE email='" + request.data[
                    'email'] + "'"
                cursor.execute(sql)
        else:
            sql = "UPDATE employee_employee SET recent_login='" +recent_login+ "' WHERE email='" + request.data['email'] + "'"
            cursor.execute(sql)
        if employees:
            if employees[0]['active_start_date']:
                if employees[0]['active_start_date'] and employees[0]['active_end_date']=="":
                    employee=Employee.objects.filter(Q(emp_code__iexact=request.data['email'])|Q(user_name__iexact=request.data['email']),active_start_date__lte=t)
                else:
                    employee=Employee.objects.filter(Q(emp_code__iexact=request.data['email'])|Q(user_name__iexact=request.data['email']),active_start_date__lte=t,active_end_date__gte=t)
            else:
                employee = Employee.objects.filter(Q(emp_code__iexact=request.data['email']) | Q(user_name__iexact=request.data['email']))
        else:
            employee=Employee.objects.filter(Q(emp_code__iexact=request.data['email'])|Q(user_name__iexact=request.data['email']))
        if employee:
            emp_serializer = EmployeeSerializers(employee,many=True)
            infoemail=emp_serializer.data[0]['emp_code']
            emp_code=emp_serializer.data[0]['emp_code']
            emp_serializer.data[0]['org_id']=emp_serializer.data[0]['organization']
            emp_serializerss = Project.objects.filter(Q(business_lead=infoemail)|Q(client_executive_lead=infoemail)|Q(expense_approver=infoemail)|Q(project_manager=infoemail))
            emp_serializersss = Travel_Request.objects.filter(Q(business_lead=infoemail)|Q(client_executive_lead=infoemail)|Q(expense_approver=infoemail)|Q(project_manager=infoemail))
            employeedeatils_serializerss = Employee.objects.filter(emp_code__iexact=emp_code).values('nationality')
            print(employeedeatils_serializerss)
            if employeedeatils_serializerss:
                emp_serializer.data[0]['home']=employeedeatils_serializerss[0]['nationality']
            else:
                emp_serializer.data[0]['home']=""
            employeeemp_serializerss = Employee.objects.filter(supervisor=infoemail)
            if emp_serializerss:
                emp_serializer.data[0]['approver']="1"
            elif employeeemp_serializerss:
                emp_serializer.data[0]['approver']="1"
            elif emp_serializersss:
                emp_serializer.data[0]['approver']="1"
            else:
                emp_serializer.data[0]['approver']="0"
            if emp_serializer.data:
                emp_serializer.data[0]['password']=""

                dict = {'massage': 'data found', 'status': True, 'data':emp_serializer.data[0]}
                return Response(dict, status=status.HTTP_200_OK)
            else:
                dict = {'massage': 'data not found', 'status': False}
                return Response(dict, status=status.HTTP_200_OK)

        else:
            dict = {'massage': 'No active account found', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)


# class emoloyeedetails(APIView):
#     serializer_class = EmployeeSerializers
#     permission_classes = (IsAuthenticated,)
#     def get(self, request):
#         employee = request.GET['employee']
#         #limits= "15"
#         #emp = Employee.objects.raw("select * from employee_userinfo where email LIKE '%"+employee+"%' or emp_code LIKE '%"+employee+"%'")
#         emp = Employee.objects.filter(Q(email__contains=employee)|Q(emp_code__contains=employee))
#         emp_serializer =EmployeeSerializers(emp,many=True)
#         if emp_serializer:
#             dict = {'massage': 'data found', 'status': True, 'data':emp_serializer.data}
#             return Response(dict, status=status.HTTP_200_OK)
#         else:
#             dict = {'massage': 'data not found', 'status': True}
#             return Response(dict, status=status.HTTP_200_OK)


class emoloyeedetails(ListCreateAPIView):
    serializer_class = EmployeeSerializers
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    def get(self, request):
        employee = request.GET['employee']
        #limits= "15"
        #emp = Employee.objects.raw("select * from employee_userinfo where email LIKE '%"+employee+"%' or emp_code LIKE '%"+employee+"%'")
        queryset = Employee.objects.filter(Q(email__contains=employee)|Q(emp_code__contains=employee)|Q(first_name__contains=employee)|Q(user_name__contains=employee),organization=request.GET['org_id'])
        print(queryset)
        #emp_serializer =EmployeeSerializers(emp,many=True)
        if queryset:
            print(queryset)
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            print(page)
            if page is not None:
                emp_serializer =EmployeeSerializers(page,many=True)
                result = self.get_paginated_response(emp_serializer.data)
                data = result.data # pagination data
            else:
                serializer = self.get_serializer(queryset, many=True)
                data = emp_serializer.data
            payload = {
                'return_code': '0000',
                'return_message': 'Success',
                'data': data
            }
            dict = {'massage': 'data found', 'status': True, 'data':data}

        else:
            dict = {'massage': 'data not found', 'status': False}
        return Response(dict, status=status.HTTP_200_OK)

class transfer_emoloyeedetails(APIView):
    serializer_class = EmployeeSerializers
    permission_classes = (IsAuthenticated,)
    def get(self, request):

        #limits= "15"
        #emp = Employee.objects.raw("select * from employee_userinfo where email LIKE '%"+employee+"%' or emp_code LIKE '%"+employee+"%'")
        travel=Travel_Request.objects.filter(travel_req_id=request.GET['travel']).values('approval_level')
        print(travel[0]['approval_level'])
        emp=""
        if travel[0]['approval_level']=="1":
           travelemp=Travel_Request.objects.filter(travel_req_id=request.GET['travel']).values('expense_approver','supervisor')
           emp=Employee.objects.filter(
               Q(email__contains=request.GET['employee'])|Q(emp_code__contains=request.GET['employee'])).exclude(
               Q(email=travelemp[0]['expense_approver'])|
               Q(email=travelemp[0]['supervisor']))

        elif travel[0]['approval_level']=="2":
           travelemp=Travel_Request.objects.filter(travel_req_id=request.GET['travel']).values('expense_approver','project_manager','supervisor')
           emp=Employee.objects.filter(
               Q(email__contains=request.GET['employee'])|Q(emp_code__contains=request.GET['employee'])).exclude(
               Q(email=travelemp[0]['expense_approver'])|Q(email=travelemp[0]['project_manager'])|
               Q(email=travelemp[0]['supervisor']))

        elif travel[0]['approval_level']=="3":
           travelemp=Travel_Request.objects.filter(travel_req_id=request.GET['travel']).values('expense_approver','project_manager','business_lead','supervisor')
           emp=Employee.objects.filter(
               Q(email__contains=request.GET['employee'])|Q(emp_code__contains=request.GET['employee'])).exclude(
               Q(email=travelemp[0]['expense_approver'])|Q(email=travelemp[0]['project_manager'])|
               Q(email=travelemp[0]['business_lead'])|Q(email=travelemp[0]['supervisor']))

        elif travel[0]['approval_level']=="4":
           travelemp=Travel_Request.objects.filter(travel_req_id=request.GET['travel']).values('expense_approver','project_manager','business_lead','client_executive_lead','supervisor')
           emp=Employee.objects.filter(
               Q(email__contains=request.GET['employee'])|Q(emp_code__contains=request.GET['employee'])).exclude(
               Q(email=travelemp[0]['expense_approver'])|Q(email=travelemp[0]['project_manager'])|
               Q(email=travelemp[0]['business_lead'])|Q(email=travelemp[0]['client_executive_lead'])|
               Q(email=travelemp[0]['supervisor']))
        emp_serializer =EmployeeSerializers(emp,many=True)
        if emp_serializer:
            dict = {'massage': 'data found', 'status': True, 'data':emp_serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'massage': 'data not found', 'status': True}
            return Response(dict, status=status.HTTP_200_OK)


class getemoloyeedata(APIView):
    serializer_class = EmployeeSerializers
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        employee = request.GET['employee']
        #emp = Employee.objects.raw("select * from employee_employee where emp_code LIKE '%"+employee+"%'")
        emp = Employee.objects.filter(Q(email__contains=employee)|Q(emp_code__contains=employee))

        emp_serializer = EmployeeSerializers(emp,many=True)
        dicts=[]
        for employees in emp_serializer.data:
            alldata={}
            emp_code=employees['emp_code']
            emp = Employee.objects.filter(emp_code__contains=emp_code)
            emp_serializers = EmployeeSerializers(emp,many=True)
            emp_serializers.data[0]['password']=""
            i=0
            for datas in emp_serializers.data:
                emp_serializers.data[i]['supervisor_name']=self.employee_name(emp_code=datas['supervisor'])
                i=i+1
            alldata['emp_info']=emp_serializers.data
            empadd = Employee_Address.objects.filter(emp_code=emp_code)
            empadd_serializer = Employee_AddressSerializers(empadd,many=True)
            alldata['emp_add']=empadd_serializer.data
            empadd = Employee_Emails.objects.filter(emp_code=emp_code)
            empemails_serializer = Employee_EmailsSerializers(empadd,many=True)
            alldata['emp_emails']=empemails_serializer.data
            empadd = Employee_Emergency_Contact.objects.filter(emp_code=emp_code)
            empemergency_serializer = Employee_Emergency_ContactSerializers(empadd,many=True)
            alldata['emp_emergency']=empemergency_serializer.data
            empadd = Employee_Phones.objects.filter(emp_code=emp_code)
            empphones_serializer = Employee_PhonesSerializers(empadd,many=True)
            alldata['emp_phones']=empphones_serializer.data
            empadd = Employee_Nationalid.objects.filter(emp_code=emp_code)
            empnational_serializer = Employee_NationalidSerializers(empadd,many=True)
            alldata['emp_national']=empnational_serializer.data
            empadd = Employee_Passport_Detail.objects.filter(emp_code=emp_code)
            emppassport_serializer = Employee_Passport_DetailSerializers(empadd,many=True)
            alldata['emp_passport']=emppassport_serializer.data
            empadd = Employee_Visa_Detail.objects.filter(emp_code=emp_code)
            empvisa_serializer = Employee_Visa_DetailSerializers(empadd,many=True)
            alldata['emp_visa']=empvisa_serializer.data
            empadd = Employee_Org_Info.objects.filter(emp_code=emp_code)
            emporg_serializer = Employee_Org_InfoSerializers(empadd,many=True)
            alldata['emp_orginfo']=emporg_serializer.data

            dicts.append(alldata)
        if dicts:
            dict = {'massage': 'data found', 'status': True, 'data':dicts}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'massage': 'data not found', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)
    def employee_name(self,emp_code):
        if emp_code:
            emp_code=Employee.objects.filter(emp_code=emp_code).values('emp_code','preferred_first_name','first_name','last_name')
            if emp_code:
                if emp_code[0]['first_name']:
                    first_name=emp_code[0]['first_name']
                else:
                    first_name=''

                if emp_code[0]['last_name']:
                    last_name=emp_code[0]['last_name']
                else:
                    last_name=""
                name=first_name+" "+last_name
            else:
                name = ""
            return name


class get_delete_update_employee(RetrieveDestroyAPIView):
    http_method_names = ['get', 'put', 'delete', 'head', 'options', 'trace']
    permission_classes = (IsAuthenticated,)
    serializer_class = EmployeeSerializers

    def get_queryset(self,id):
        try:
            employee = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            return []
        return employee
    def employee_detail_queryset(self,id):
        try:
            employee_details = Employee_Passport_Detail.objects.get(emp_code=id)
        except Employee_Passport_Detail.DoesNotExist:
            return []
        return employee_details

    def employee_visa_queryset(self,id):
        try:
            employee_details = Employee_Visa_Detail.objects.get(emp_code=id)
        except Employee_Visa_Detail.DoesNotExist:
            return []
        return employee_details

    # Get a employee
    def get(self, request):
        # import ipdb;ipdb.set_trace()
        employee = self.get_queryset(request.GET["id"])
        employee_details=self.employee_detail_queryset(request.GET["id"])
        employee_visa_queryset=self.employee_visa_queryset(request.GET["id"])
        dict={"status":True,"msg":"data found","employee_detail":"details not found","employee_visa":"visa details not found"}
        if employee:
            serializer = EmployeeSerializers(employee)
            dict["employee"]=serializer.data
            if employee_details:
                serializer2 = Employee_Passport_DetailSerializers(employee_details)
                dict["employee_detail"] = serializer2.data
            if employee_visa_queryset:
                serializer3 = Employee_Visa_DetailSerializers(employee_visa_queryset)
                dict["employee_visa"]=serializer3.data
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'status':False ,'msg': 'data Not Found'}
            return Response(dict, status=status.HTTP_404_NOT_FOUND)

    # Delete a employee
    def delete(self, request):
        employee = self.get_queryset(request.data["id"])
        if (True):  # If creator is who makes request
            try:
                employee.delete()
            except ProtectedError:
                content = {
                    'status': 'This resource is related to other active record.'
                }
                return Response(content, status=status.HTTP_423_LOCKED)
            content = {
                'status': True,
                "msg":"data deleted successfully"
            }
            return Response(content, status=status.HTTP_204_NO_CONTENT)
        else:
            content = {
                'status': 'user not found'
            }
            return Response(content, status=status.usernotfound)





class get_post_employee_info(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserinfoSerializers

    def get_queryset(self):
        employee = Userinfo.objects.all()
        return employee

    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        employee = self.get_queryset()
        emp_serializer = UserinfoSerializers(employee,many=True)
        dict = {'massage': 'data found', 'status': True, 'data':emp_serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()
        employe = Userinfo.objects.filter(
            emp_code=request.data.get('emp_code'))
        try:
            if (employe):
                serializer = UserinfoSerializers(employe, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                dict = {'massage code': '201', 'massage': 'updated successfully', 'status': True, 'data': serializer.data}
                return Response(dict, status=status.HTTP_201_CREATED)
            else:
                request.data['person_id'] = "PER" + str(uuid.uuid4().int)[:6]
                res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
                request.data['password'] = str(res)

                serializer = UserinfoSerializers(data=request.data)
                if request.data['preferred_first_name']:
                   name=request.data['preferred_first_name']
                else:
                   name=request.data['first_name']
                ctxt = {
                            'password':request.data['password'],
                            'first_name':name,
                            'user_name':request.data['user_name']

                        }


                subject, from_email, to = 'Welcome to MobilitySQR - Registration Successful', request.data['email']

                html_content = render_to_string('email/registration.html', ctxt)
                # render with dynamic value
                text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

                # create the email, and attach the HTML version as well.

                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                if serializer.is_valid():
                    serializer.save()
                    dict = {'status_code': '201', 'massage': 'successful', 'status': True, 'data': serializer.data}
                    return Response(dict, status=status.HTTP_201_CREATED)
                else:
                    dict = {'status_code': '201', 'massage': 'unsuccessful', 'status': False, 'data': serializer.errors}
                    return Response(dict, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'status_code': '200', 'massage': 'unsuccessful', 'status': False,'data':[]}
            return Response(dict, status=status.HTTP_200_OK)
        # return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def approver_name(self,email):
        if email:
            emp_code=Employee.objects.filter(email=email).values('emp_code','preferred_first_name','first_name','last_name')
            if emp_code[0]['preferred_first_name']:
                first_name=emp_code[0]['preferred_first_name']
            else:
                first_name=emp_code[0]['first_name']

            # if emp_code[0]['last_name']:
            #     last_name=emp_code[0]['last_name']
            # else:
            #     last_name=""
            name=first_name
            return name
        else:
            name=''
            return name

class get_post_employee(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmployeeSerializers

    def get_queryset(self):
        employee = Employee.objects.all()
        return employee

    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        employee = self.get_queryset()
        emp_serializer = EmployeeSerializers(employee,many=True)
        dict = {'massage': 'data found', 'status': True, 'data':emp_serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()
        employe = Employee.objects.filter(
            emp_code=request.data.get('emp_code')).first()
        print('############ emp ##########')
        print(employe)
        try:
            if (employe):
                businessemail=Employee_Emails.objects.filter(emp_code=request.data.get('emp_code'),email_type="business").values("id")

                if businessemail:
                    if businessemail[0]['id']:
                        cursor = connection.cursor()
                        sqlemails ="UPDATE employee_employee_emails SET email_address='"+request.data['email']+"' WHERE id='"+str(businessemail[0]['id'])+"'"
                        print(sqlemails)
                        cursor.execute(sqlemails)
                serializer = EmployeeSerializers(employe, data=request.data)
                if request.data.get('old_username'):
                   cursor = connection.cursor()
                   sql="UPDATE api_user SET username='"+request.data.get('user_name')+"' WHERE username='"+request.data.get('old_username')+"'"
                   cursor.execute(sql)
                   if request.data['preferred_first_name']:
                        name=request.data['preferred_first_name']
                   else:
                        name=request.data['first_name']
                   ctxt = {'first_name':name,'user_name':request.data['user_name'] }
                   subject, from_email, to = 'Updated Username','',request.data['email']
                   html_content = render_to_string('email/emailanduserupdate.html', ctxt)
                    # render with dynamic value
                   text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

                    # create the email, and attach the HTML version as well.

                   msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                   msg.attach_alternative(html_content, "text/html")
                   msg.send()
                if request.data.get('old_email'):
                   cursor = connection.cursor()
                   sql="UPDATE api_user SET email='"+request.data.get('email')+"' WHERE email='"+request.data.get('old_email')+"'"
                   cursor.execute(sql)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'massage code': '201', 'massage':  MSG_DETAILSUPDATE, 'status': True, 'data': serializer.data}
                else:

                    dict = {'massage code': '201', 'massage': 'Unsuccessfully', 'status': False, 'data': serializer.errors}
                return Response(dict, status=status.HTTP_201_CREATED)
            else:
                request.data['person_id'] = "PER" + str(uuid.uuid4().int)[:6]
                res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
                request.data['password'] = make_password(str(res))
                serializer = EmployeeSerializers(data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    if request.data['preferred_first_name']:
                        name=request.data['preferred_first_name']
                    else:
                        name=request.data['first_name']
                    ctxt = {
                                'password':request.data['password'],
                                'first_name':name,
                                'user_name':request.data['user_name']

                            }

                    subject, from_email, to = 'Welcome to MobilitySQR- Registration Successful','',request.data['email']

                    html_content = render_to_string('email/registration.html', ctxt)

                    # render with dynamic value
                    text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

                    # create the email, and attach the HTML version as well.

                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    dict = {'massage code': '201', 'massage': MSG_ADDED, 'status': True, 'data': serializer.data}
                    return Response(dict, status=status.HTTP_201_CREATED)
                else:
                    dict = {'massage code': '201', 'massage': 'unsuccessful', 'status': False, 'data': serializer.errors}
                    return Response(dict, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'massage code': 'Exception', 'massage': e, 'status': False}
            return Response(dict, status=status.HTTP_200_OK)
        # return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class get_post_employee_address(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_AddressSerializers

    def get_queryset(self):
        employee = Employee_Address.objects.all()
        return employee

    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        employee = self.get_queryset()
        emp_serializer = Employee_AddressSerializers(employee,many=True)
        dict = {'massage': 'data found', 'status': True, 'data':emp_serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()

        # employe = Employee_Address.objects.filter(
        #    emp_code=request.data[0]['emp_code'])
        dicts=[]
        for empdata in request.data:
            if empdata['update_id']:
                employee=Employee_Address.objects.filter(id=empdata['update_id']).first()
                serializer = Employee_AddressSerializers(employee,data=empdata)
                if serializer.is_valid():
                    serializer.save()
                if empdata['is_primary']==True:
                    employeess=Employee_Emergency_Contact.objects.filter(emp_code=empdata['emp_code'],isAddSameAsEmployee=True)
                    empdatas={}
                    if employeess:
                        for employees in employeess:
                            empdatas.update({"address1":empdata['address1']})
                            empdatas.update({"address2":empdata['address2']})
                            empdatas.update({"address3":empdata['address3']})
                            empdatas.update({"city":empdata['city']})
                            empdatas.update({"state":empdata['state']})
                            empdatas.update({"zip":empdata['zip']})
                            empdatas.update({"country":empdata['country']})
                            serializers = Employee_Emergency_ContactSerializers(employees,data=empdatas)
                            if serializers.is_valid():
                               serializers.save()
                dicts.append(serializer.data)
                dict = {'massage code': '201', 'massage': MSG_DETAILSUPDATE, 'status': True, 'data': dicts}
            else:
                serializer = Employee_AddressSerializers(data=empdata)
                if serializer.is_valid():
                    serializer.save()
                dicts.append(serializer.data)
                dict = {'massage code': '201', 'massage': MSG_ADDED, 'status': True, 'data': dicts}
        return Response(dict, status=status.HTTP_201_CREATED)


class get_post_employee_nationalid(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = Employee_NationalidSerializers

    def get_queryset(self):
        employee = Employee_Nationalid.objects.all()
        return employee

    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        employee = self.get_queryset()
        emp_serializer = Employee_NationalidSerializers(employee,many=True)
        dict = {'massage': 'data found', 'status': True, 'data':emp_serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()

        # employe = Employee_Address.objects.filter(
        #    emp_code=request.data[0]['emp_code'])
        dicts=[]
        for empdata in request.data:
            if empdata['update_id']:
                employee=Employee_Nationalid.objects.filter(id=empdata['update_id']).first()
                serializer = Employee_NationalidSerializers(employee,data=empdata)
                if serializer.is_valid():
                    serializer.save()
                dicts.append(serializer.data)
                dict = {'massage code': '201', 'massage': MSG_DETAILSUPDATE, 'status': True, 'data': dicts}
            else:
                serializer = Employee_NationalidSerializers(data=empdata)
                if serializer.is_valid():
                    serializer.save()
                dicts.append(serializer.data)
                dict = {'massage code': '201', 'massage': MSG_ADDED, 'status': True, 'data': dicts}
        return Response(dict, status=status.HTTP_201_CREATED)



class get_post_employee_emails(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_EmailsSerializers

    def get_queryset(self):
        employee = Employee_Emails.objects.all()
        return employee

    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        employee = self.get_queryset()
        emp_serializer = Employee_EmailsSerializers(employee,many=True)
        dict = {'massage': 'data found', 'status': True, 'data':emp_serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()

        # employe = Employee_Address.objects.filter(
        #    emp_code=request.data[0]['emp_code'])
        dicts=[]
        for empdata in request.data:
            if empdata['update_id']:
                if empdata['email_type']=="business":
                    cursor = connection.cursor()
                    sql ="UPDATE employee_employee SET email='"+empdata['email_address']+"' WHERE emp_code='"+empdata['emp_code']+"'"
                    print(sql)
                    cursor.execute(sql)
                employee=Employee_Emails.objects.filter(id=empdata['update_id']).first()
                serializer = Employee_EmailsSerializers(employee,data=empdata)
                if serializer.is_valid():
                    serializer.save()
                dicts.append(serializer.data)
                dict = {'massage code': '201', 'massage': MSG_DETAILSUPDATE, 'status': True, 'data': dicts}

            else:
                serializer = Employee_EmailsSerializers(data=empdata)
                if serializer.is_valid():
                    serializer.save()
                dicts.append(serializer.data)
                dict = {'massage code': '201', 'massage': MSG_ADDED, 'status': True, 'data': dicts}
        return Response(dict, status=status.HTTP_201_CREATED)

class get_post_employee_phoneinfo(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_PhonesSerializers

    def get_queryset(self):
        employee = Employee_Phones.objects.all()
        return employee

    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        employee = self.get_queryset()
        emp_serializer = Employee_PhonesSerializers(employee,many=True)
        dict = {'massage': 'data found', 'status': True, 'data':emp_serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()

        # employe = Employee_Address.objects.filter(
        #    emp_code=request.data[0]['emp_code'])
        dicts=[]
        for empdata in request.data:
            if empdata['update_id']:
                employee=Employee_Phones.objects.filter(id=empdata['update_id']).first()
                serializer = Employee_PhonesSerializers(employee,data=empdata)
                if serializer.is_valid():
                    serializer.save()
                dicts.append(serializer.data)
                dict = {'massage code': '201', 'massage': MSG_DETAILSUPDATE, 'status': True, 'data': dicts}
            else:
                serializer = Employee_PhonesSerializers(data=empdata)
                if serializer.is_valid():
                    serializer.save()
                dicts.append(serializer.data)
                dict = {'massage code': '201', 'massage': MSG_ADDED, 'status': True, 'data': dicts}
        return Response(dict, status=status.HTTP_201_CREATED)



class get_post_employee_emergencycontact(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_Emergency_ContactSerializers

    def get_queryset(self):
        employee = Employee_Emergency_Contact.objects.all()
        return employee

    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        employee = self.get_queryset()
        emp_serializer = Employee_Emergency_ContactSerializers(employee,many=True)
        dict = {'massage': 'data found', 'status': True, 'data':emp_serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()

        # employe = Employee_Address.objects.filter(
        #    emp_code=request.data[0]['emp_code'])
        dicts=[]
        for empdata in request.data:

            if empdata['update_id']:
                if empdata['isAddSameAsEmployee']==True:
                    emp=empdata['emp_code']
                    emp_add=Employee_Address.objects.filter(emp_code_id=emp,is_primary=True)
                    if emp_add:
                        emp_add=Employee_AddressSerializers(emp_add,many=True)
                        empdata.update({"address1":emp_add.data[0]['address1']})
                        empdata.update({"address2":emp_add.data[0]['address2']})
                        empdata.update({"address3":emp_add.data[0]['address3']})
                        empdata.update({"city":emp_add.data[0]['city']})
                        empdata.update({"state":emp_add.data[0]['state']})
                        empdata.update({"zip":emp_add.data[0]['zip']})
                        empdata.update({"country":emp_add.data[0]['country']})
                        employee=Employee_Emergency_Contact.objects.filter(id=empdata['update_id']).first()
                        serializer = Employee_Emergency_ContactSerializers(employee,data=empdata)
                        if serializer.is_valid():
                            serializer.save()
                    else:
                        employee=Employee_Emergency_Contact.objects.filter(id=empdata['update_id']).first()
                        serializer = Employee_Emergency_ContactSerializers(employee,data=empdata)
                        if serializer.is_valid():
                            serializer.save()
                else:
                    employee=Employee_Emergency_Contact.objects.filter(id=empdata['update_id']).first()
                    serializer = Employee_Emergency_ContactSerializers(employee,data=empdata)
                    if serializer.is_valid():
                        serializer.save()
                    dicts.append(serializer.data)
                dict = {'massage code': '201', 'massage': MSG_DETAILSUPDATE, 'status': True, 'data': dicts}
            else:
                if empdata['isAddSameAsEmployee']==True:
                    emp=empdata['emp_code']
                    emp_add=Employee_Address.objects.filter(emp_code_id=emp,is_primary=True)
                    if emp_add:
                        emp_add=Employee_AddressSerializers(emp_add,many=True)
                        empdata.update({"address1":emp_add.data[0]['address1']})
                        empdata.update({"address2":emp_add.data[0]['address2']})
                        empdata.update({"address3":emp_add.data[0]['address3']})
                        empdata.update({"city":emp_add.data[0]['city']})
                        empdata.update({"state":emp_add.data[0]['state']})
                        empdata.update({"zip":emp_add.data[0]['zip']})
                        empdata.update({"country":emp_add.data[0]['country']})
                serializer = Employee_Emergency_ContactSerializers(data=empdata)
                if serializer.is_valid():
                    serializer.save()
                dicts.append(serializer.data)
                dict = {'massage code': '201', 'massage': MSG_ADDED, 'status': True, 'data': dicts}
        return Response(dict, status=status.HTTP_201_CREATED)

class get_post_employee_passport(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_Passport_DetailSerializers

    def get_queryset(self):
        employee = Employee_Passport_Detail.objects.all()
        return employee

    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        employee = self.get_queryset()
        emp_serializer = Employee_Passport_DetailSerializers(employee,many=True)
        dict = {'massage': 'data found', 'status': True, 'data':emp_serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()

        # employe = Employee_Address.objects.filter(
        #    emp_code=request.data[0]['emp_code'])
        dicts=[]
        for empdata in request.data:
            if empdata['update_id']:
                employee=Employee_Passport_Detail.objects.filter(id=empdata['update_id']).first()
                serializer = Employee_Passport_DetailSerializers(employee,data=empdata)
                if serializer.is_valid():
                    serializer.save()
                dicts.append(serializer.data)
                dict = {'massage code': '201', 'massage': MSG_DETAILSUPDATE, 'status': True, 'data': dicts}

            else:
                serializer = Employee_Passport_DetailSerializers(data=empdata)
                if serializer.is_valid():
                    serializer.save()
                dicts.append(serializer.data)
                dict = {'massage code': '201', 'massage':MSG_ADDED, 'status': True, 'data': dicts}
        return Response(dict, status=status.HTTP_201_CREATED)

class get_employee_passport(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_Passport_DetailSerializers

    def get_queryset(self,emp_id):
        employee = Employee_Passport_Detail.objects.filter(emp_code_id=emp_id,isdependent=False)
        return employee

    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        employee = self.get_queryset(request.GET['emp_id'])
        emp_serializer = Employee_Passport_DetailSerializers(employee,many=True)
        dict = {'massage': 'data found', 'status': True, 'data':emp_serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

class get_post_employee_visa(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_Visa_DetailSerializers

    def get_queryset(self):
        employee = Employee_Visa_Detail.objects.all()
        return employee

    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        employee = self.get_queryset()
        emp_serializer = Employee_Visa_DetailSerializers(employee,many=True)
        dict = {'massage': 'data found', 'status': True, 'data':emp_serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()

        # employe = Employee_Address.objects.filter(
        #    emp_code=request.data[0]['emp_code'])
        dicts=[]
        for empdata in request.data:
            if empdata['update_id']:
                employee=Employee_Visa_Detail.objects.filter(id=empdata['update_id']).first()
                ##################
                if empdata['relation']=='':
                    emp=Employee_Visa_Detail.objects.filter(id=empdata['update_id']).first()
                    empdata['relation']=emp.relation
                ##############
                serializer = Employee_Visa_DetailSerializers(employee,data=empdata)
                if serializer.is_valid():
                    serializer.save()
                dicts.append(serializer.data)
                dict = {'massage code': '201', 'massage': MSG_DETAILSUPDATE, 'status': True, 'data': dicts}
            else:
                serializer = Employee_Visa_DetailSerializers(data=empdata)
                if serializer.is_valid():
                    serializer.save()
                dicts.append(serializer.data)
                dict = {'massage code': '201', 'massage': MSG_ADDED, 'status': True, 'data': dicts}
        return Response(dict, status=status.HTTP_201_CREATED)


        #
# bulk upload api(import employee)
class bulk_upload_employee(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmployeeSerializers

    # bulk upload api(import employee)
    def post(self, request):
        # try:

            data=pd.read_excel(request.data.get("file"),sheet_name=['personal_info'])
            data1=pd.read_excel(request.data.get("file"),sheet_name=['address'])
            print(data)
            df2 = pd.concat(data[frame] for frame in data.keys())
            #print(df2)
            #print(data1)
            sucessCount = 0
            failureCount = 0
            alldata=[]
            for i, value in df2.iterrows():

                employe = Employee.objects.filter(
                    emp_code=value['emp_code']).first()
                value=value.to_dict()
                #print(employe)
                if (employe):
                    test={}
                    test['empcode']=employe.emp_code
                    test['empemail']=employe.email
                    test['fcount']=failureCount
                    alldata.append(test)
                    failureCount += 1
                    continue
                else:
                    print(value)
                    sucessCount += 1
                    value['person_id'] = "PER" + str(uuid.uuid4().int)[:6]
                    serializer = EmployeeSerializers(data=value)
                    #data = value
                    if serializer.is_valid():
                        id=serializer.save().id
                        print(id)
                    else:
                        print(serializer.errors)
                    # data["emp_code"] = id
                    # emp_detail = Employee_Passport_DetailSerializers(data=data)
                    # if emp_detail.is_valid():
                    #     emp_detail.save()
                    # emp_visa_detail = Employee_Visa_DetailSerializers(data=data)
                    # if emp_visa_detail.is_valid():
                    #     emp_visa_detail.save()
                    # tests=''
                    alldata.append(serializer.data)
            data1=pd.read_excel(request.data.get("file"),sheet_name=['address'])
            df3 = pd.concat(data1[frame] for frame in data1.keys())

            alldata1=[]
            infosucessCount = 0
            infofailureCount = 0
            for i, values in df3.iterrows():
                #employess = Employee_Address.objects.filter(emp_code=values['emp_code']).first()
                values=values.to_dict()

                infosucessCount += 1
                print(values['is_primary'])
                serializer = Employee_AddressSerializers(data=values)
                if serializer.is_valid():
                    serializer.save()
                    tests=serializer.data
                else:
                    tests=serializer.errors
                alldata1.append(tests)
            dict = {'msg': 'Excel upload sucessfully', 'status': True, 'record pass personalinfo':sucessCount,'record fail':infofailureCount, 'record fail personal info':alldata , 'record fail address':alldata1}
            responseList = [dict]
            return Response(responseList, status=status.HTTP_200_OK)
        # except Exception as e:
        #     dict = {'msg': 'Excel format not be corrected', 'status': False}
        #     return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)


#Employee deatils views
class get_post_employee_details(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_Passport_DetailSerializers

    def get_queryset(self):
        employee = Employee_Passport_Detail.objects.all()
        return employee

    # Get all employee_detail
    def get(self, request):
        employee = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Employee_Passport_DetailSerializers(employee,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new employee_detail
    def post(self, request):
        employedetail = Employee_Passport_Detail.objects.filter(emp_code__id=request.data.get('id'), department__department_id=request.data.get("department_id")).first()
        if (employedetail):
            serializer = Employee_Passport_DetailSerializers(
                employedetail, data=request.data)
        else:
            serializer = Employee_Passport_DetailSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class get_post_employee_visa_details(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_Visa_DetailSerializers

    def get_queryset(self):
        employee = Employee_Visa_Detail.objects.all()
        return employee

    # Get all employee
    def get(self, request):
        #import ipdb;ipdb.set_trace()
        employee = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Employee_Visa_DetailSerializers(employee,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new employee
    def post(self, request):
        employevisadetail = Employee_Visa_Detail.objects.filter(emp_code__id=request.data.get('id'), visa_country__country_code=request.data.get('country_code')).first()
        if (employevisadetail):
            serializer = Employee_Visa_DetailSerializers(
                employevisadetail, data=request.data)
        else:
            serializer = Employee_Visa_DetailSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Employee_DetailListCreateAPIView(APIView):

    def get_queryset(self):
        employee_detail = Employee_Passport_Detail.objects.all()
        return employee_detail

    def get(self, request):

        # import ipdb;ipdb.set_trace()
        employee_detail = self.get_queryset()
        serializer = Employee_Passport_DetailSerializers(employee_detail,many=True)
        dict = {'massage': 'data found', 'status': True, 'data': serializer.data}
        #responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)



class get_post_visa_country(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_Visa_DetailSerializers

    def get_queryset(self,emp_code_id,visa_country_id,visa_type):
        try:
            criterion1 = Q(emp_code=emp_code_id)
            criterion2 = Q(country_code=visa_country_id)
            criterion3 = Q(document_type=visa_type)
            criterion4 = Q(isdependent=False)
            employee= Employee_Visa_Detail.objects.filter(criterion1&criterion2&criterion3&criterion4)
        # print(visa)
        except Employee.DoesNotExist:

            return []
        return employee

    # Get all visa_purpose
    def get(self, request):
        employee = self.get_queryset(request.GET['emp_code_id'],request.GET['visa_country_id'],request.GET['visa_type'])
        #print(employee)
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        if employee:
            serializer =Employee_Visa_DetailSerializers(employee,many=True)
            dict = {"status": True, "message":MSG_SUCESS, "data": serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {"status": False,"status_code":200, "message":MSG_FAILED}
            return Response(dict, status=status.HTTP_200_OK)




class get_post_employee_group(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Assignment_GroupSerializers
    # Get all visa_purpose
    def list(self, request):
        #queryset = list(itertools.chain(Assignment_Group.objects.all(), Employee.objects.all()))
        #data=cursor.execute('''SELECT * FROM employee_employee where email not in(select emp_email_id from master_assignment_group)''')
        queryset=Employee.objects.raw('SELECT * FROM employee_employee where email not in(select emp_email_id from master_assignment_group)')
        serializer = EmployeeSerializers(queryset, many=True)
        dict = {"status": True, "message":MSG_SUCESS, "data": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

class get_post_employee_officeaddress(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = Employee_AddressSerializers

    def get_queryset(self,emp_code):
        employee = Employee_Address.objects.filter(emp_code_id=emp_code,address_type='office')
        return employee

    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        employee = self.get_queryset(request.GET['emp_code'])
        emp_serializer = Employee_AddressSerializers(employee,many=True)
        if emp_serializer.data:
            dict = {'massage': 'data found', 'status': True, 'data':emp_serializer.data}
        else:
            dict = {'massage': 'data not found', 'status': False, 'data':emp_serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

class emoloyeedependent(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        employee = request.GET['employee']
        emp = Employee.objects.filter(emp_code=employee)

        if emp:
            emp_serializer = EmployeeSerializers(emp,many=True)
            for employees in emp_serializer.data:
                emp_code=employees['emp_code']
                empadd = Employee_Emergency_Contact.objects.filter(emp_code=emp_code,isDependent=True)
                if empadd:
                    empemergency_serializer = Employee_Emergency_ContactSerializers(empadd,many=True)
                    alldata=[]
                    for data in empemergency_serializer.data:
                        empadd = Employee_Passport_Detail.objects.filter(emp_code=data['emp_code'],relation=data['id']).exclude(passport_status=False)
                        if empadd:
                            emppassport_serializer = Employee_Passport_DetailSerializers(empadd,many=True)
                            data['emp_passport']=emppassport_serializer.data[0]
                        else:
                            data['emp_passport']=""
                        empadds = Employee_Visa_Detail.objects.filter(emp_code=data['emp_code'],relation=data['id'],country_code=request.GET['country']).exclude(is_validated=False).first()
                        if empadds:
                            empvisa_serializer = Employee_Visa_DetailSerializers(empadds)
                            data['emp_visa']=empvisa_serializer.data
                        else:
                            data['emp_visa']=""
                        alldata.append(data)
                    if alldata:
                        dict = {'massage': 'data found', 'status': True, 'data':alldata}
                    else:
                        dict = {'massage': 'data not found', 'status': False}
                else:
                    dict = {'massage': 'data not found', 'status': False}
        else:
            dict = {'massage': 'data not found', 'status': False}
        return Response(dict, status=status.HTTP_200_OK)

class emoloyee_search_info(APIView):
    serializer_class = EmployeeSerializers
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        employee = request.GET['employee']
        limits= "15"
        #emp = Employee.objects.raw("select * from employee_employee where email LIKE '%"+employee+"%' or emp_code LIKE '%"+employee+"%'  limit '"+limits+"'")
        emp = Employee.objects.filter(Q(email__contains=employee)|Q(emp_code__icontains=employee))[:10]
        emp_serializer =EmployeeSerializers(emp,many=True)
        if emp_serializer:
            dict = {'massage': 'data found', 'status': True, 'data':emp_serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'massage': 'data not found', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)


class forget_password(APIView):
    serializer_class = EmployeeSerializers
    #permission_classes = (IsAuthenticated,)
    def post(self, request):
        #username=request.data['username']
        request.data['email']=request.data['email']
        #request.data['person_id']=request.data['person_id']
        #empcode=request.data['empcode']
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
        password = str(res)
        request.data['password'] = make_password(password)
        request.data['istemporary'] = "1"
        userinfo=Employee.objects.filter(email=request.data['email']).first()
        if userinfo:
            cursor = connection.cursor()
            sql="UPDATE api_user SET password='"+request.data['password']+"' WHERE email='"+request.data['email']+"'"
            cursor1=cursor.execute(sql)
            sql1="UPDATE employee_employee SET istemporary='"+request.data['istemporary']+"' WHERE email='"+request.data['email']+"'"
            cursor2=cursor.execute(sql1)
            user_serializer = EmployeeSerializers(userinfo,data=request.data)

            if user_serializer.is_valid():
                user_serializer.save()
            usename_ = Employee.objects.filter(email=request.data['email']).values('user_name').first()
            subject = 'New Password'
            message = ''
            newpassword = '123456'
            html_message = '<h3>Your New Password:</h3>'
            html_message += '<p> Username <b>: '+usename_['user_name']+'</b> </p>'
            html_message += '<p>Temporary Password : <b>' +password+ '</b> </p>'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.data['email'],]
            sentemail=send_mail(subject, message, email_from, recipient_list, fail_silently=False, html_message=html_message)
            if sentemail:
                dict = {'massage': 'An email has been sent to reset your password', 'status': True}
                return Response(dict, status=status.HTTP_200_OK)
            else:
                dict = {'massage': 'data not found', 'status': False}
                return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'massage': 'Sorry, we do not recognize this email', 'status': False,'code':'400'}
            return Response(dict, status=status.HTTP_200_OK)


class is_termandcondtion(APIView):
    serializer_class = EmployeeSerializers
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        #username=request.data['username']
        request.data['email']=request.data['email']
        termandcondtion = request.data['termandcondtion']
        #userinfo=Employee.objects.filter(email=request.data['email']).first()
        cursor = connection.cursor()
        sql="UPDATE employee_employee SET termandcondtion='"+str(request.data['termandcondtion'])+"' WHERE user_name='"+request.data['email']+"'"
        cursor=cursor.execute(sql)
        if cursor:
            dict = {'massage': 'success', 'status': True}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'massage': 'data not found', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)

class reset_password(APIView):
    serializer_class = EmployeeSerializers
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        #username=request.data['username']
        if request.data['old_password']:
            old_password=make_password(request.data['old_password'])
            user_old = User.objects.filter(email=request.data['email']).values("password")
            user_olds=check_password(request.data['old_password'], user_old[0]['password'])
            if user_olds:
                request.data['email']=request.data['email']
                #request.data['person_id']=request.data['person_id']
                #empcode=request.data['empcode']
                passwords = make_password(request.data['password'])
                request.data['istemporary'] = "0"
                # userinfo=Userinfo.objects.filter(email=request.data['email']).first()

                cursor = connection.cursor()
                sql="UPDATE api_user SET password='"+passwords+"' WHERE email='"+request.data['email']+"'"
                cursor.execute(sql)
                cursorss="UPDATE employee_employee SET istemporary='"+request.data['istemporary']+"' WHERE email='"+request.data['email']+"'"
                cursor.execute(cursorss)
                update_result = cursor.rowcount
                # user_serializer = EmployeeSerializers(userinfo,data=request.data)
                if update_result:
                    dict = {'massage': 'success', 'status': True}

                else:
                    dict = {'massage': 'data not found', 'status': False}
            else:
                dict = {'massage': 'Old Password Does Not Match', 'status': False}
        else:
            request.data['email']=request.data['email']
            #request.data['person_id']=request.data['person_id']
            #empcode=request.data['empcode']
            passwords = make_password(request.data['password'])
            request.data['istemporary'] = "0"
            # userinfo=Userinfo.objects.filter(email=request.data['email']).first()

            cursor = connection.cursor()
            sql="UPDATE api_user SET password='"+passwords+"' WHERE email='"+request.data['email']+"'"
            cursor.execute(sql)
            cursorss = "UPDATE employee_employee SET istemporary='"+request.data['istemporary']+"' WHERE email='"+request.data['email']+"'"
            cursor.execute(cursorss)
            updated_result = cursor.rowcount
            # user_serializer = EmployeeSerializers(userinfo,data=request.data)
            if updated_result:
                dict = {'massage': 'success', 'status': True}

            else:
                dict = {'massage': 'data not found', 'status': False}
        return Response(dict, status=status.HTTP_200_OK)

class uploadDoc(APIView):
    def post(self, request, format=None):
        file = request.FILES['file']
        fil_size = file_size(request)
        if fil_size:
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_file_url = fs.url(filename)
            dict = {'massage': 'File uploaded', 'status': True, 'data': uploaded_file_url}
        else:
            dict = {'message': 'Exceeds the maximum file size 10MB', 'status': False}
        return Response(dict, status=status.HTTP_200_OK)


def file_size(request):
    if request.FILES['file'].size <= 10000000:
        result = True
    else:
        result = False
    return result


class checkemployeeuser(APIView):
    def get(self, request):
        # import ipdb;ipdb.set_trace()
        employees1 = Employee.objects.filter(user_name__iexact=request.GET['user_name'])
        if employees1:
            dict = {'massage': 'User Name Already Exist', 'status': True,'isUser':0}
        else:
            dict = {'massage': 'User Name not Available', 'status': True,'isUser':1}
        return Response(dict, status=status.HTTP_200_OK)

class checkemployeeemail(APIView):
    def get(self, request):
        # import ipdb;ipdb.set_trace()
        employees1 = Employee.objects.filter(email=request.GET['email'])
        if employees1:
            dict = {'massage': 'Email Already Exist', 'status': True}
        else:
            dict = {'massage': 'Email Available', 'status': True}
        return Response(dict, status=status.HTTP_200_OK)

class checkemployeeempcode(APIView):
    def get(self, request):
        # import ipdb;ipdb.set_trace()
        employees1 = Employee.objects.filter(emp_code=request.GET['emp_code'])
        if employees1:
            dict = {'massage': 'Employee Code Already Exist', 'status': True}
        else:
            dict = {'massage': 'Employee Code Available', 'status': True}
        return Response(dict, status=status.HTTP_200_OK)



class FileUploadView(ListCreateAPIView):
    def post(self, request):

        file_obj = request.FILES['file']
        data={"status":"true","s":str(file_obj.name)}
        xl = pd.ExcelFile(file_obj)
        #df2 = pd.concat(data[frame] for frame in data.keys())
        #personal_info = pd.read_excel(file_obj, sheet_name='personal_info')
        #print(personal_info.info())

        for idx, name in enumerate(xl.sheet_names):
            df = pd.DataFrame()

            sheet = xl.parse(name)
            if idx == 0:
              columns = sheet.columns
            #sheet.columns = columns
            #print(name)
            #cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='mobilitysqrdev.database.windows.net';DATABASE='mobilitysqrdevnew';UID='mobilitysqr_admin';PWD='mob!@sqr1123573121')
            #cursor = cnxn.cursor()
            df = df.append(sheet, ignore_index=True)
            # params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
            #                      "SERVER=mobilitysqrdev.database.windows.net;"
            #                          "DATABASE=mobilitysqrdevnew;"
            #                      "UID=mobilitysqr_admin;"
            #                      "PWD=mob!@sqr1123573121")
            sqlEngine= create_engine('postgresql+psycopg2://postgres:admin@123@172.104.183.68/mobilitysqr_staging')
            dbConnection= sqlEngine.connect()

            if name == 'personal_info':
                dataadded =  df.to_sql(con=dbConnection, name='tmp_personal_info3', if_exists='replace')
            if name == 'address':
                dataadded =  df.to_sql(con=dbConnection, name='tmp_employee_address3', if_exists='replace')
            if name == 'employee_emails':
                dataadded =  df.to_sql(con=dbConnection, name='tmp_employee_emails3', if_exists='replace')
            if name == 'employee_emergency_contact':
                dataadded =  df.to_sql(con=dbConnection, name='tmp_employee_emergency_contact3', if_exists='replace')
            if name == 'employee_phones':
                dataadded =  df.to_sql(con=dbConnection, name='tmp_employee_phones3', if_exists='replace')
            if name == 'employee_passport_detail':
                dataadded =  df.to_sql(con=dbConnection, name='tmp_employee_passport_detail', if_exists='replace')
            if name == 'employee_visa_detail':
                dataadded =  df.to_sql(con=dbConnection, name='tmp_employee_visa_detail', if_exists='replace')
            if name == 'employee_org_info':
                dataadded =  df.to_sql(con=dbConnection, name='tmp_employee_org_info', if_exists='replace')
            if name == 'employee_nationalid':
                dataadded =  df.to_sql(con=dbConnection, name='tmp_employee_nationalid', if_exists='replace')

            dbConnection.close()

        data={"df":"success","status":"true","s":str(file_obj.name)}
        return Response(data,status=status.HTTP_200_OK)

class FileUploadView2(ListCreateAPIView):
    def post(self, request):

        file_obj = request.FILES['file']
        data={"status":"true","s":str(file_obj.name)}
        xl = pd.ExcelFile(file_obj)

        for idx, name in enumerate(xl.sheet_names):
            df = pd.DataFrame()

            sheet = xl.parse(name)
            if idx == 0:
              columns = sheet.columns

            df = df.append(sheet, ignore_index=True)
            if name == 'address':
                #print(df)
                for item in df.to_dict('records'):
                    #print(item)
                    entry = Employee_AddressSerializer(data=item)
                    #print(item)
                    #item.save()
                    if entry.is_valid():
                        entry.save();
                    else :
                        entry.errors

                    #entry = Employee_AddressSerializer(item)
                    #print(entry.data)
                    #entry.save()
                #rw=Employee_AddressSerializer(row_iter,many=True);
                #print(rw.data)


            data={"df":df,"status":"true","s":str(file_obj.name)}
        return Response(data,status=status.HTTP_200_OK)

class GETData(ListCreateAPIView):
    def get(self, request):
        cursor = connection.cursor()
        sql = "select * From tmp_personal_info3"
        cursor.execute(sql)
        myresult=cursor.fetchone()

        data={"status":"true","s":myresult}
        return Response(data,status=status.HTTP_200_OK)


class get_post_employee_orginfo(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_Org_InfoSerializers

    def get_queryset(self):
        employee = Employee_Org_InfoSerializers.objects.all()
        return employee

    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        employee = self.get_queryset()
        emp_serializer = Employee_Org_InfoSerializers(employee,many=True)
        dict = {'massage': 'data found', 'status': True, 'data':emp_serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()

        # employe = Employee_Address.objects.filter(
        #    emp_code=request.data[0]['emp_code'])
        dicts=[]
        if request.data['update_id']:
            employee=Employee_Org_Info.objects.filter(id=request.data['update_id']).first()
            serializer = Employee_Org_InfoSerializers(employee,data=request.data)
            if serializer.is_valid():
                serializer.save()
            dicts.append(serializer.data)

        else:
            serializer = Employee_Org_InfoSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
            dicts.append(serializer.data)
        dict = {'massage code': '201', 'massage': MSG_DETAILSUPDATE, 'status': True, 'data': dicts}
        return Response(dict, status=status.HTTP_201_CREATED)


class import_employee(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    #serializer_class = Employee
    # Create a new employee
    def get(self, request):
        # import ipdb;ipdb.set_trace()

        # employe = Employee_Address.objects.filter(
        cursor = connection.cursor()
        class CursorByName():
            def __init__(self, cursor):
                self._cursor = cursor

            def __iter__(self):
                return self

            def __next__(self):
                row = self._cursor.__next__()
                return { description[0]: row[col] for col, description in enumerate(self._cursor.description) }

        sql ="SELECT * FROM tmp_personal_info3"
        cursor.execute(sql)

        #sql ="TRUNCATE TABLE letter_letters"tmp_personal_info3
        errordata=[]
        datas=[]
        for data in CursorByName(cursor):

            list={}
            res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))

            list['emp_code']=data['emp_code']
            list['person_id']="PER" + str(uuid.uuid4().int)[:6]
            list['role']=data['role']
            list['login_method']=data['login_method']
            list['password']=make_password(str(res))
            list['termandcondtion']='0'
            list['istemporary']='0'
            list['user_name']=data['user_name']
            list['first_name']=data['first_name']
            list['last_name']=data['last_name']
            list['middle_name']=data['middle_name']
            list['preferred_first_name']=data['preferred_first_name']
            list['preferred_last_name']=data['preferred_last_name']
            list['salutation']=data['salutation']
            list['initials']=data['initials']
            list['title']=data['title']
            list['suffix']=data['suffix']
            list['display_name']=data['display_name']
            list['formal_name']=data['formal_name']
            list['birth_name']=data['birth_name']
            list['name_prefix']=data['name_prefix']
            list['gender']=data['gender']
            list['marital_status']=data['marital_status']
            list['marital_status_since']=data['marital_status_since']
            list['country_of_birth']=data['country_of_birth']
            list['nationality']=data['nationality']
            list['second_nationality']=data['second_nationality']
            list['native_preferred_lang']=data['native_preferred_lang']
            list['partner_name']=data['partner_name']
            list['partner_name_prefix']='Mr.'
            list['note']=data['note']
            list['dob']=str(data['dob'].date())
            list['place_of_birth']=data['place_of_birth']
            list['active_start_date']=str(data['active_start_date'].date())
            list['active_end_date']=str(data['active_end_date'].date())
            list['email']=data['email']
            list['department']=data['department']
            list['role']=data['role']
            list['photo']=data['photo']
            list['organization']=data['organization']
            list['supervisor']=data['supervisor']
            datas.append(list)
        if datas:
            personal_data=[]
            for datass in datas:
                personalinfoerror={}
                employee=Employee.objects.filter(emp_code=datass['emp_code']).first()

                if employee:
                    employeeserializer=EmployeeSerializers(employee,data=datass)
                    emp_code=datass['emp_code']
                    if employeeserializer.is_valid():
                        employeeserializer.save()
                    else:
                        personalinfoerror[emp_code]=employeeserializer.errors
                else:
                    employeeserializer=EmployeeSerializers(data=datass)
                    emp_code=datass['emp_code']
                    if employeeserializer.is_valid():
                        employeeserializer.save()
                    else:
                        personalinfoerror[emp_code]=employeeserializer.errors
                        personal_data.append(personalinfoerror)
            errordata.append({'Personal_Info_Error':personal_data})

        #Emplyee Personal Info Inserted

        #Employee address insert start..

        sql ="SELECT * FROM tmp_employee_address3"
        cursor=cursor.execute(sql)
        dataaddress=[]
        for dataadd in CursorByName(cursor):

            lists={}
            lists['emp_code']=dataadd['emp_code_id']
            lists['address1']=dataadd['address1']
            lists['address2']=dataadd['address2']
            lists['address3']=dataadd['address3']
            lists['city']=dataadd['city']
            lists['state']=dataadd['state']
            lists['country']=dataadd['country']
            lists['is_primary']=dataadd['is_primary']
            dataaddress.append(lists)
        address_data=[]
        for dataad in dataaddress:
            addresserror={}
            address=Employee_AddressSerializers(data=dataad)
            emp_code=dataad['emp_code']
            if address.is_valid():
                id=address.save().id

            else:
               addresserror[emp_code]=address.errors
               address_data.append(addresserror)
        errordata.append({'Address_Errors':address_data})
        #Employee address insert start..

        #Employee emails insert start..
        sql ="SELECT * FROM tmp_employee_emails3"
        cursor=cursor.execute(sql)
        dataemails=[]
        for dataemail in CursorByName(cursor):

            listeamil={}
            listeamil['emp_code']=dataemail['emp_code_id']
            listeamil['email_type']=dataemail['email_type']
            listeamil['email_address']=dataemail['email_address']
            listeamil['is_primary']=''
            dataemails.append(listeamil)
        emails_data=[]
        for dataemailss in dataemails:
            emails_error={}
            emails=Employee_EmailsSerializers(data=dataemailss)
            emp_code=dataemailss['emp_code']
            if emails.is_valid():
               id=emails.save().id
            else:
              emails_error[emp_code]=emails.errors
              emails_data.append(emails_error)
        errordata.append({'Emails_Errors':emails_data})

        # #Employee email inserted..
        # #Employee emergency insert start..
        sql ="SELECT * FROM tmp_employee_emergency_contact3"
        cursor=cursor.execute(sql)
        dataemergencys=[]
        for dataemergency in CursorByName(cursor):
            listem={}
            listem['emp_code']=dataemergency['emp_code_id']
            listem['name']=dataemergency['name']
            listem['relationship']=dataemergency['relationship']
            listem['primary_flag']=dataemergency['primary_flag']
            listem['country_code']=dataemergency['country_code']
            listem['second_country_code']=dataemergency['second_country_code']
            listem['phone']=dataemergency['phone']
            listem['second_phone']=dataemergency['second_phone']
            listem['isDependent']=dataemergency['isDependent']
            listem['isEmergencyContact']=dataemergency['isEmergencyContact']
            listem['gender']=dataemergency['gender']
            listem['email']=dataemergency['email']
            listem['isAddSameAsEmployee']=dataemergency['isAddSameAsEmployee']
            listem['address1']=dataemergency['address1']
            listem['address2']=dataemergency['address2']
            listem['address3']=dataemergency['address3']
            listem['city']=dataemergency['city']
            listem['state']=dataemergency['state']
            listem['address_type']=dataemergency['address_type']
            listem['country']=dataemergency['country']
            listem['zip']=dataemergency['zip']
            dataemergencys.append(listem)
        emergency_data=[]
        for dataemergencyss in dataemergencys:
            emergency_contact={}
            emergency=Employee_Emergency_ContactSerializers(data=dataemergencyss)
            emp_code=dataemergencyss['emp_code']
            if emergency.is_valid():
               id=emergency.save().id
            else:
                emergency_contact[emp_code]=emergency.errors
                emergency_data.append(emergency_contact)
        errordata.append({'Emergency_Contact_Error':emergency_data})
        #Employee email inserted..

        # #Employee phone insert start..
        sql ="SELECT * FROM tmp_employee_phones3"
        cursor=cursor.execute(sql)
        dataphones=[]
        for dataphone in CursorByName(cursor):

            listp={}
            listp['emp_code']=dataphone['emp_code_id']
            listp['phone_type']=dataphone['phone_type']
            listp['country_code']=dataphone['country_code']
            listp['area_code']=dataphone['area_code']
            listp['phone_number']=dataphone['phone_number']
            listp['extension']=dataphone['extension']
            listp['isprimary']=dataphone['isprimary']
            dataphones.append(listp)
        phone_data=[]
        for dataphoness in dataphones:
            phonerror={}
            phone=Employee_PhonesSerializers(data=dataphoness)
            emp_code=dataphoness['emp_code']
            if phone.is_valid():
               id=phone.save().id
            else:
                phonerror[emp_code]=phone.errors
                phone_data.append(phonerror)
        errordata.append({'Phone':phone_data})


        # #Employee passport insert start..
        sql ="SELECT * FROM tmp_employee_passport_detail"
        cursor=cursor.execute(sql)
        datapassports=[]
        for datapassport in CursorByName(cursor):
            datapass={}
            datapass['emp_code']=datapassport['emp_code_id']
            datapass['passport_status']=datapassport['passport_status']
            datapass['passport_number']=datapassport['passport_number']
            datapass['passport_expiry_date']=str(datapassport['passport_expiry_date'])
            datapass['isdependent']=datapassport['isdependent']
            datapass['relation']=datapassport['relation']
            datapass['nationality']=datapassport['nationality']
            datapass['country_of_issue']=datapassport['country_of_issue']
            datapass['place_of_issue']=datapassport['place_of_issue']
            datapass['date_of_issue']=str(datapassport['date_of_issue'])
            datapass['date_of_expiration']=str(datapassport['date_of_expiration'])
            datapass['duplicate_passport']=datapassport['duplicate_passport']
            datapass['pages_passport']=str(datapassport['pages_passport'])
            datapass['photo']=datapassport['photo']
            datapassports.append(datapass)
        passport_data=[]
        for datapassport in datapassports:
            passporterror={}
            passport=Employee_Passport_DetailSerializers(data=datapassport)
            emp_code=datapassport['emp_code']
            if passport.is_valid():
               id=passport.save().id
            else:
                passporterror[emp_code]=passport.errors
                passport_data.append(passporterror)
        errordata.append({'Passport_Error':passport_data})
        # #Employee passport inserted..


        # #Employee visa insert start..
        sql ="SELECT * FROM tmp_employee_visa_detail"
        cursor=cursor.execute(sql)
        datavisas=[]
        for datavisa in CursorByName(cursor):
            datav={}
            issue=datavisa['issue_date'].date()
            valid=datavisa['valid_from'].date()
            expiration=datavisa['expiration_date'].date()
            datav['emp_code']=datavisa['emp_code']
            datav['country_code']=datavisa['country_code']
            datav['document_type']=datavisa['document_type']
            datav['document_title']=datavisa['document_title']
            datav['isdependent']=datavisa['isdependent']
            datav['relation']=datavisa['relation']
            datav['document_number']=datavisa['document_number']
            datav['issue_date']=str(issue)
            datav['issue_place']=datavisa['issue_place']
            datav['issuing_authority']=datavisa['issuing_authority']
            datav['expiration_date']=str(expiration)
            datav['is_validated']=datavisa['is_validated']
            datav['valid_from']=str(valid)
            datav['attachment_id']=datavisa['attachment_id']
            datavisas.append(datav)
        visas_data=[]
        for datavis in datavisas:
            visa_error={}
            visa=Employee_Visa_DetailSerializers(data=datavis)
            emp_code=datavis['emp_code']
            if visa.is_valid():
               id=visa.save().id
            else:
               visa_error[emp_code]=visa.errors
               visas_data.append(visa_error)
        errordata.append({'Visa_Error':visas_data})
        # #Employee visa inserted..


        # #Employee org insert start..
        sql ="SELECT * FROM tmp_employee_org_info"
        cursor=cursor.execute(sql)
        dataorgs=[]
        for dataorg in CursorByName(cursor):
            dataorga={}
            dataorga['emp_code']=dataorg['emp_code']
            dataorga['org1']=dataorg['org1']
            dataorga['org2']=dataorg['org2']
            dataorga['org3']=dataorg['org3']
            dataorga['org1ID']=dataorg['org1ID']
            dataorga['org2ID']=dataorg['org2ID']
            dataorga['org3ID']=dataorg['org3ID']
            dataorga['home_office_location']=dataorg['home_office_location']
            dataorga['host_office_location']=dataorg['host_office_location']
            dataorga['client_office_location']=dataorg['client_office_location']
            dataorga['home_country_designation']=dataorg['home_country_designation']
            dataorga['host_country_designation']=dataorg['host_country_designation']
            dataorgs.append(dataorga)
        org_data=[]
        for dataorg in dataorgs:
            org_error={}
            org=Employee_Org_InfoSerializers(data=dataorg)
            emp_code=dataorg['emp_code']
            if org.is_valid():
               id=org.save().id
            else:
                org_error[emp_code]=org.errors
                org_data.append(org_error)
        errordata.append({'Organization_Error':org_data})
        # #Employee org inserted..

        # #Employee visa insert start..
        sql ="SELECT * FROM tmp_employee_nationalid"
        cursor=cursor.execute(sql)
        datanationalids=[]
        for datanationalid in CursorByName(cursor):
            datanational={}
            datanational['emp_code']=datanationalid['emp_code']
            datanational['country_code']=datanationalid['country_code']
            datanational['card_type']=datanationalid['card_type']
            datanational['national_id']=datanationalid['national_id']
            datanational['attachment_id']=datanationalid['attachment_id']
            datanational['isprimary']=datanationalid['isprimary']
            datanationalids.append(datanational)
        national_data=[]
        for datanationalid in datanationalids:
            nationalid_error={}
            nationalid=Employee_NationalidSerializers(data=datanationalid)
            emp_code=datanationalid['emp_code']
            if nationalid.is_valid():
               id=nationalid.save().id
            else:
                nationalid_error[emp_code]=nationalid.errors
                national_data.append(nationalid_error)
        errordata.append({'NationalID_Error':national_data})
        #Employee visa inserted..
        logger.error(errordata)

        text_file = open("uploadpdf/error_report.txt", "w")
        text_file.write(str(errordata))

        text_file.close()
        dict = {'message':MSG_SUCESS,'status_code':200, 'status': True,'data':errordata}
        return Response(dict, status=status.HTTP_201_CREATED)


class Otp_Generate(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = EmployeeSerializers
    # Get all employee
    # import ipdb;ipdb.set_trace()
    def post(self, request):
        username=request.data.get('username')
        otp=str(uuid.uuid4().int)[:6]
        cursor = connection.cursor()
        sql ="UPDATE api_user SET otp='"+otp+"' WHERE username ILIKE '"+username+"'"
        cursor.execute(sql)
        updated_record = cursor.rowcount
        if updated_record:
            email = Employee.objects.filter(user_name__iexact=username).values("email")
            if email:
                ctxt = {
                    'OTP': otp,
                    'email': self.employee_name(email=email[0]['email'])
                }

                subject, from_email, to = 'OTP Generated Successful',"",email[0]['email']
                html_content = render_to_string('email/otp.html', ctxt)
                print(html_content)
                # render with dynamic value
                text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

                # create the email, and attach the HTML version as well.

                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                dict = {'massage': 'OTP has been sent to your email', 'status': True}
            else:
                dict = {'massage': 'Wrong username', 'status': False}
        else:
            dict = {'massage': 'Wrong username', 'status': False}
        return Response(dict, status=status.HTTP_200_OK)

    def employee_name(self,email):
        if email:
            emp_code=Employee.objects.filter(email=email).values('emp_code','preferred_first_name','first_name','last_name')
            if emp_code:
                if emp_code[0]['first_name']:
                    first_name=emp_code[0]['first_name']
                else:
                    first_name=''

                if emp_code[0]['last_name']:
                    last_name=emp_code[0]['last_name']
                else:
                    last_name=""
                name=first_name+" "+last_name
                return name
            else:
                name = " "
                return name

        else:
            name=''
            return name


class access_token(ListCreateAPIView):
        def post(self,request):
            User = get_user_model()
            username = request.data['username']
            otp = request.data['otp']
            response = Response()
            if (username is None) or (otp is None):
                dict = {'massage': 'Username and OTP required', 'status': False}
                return Response(dict, status=status.HTTP_200_OK)
            userss=User.objects.filter(username__iexact=username,otp=otp).values("id")

            if userss:
                otp=User.objects.filter(otp=otp).values("id")
                print(otp)
                if otp:
                    user=otp[0]['id']

                    access_token = generate_access_token(user)
                    refresh_token = generate_refresh_token(user)

                    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
                    response.data = {
                        'access': access_token,
                        'refresh': refresh_token,
                    }
                    return response
                else:
                    dict = {'massage': 'Wrong OTP', 'status': False}
                    return Response(dict, status=status.HTTP_200_OK)
            else:
                dict = {'massage': 'Wrong Username and OTP', 'status': False}
                return Response(dict, status=status.HTTP_200_OK)


class calender_event_get_post(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Calender_EventsSerializers

    " create clalener event"
    def post(self, request):
        serializer = Calender_EventsSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            emp_code = serializer.data['emp_code']
            if emp_code:
                calender_event_data = Calender_Events.objects.filter(emp_code=emp_code, is_visible=True, is_deleted=False)
                serializer = Calender_EventsSerializers(calender_event_data, many=True)
                dict = {'massage': 'data found', 'status': True, 'data': serializer.data}
            else:
                dict = {'massage': 'Employee code not found', 'status': False, 'data': []}

            return Response(dict, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    " get all calender event data by emp_id"
    def get(self, request, emp_code=None):
        emp_code = request.GET.get('emp_code', '')
        if (emp_code is None) or (emp_code == ''):
            dict = {'massage': 'Please send me employee code', 'status': False,'data':[]}
        else:
            calender_event_data = Calender_Events.objects.filter(emp_code_id=emp_code, is_visible=True, is_deleted=False)
            serializer = Calender_EventsSerializers(calender_event_data, many=True)
            dict = {'massage': 'data found', 'status': True, 'data': serializer.data}
        return Response(dict, status=status.HTTP_200_OK)


class calender_event_update_delete(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Calender_EventsSerializers

    def get_object(self, pk):
        return Calender_Events.objects.get(pk=pk)

    "Update calender event by id"
    def patch(self, request, pk):
        instance = self.get_object(pk)
        serializer = Calender_EventsSerializers(instance, data=request.data, partial=True)  # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            emp_code = serializer.data['emp_code']
            calender_event_data = Calender_Events.objects.filter(emp_code_id=emp_code, is_visible=True,is_deleted=False)
            serializer_data = Calender_EventsSerializers(calender_event_data, many=True)
            dict = {'massage': 'data found', 'status': True, 'data': serializer_data.data}
        else:
            dict = {'massage': 'Failed to update calender event', 'status': False}
        return Response(dict, status=status.HTTP_200_OK)


#################################################
"jwt custome login "
#################################################

class jwt_custom_login(APIView):
    serializer_class = EmployeeSerializers

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        response = Response()
        if (username is not None) and (password is not None):
            user_pass = User.objects.filter(username__iexact=username).values('password','id')
            if user_pass:
                user_data = check_password(password, user_pass[0]['password'])
                if user_data:
                    user_id = user_pass[0]['id']
                    # print(user_id)
                    # print(user_pass[0]['password'])
                    # return True
                    access_token = generate_access_token(user_id)
                    refresh_token = generate_refresh_token(user_id)
                    response.data = {"access": access_token, "refresh": refresh_token,'status': True}
                else:
                    response.data = {'massage': 'Incorrect login credentials. Please try again', 'status': False}
            else:
                response.data = {'massage': 'Incorrect login credentials. Please try again', 'status': False}
        else:
            response.data = {'massage': 'Please enter Username and Password', 'status': False}
        return response
        return response


#############################################
" get calender event api"
#############################################

class calender_activity(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Calender_ActivitySerializers

    def get(self, request):
        calender_activity = Calender_Activity.objects.filter(is_visible=True)
        serializer = Calender_ActivitySerializers(calender_activity, many=True)
        if serializer.data:
            dict = {'massage': 'data found', 'status': True, 'data': serializer.data}
        else:
            dict = {'massage': 'data not found', 'status': False, 'data': []}
        return Response(dict, status=status.HTTP_200_OK)


#################################################
" get employee information "
#################################################

class getEmployeePersonalInfo(APIView):
    serializer_class = EmployeeSerializers
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        employee = request.GET['employee']
        emp = Employee.objects.filter(Q(email__contains=employee)|Q(emp_code__contains=employee))
        emp_serializer = EmployeeSerializers(emp,many=True)
        dicts=[]
        for employees in emp_serializer.data:
            alldata={}
            emp_code=employees['emp_code']
            emp = Employee.objects.filter(emp_code__contains=emp_code)
            emp_serializers = EmployeeSerializers(emp,many=True)
            emp_serializers.data[0]['password']=""
            i=0
            for datas in emp_serializers.data:
                emp_serializers.data[i]['supervisor_name']=self.employee_name(emp_code=datas['supervisor'])
                i=i+1
        if emp_serializers.data:
            dict = {'massage': 'data found', 'status': True, 'data':emp_serializers.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'massage': 'data not found', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)
    def employee_name(self,emp_code):
        if emp_code:
            emp_code=Employee.objects.filter(emp_code=emp_code).values('emp_code','preferred_first_name','first_name','last_name')
            if emp_code:
                if emp_code[0]['first_name']:
                    first_name=emp_code[0]['first_name']
                else:
                    first_name=''

                if emp_code[0]['last_name']:
                    last_name=emp_code[0]['last_name']
                else:
                    last_name=""
                name=first_name+" "+last_name
            else:
                name = ""
            return name


#################################################
" get employee Org information "
#################################################

class getEmployeeOrgInfo(APIView):
    serializer_class = Employee_Org_InfoSerializers
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        emp_code = request.GET['employee']
        empadd = Employee_Org_Info.objects.filter(emp_code__exact=emp_code)
        emporg_serializer = Employee_Org_InfoSerializers(empadd,many=True)
        dicts = []
        if emporg_serializer.data:
            dict = {'massage': 'data found', 'status': True, 'data':emporg_serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'massage': 'data not found', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)

#################################################
" get employee address information "
#################################################

class getEmployeeAddressInfo(APIView):
    serializer_class = Employee_AddressSerializers
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        emp_code = request.GET['employee']
        empadd = Employee_Address.objects.filter(emp_code=emp_code).order_by('id')
        empadd_serializer = Employee_AddressSerializers(empadd,many=True)
        dicts = []
        if empadd_serializer.data:
            dict = {'massage': 'data found', 'status': True, 'data':empadd_serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'massage': 'data not found', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)

#################################################
" get employee Email information "
#################################################

class getEmployeeEmailInfo(APIView):
    serializer_class = Employee_EmailsSerializers
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        emp_code = request.GET['employee']
        empadd = Employee_Emails.objects.filter(emp_code=emp_code).order_by('id')
        empemails_serializer = Employee_EmailsSerializers(empadd,many=True)
        dicts = []
        if empemails_serializer.data:
            dict = {'massage': 'data found', 'status': True, 'data':empemails_serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'massage': 'data not found', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)

#################################################
" get employee phone information "
#################################################

class getEmployeePhoneInfo(APIView):
    serializer_class = Employee_PhonesSerializers
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        emp_code = request.GET['employee']
        empadd = Employee_Phones.objects.filter(emp_code=emp_code).order_by('id')
        empphones_serializer = Employee_PhonesSerializers(empadd,many=True)
        dicts = []
        if empphones_serializer.data:
            dict = {'massage': 'data found', 'status': True, 'data':empphones_serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'massage': 'data not found', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)

#################################################
" get employee national id "
#################################################

class getEmployeeNationalId(APIView):
    serializer_class = Employee_NationalidSerializers
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        emp_code = request.GET['employee']
        empadd = Employee_Nationalid.objects.filter(emp_code=emp_code).order_by('id')
        empnational_serializer = Employee_NationalidSerializers(empadd,many=True)
        dicts = []
        if empnational_serializer.data:
            dict = {'massage': 'data found', 'status': True, 'data':empnational_serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'massage': 'data not found', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)
#################################################
" get employee Emergency contact "
#################################################

class getEmployeeEmergencyContact(APIView):
    serializer_class = Employee_Emergency_ContactSerializers
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        emp_code = request.GET['employee']
        empadd = Employee_Emergency_Contact.objects.filter(emp_code=emp_code).order_by('id')
        empemergency_serializer = Employee_Emergency_ContactSerializers(empadd,many=True)
        dicts = []
        if empemergency_serializer.data:
            dict = {'massage': 'data found', 'status': True, 'data':empemergency_serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'massage': 'data not found', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)

#################################################
" get employee passport information "
#################################################

class getEmployeePassportInfo(APIView):
    serializer_class = Employee_Passport_DetailSerializers
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        emp_code = request.GET['employee']
        empadd = Employee_Passport_Detail.objects.filter(emp_code=emp_code).order_by('id')
        emppassport_serializer = Employee_Passport_DetailSerializers(empadd,many=True)
        dicts = []
        if emppassport_serializer.data:
            dict = {'massage': 'data found', 'status': True, 'data':emppassport_serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'massage': 'data not found', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)

#################################################
" get employee vissa information "
#################################################

class getEmployeeVisaInfo(APIView):
    serializer_class = Employee_Visa_DetailSerializers
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        emp_code = request.GET['employee']
        empadd = Employee_Visa_Detail.objects.filter(emp_code=emp_code).order_by('id')
        empvisa_serializer = Employee_Visa_DetailSerializers(empadd,many=True)
        dicts = []
        if empvisa_serializer.data:
            dict = {'massage': 'data found', 'status': True, 'data':empvisa_serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'massage': 'data not found', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)



##################################################
# bulk json employee add
##################################################

class bulk_json_upload_employee(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmployeeSerializers


    def post(self, request):

        dicts = []
        for empdata in request.data:

            employe = Employee.objects.filter(emp_code=empdata['emp_code']).first()
            print('############ emp ##########')
            print(employe)

            try:
                if (employe):
                    personid = Employee.objects.filter(emp_code=empdata['emp_code']).values('person_id').first()
                    # print(personid['person_id'])
                    empdata['person_id'] = personid['person_id']
                    businessemail = Employee_Emails.objects.filter(emp_code=empdata['emp_code'],
                                                                   email_type="business").values("id")
                    if businessemail:
                        if businessemail[0]['id']:
                            cursor = connection.cursor()
                            sqlemails = "UPDATE employee_employee_emails SET email_address='" + empdata[
                                'email'] + "' WHERE id='" + str(businessemail[0]['id']) + "'"
                            print(sqlemails)
                            cursor.execute(sqlemails)
                    print(empdata)
                    serializer = EmployeeSerializers(employe, data=empdata)
                    if empdata['old_username']:
                        cursor = connection.cursor()
                        sql = "UPDATE api_user SET username='" + empdata['user_name'] + "' WHERE username='" + empdata['old_username'] + "'"
                        cursor.execute(sql)
                        if empdata['preferred_first_name']:
                            name = empdata['preferred_first_name']
                        else:
                            name = empdata['first_name']
                        ctxt = {'first_name': name, 'user_name': empdata['user_name']}
                        subject, from_email, to = 'Updated Username', '', empdata['email']
                        html_content = render_to_string('email/emailanduserupdate.html', ctxt)
                        # render with dynamic value
                        text_content = strip_tags(
                            html_content)  # Strip the html tag. So people can see the pure text at least.

                        # create the email, and attach the HTML version as well.

                        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()

                    if empdata['old_email']:
                        cursor = connection.cursor()
                        sql = "UPDATE api_user SET email='" + empdata['email'] + "' WHERE email='" + empdata['old_email'] + "'"
                        cursor.execute(sql)
                    if serializer.is_valid():
                        serializer.save()
                        dict = {'massage code': '201', 'massage': 'Updated', 'status': True,
                                'emp_code': empdata['emp_code']}
                    else:
                        print(serializer.errors)
                        dict = {'massage code': '201', 'massage': 'Updated', 'status': False,
                                'emp_code': empdata['emp_code']}

                    dicts.append(dict)
                else:
                    empdata['person_id'] = "PER" + str(uuid.uuid4().int)[:6]
                    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                    empdata['password'] = make_password(str(res))
                    if empdata['supervisor'] == '':
                        empdata['supervisor'] = 'demo_supervisor_1'

                    serializer = EmployeeSerializers(data=empdata)

                    if serializer.is_valid():
                        serializer.save()
                        if empdata['preferred_first_name']:
                            name = empdata['preferred_first_name']
                        else:
                            name = empdata['first_name']
                        ctxt = {
                            'password': empdata['password'],
                            'first_name': name,
                            'user_name': empdata['user_name']

                        }

                        subject, from_email, to = 'Welcome to MobilitySQR- Registration Successful', '', empdata['email']

                        html_content = render_to_string('email/registration.html', ctxt)

                        # render with dynamic value
                        text_content = strip_tags(
                            html_content)  # Strip the html tag. So people can see the pure text at least.

                        # create the email, and attach the HTML version as well.

                        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                        dict = {'massage code': '201', 'massage': 'Insert', 'status': True,
                                'emp_code': empdata['emp_code']}
                    else:
                        dict = {'massage code': '201', 'massage': 'Insert failed', 'status': False,
                                'emp_code': empdata['emp_code']}
                    dicts.append(dict)
            except Exception as e:
                dict = {'massage code': 'Exception', 'massage': e, 'status': False,'emp_code': empdata['emp_code']}
                dicts.append(dict)
        return Response(dicts, status=status.HTTP_200_OK)



#########################################
#    bulk json upload employee org information
#########################################

class bulk_json_upload_employee_orginfo(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_Org_InfoSerializers

    def post(self, request):
        dicts=[]
        for empdata in request.data:
            employee = Employee_Org_Info.objects.filter(emp_code=empdata['emp_code']).first()
            if employee:
                serializer = Employee_Org_InfoSerializers(employee,data=empdata)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'massage code': '201', 'massage': 'Updated', 'status': True,
                            'emp_code': empdata['emp_code']}
                else:
                    dict = {'massage code': '201', 'massage': 'Updated', 'status': False,
                        'emp_code': empdata['emp_code']}
                dicts.append(dict)
            else:
                serializer = Employee_Org_InfoSerializers(data=empdata)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'massage code': '201', 'massage': 'Insert', 'status': True,
                            'emp_code': empdata['emp_code']}
                else:
                    dict = {'massage code': '201', 'massage': 'Insert', 'status': False,
                            'emp_code': empdata['emp_code']}
                dicts.append(dict)
        return Response(dicts, status=status.HTTP_201_CREATED)


###########################################
# bulk json employee address upload
###########################################

class bulk_json_upload_employee_address(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_AddressSerializers


    def post(self, request):
        dicts=[]
        for empdata in request.data:
            employee = Employee_Address.objects.filter(emp_code=empdata['emp_code']).first()
            if employee:
                serializer = Employee_AddressSerializers(employee,data=empdata)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'massage code': '201', 'massage': 'Updated', 'status': True,
                            'emp_code': empdata['emp_code']}
                else:
                    dict = {'massage code': '201', 'massage': 'Updated', 'status': False,
                            'emp_code': empdata['emp_code']}
                dicts.append(dict)
                if empdata['is_primary']==True:
                    employeess=Employee_Emergency_Contact.objects.filter(emp_code=empdata['emp_code'],isAddSameAsEmployee=True)
                    empdatas={}
                    if employeess:
                        for employees in employeess:
                            empdatas.update({"address1":empdata['address1']})
                            empdatas.update({"address2":empdata['address2']})
                            empdatas.update({"address3":empdata['address3']})
                            empdatas.update({"city":empdata['city']})
                            empdatas.update({"state":empdata['state']})
                            empdatas.update({"zip":empdata['zip']})
                            empdatas.update({"country":empdata['country']})
                            serializers = Employee_Emergency_ContactSerializers(employees,data=empdatas)
                            if serializers.is_valid():
                               serializers.save()
            else:
                serializer = Employee_AddressSerializers(data=empdata)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'massage code': '201', 'massage': 'Inserted', 'status': True,
                        'emp_code': empdata['emp_code']}
                else:
                    dict = {'massage code': '201', 'massage': 'Inserted', 'status': False,
                        'emp_code': empdata['emp_code']}
                dicts.append(dict)
        return Response(dicts, status=status.HTTP_201_CREATED)


##################################################
# bulk json upload employee email
##################################################
class bulk_json_upload_employee_emails(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_EmailsSerializers

    def post(self, request):

        dicts=[]
        for empdata in request.data:
            employee = Employee_Emails.objects.filter(emp_code=empdata['emp_code']).first()
            if employee:
                if empdata['email_type']=="business":
                    cursor = connection.cursor()
                    sql ="UPDATE employee_employee SET email='"+empdata['email_address']+"' WHERE emp_code='"+empdata['emp_code']+"'"
                    print(sql)
                    cursor.execute(sql)
                serializer = Employee_EmailsSerializers(employee,data=empdata)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'massage code': '201', 'massage': 'Updated', 'status': True,
                        'emp_code': empdata['emp_code']}
                else:
                    dict = {'massage code': '201', 'massage': 'Updated', 'status': False,
                        'emp_code': empdata['emp_code']}
                dicts.append(dict)

            else:
                serializer = Employee_EmailsSerializers(data=empdata)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'massage code': '201', 'massage': 'Inserted', 'status': True,
                        'emp_code': empdata['emp_code']}
                else:
                    dict = {'massage code': '201', 'massage': 'Inserted', 'status': False,
                        'emp_code': empdata['emp_code']}
                dicts.append(dict)
        return Response(dicts, status=status.HTTP_201_CREATED)


##############################################
#  bulk json upload employee phoneinfo
##############################################

class bulk_json_upload_phoneinfo(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_PhonesSerializers


    def post(self, request):

        dicts=[]
        for empdata in request.data:
            employee = Employee_Phones.objects.filter(emp_code=empdata['emp_code']).first()
            if employee:
                serializer = Employee_PhonesSerializers(employee,data=empdata)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'massage code': '201', 'massage': 'Updated', 'status': True,
                        'emp_code': empdata['emp_code']}
                else:
                    dict = {'massage code': '201', 'massage': 'Updated', 'status': False,
                        'emp_code': empdata['emp_code']}
                dicts.append(dict)
            else:
                serializer = Employee_PhonesSerializers(data=empdata)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'massage code': '201', 'massage': 'Inserted', 'status': True,
                        'emp_code': empdata['emp_code']}
                else:
                    dict = {'massage code': '201', 'massage': 'Inserted', 'status': False,
                        'emp_code': empdata['emp_code']}
                dicts.append(dict)
        return Response(dicts, status=status.HTTP_201_CREATED)


##########################################
#  bulk json employee emergency contact upload
##########################################


class bulk_json_upload_employee_emergencycontact(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_Emergency_ContactSerializers


    def post(self, request):

        dicts=[]
        for empdata in request.data:
            employee = Employee_Emergency_Contact.objects.filter(emp_code_id=empdata['emp_code']).first()
            if employee:
                if empdata['isAddSameAsEmployee']==True:
                    emp=empdata['emp_code']
                    emp_add=Employee_Address.objects.filter(emp_code_id=emp,is_primary=True)
                    if emp_add:
                        emp_add=Employee_AddressSerializers(emp_add,many=True)
                        empdata.update({"address1":emp_add.data[0]['address1']})
                        empdata.update({"address2":emp_add.data[0]['address2']})
                        empdata.update({"address3":emp_add.data[0]['address3']})
                        empdata.update({"city":emp_add.data[0]['city']})
                        empdata.update({"state":emp_add.data[0]['state']})
                        empdata.update({"zip":emp_add.data[0]['zip']})
                        empdata.update({"country":emp_add.data[0]['country']})
                        serializer = Employee_Emergency_ContactSerializers(employee,data=empdata)
                        if serializer.is_valid():
                            serializer.save()
                    else:
                        serializer = Employee_Emergency_ContactSerializers(employee,data=empdata)
                        if serializer.is_valid():
                            serializer.save()
                            dict = {'massage code': '201', 'massage': 'Updated', 'status': True,
                                    'emp_code': empdata['emp_code']}
                        else:
                            dict = {'massage code': '201', 'massage': 'Updated', 'status': False,
                                    'emp_code': empdata['emp_code']}
                        dicts.append(dict)
                else:
                    serializer = Employee_Emergency_ContactSerializers(employee,data=empdata)
                    if serializer.is_valid():
                        serializer.save()
                        dict = {'massage code': '201', 'massage': 'Updated', 'status': True,
                            'emp_code': empdata['emp_code']}
                    else:
                        dict = {'massage code': '201', 'massage': 'Updated', 'status': False,
                            'emp_code': empdata['emp_code']}
                    dicts.append(dict)
            else:
                if empdata['isAddSameAsEmployee']==True:
                    emp=empdata['emp_code']
                    emp_add=Employee_Address.objects.filter(emp_code_id=emp,is_primary=True)
                    if emp_add:
                        emp_add=Employee_AddressSerializers(emp_add,many=True)
                        empdata.update({"address1":emp_add.data[0]['address1']})
                        empdata.update({"address2":emp_add.data[0]['address2']})
                        empdata.update({"address3":emp_add.data[0]['address3']})
                        empdata.update({"city":emp_add.data[0]['city']})
                        empdata.update({"state":emp_add.data[0]['state']})
                        empdata.update({"zip":emp_add.data[0]['zip']})
                        empdata.update({"country":emp_add.data[0]['country']})
                serializer = Employee_Emergency_ContactSerializers(data=empdata)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'massage code': '201', 'massage': 'Inserted', 'status': True,
                        'emp_code': empdata['emp_code']}
                else:
                    dict = {'massage code': '201', 'massage': 'Inserted', 'status': False,
                        'emp_code': empdata['emp_code']}
                dicts.append(dict)
        return Response(dicts, status=status.HTTP_201_CREATED)


#################################################
#  json bulk upload employee passport
#################################################

class bulk_json_upload_employee_passport(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_Passport_DetailSerializers


    def post(self, request):

        dicts=[]
        for empdata in request.data:
            employee = Employee_Passport_Detail.objects.filter(emp_code_id=empdata['emp_code']).first()
            if employee:
                serializer = Employee_Passport_DetailSerializers(employee,data=empdata)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'massage code': '201', 'massage': 'Updated', 'status': True,
                        'emp_code': empdata['emp_code']}
                else:
                    dict = {'massage code': '201', 'massage': 'Updated', 'status': False,
                        'emp_code': empdata['emp_code']}
                dicts.append(dict)

            else:
                serializer = Employee_Passport_DetailSerializers(data=empdata)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'massage code': '201', 'massage': 'Inserted', 'status': True,
                        'emp_code': empdata['emp_code']}
                else:
                    dict = {'massage code': '201', 'massage': 'Inserted', 'status': False,
                        'emp_code': empdata['emp_code']}
                dicts.append(dict)
        return Response(dicts, status=status.HTTP_201_CREATED)



################################
# bulk json vija upload
################################

class bulk_json_upload_employee_visa(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_Visa_DetailSerializers

    def post(self, request):

        dicts=[]
        for empdata in request.data:
            employee = Employee_Visa_Detail.objects.filter(emp_code_id=empdata['emp_code']).first()
            if employee:
                serializer = Employee_Visa_DetailSerializers(employee,data=empdata)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'massage code': '201', 'massage': 'Updated', 'status': True,
                        'emp_code': empdata['emp_code']}
                else:
                    dict = {'massage code': '201', 'massage': 'Updated', 'status': False,
                        'emp_code': empdata['emp_code']}
                dicts.append(dict)
            else:
                serializer = Employee_Visa_DetailSerializers(data=empdata)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'massage code': '201', 'massage': 'Inserted', 'status': True,
                        'emp_code': empdata['emp_code']}
                else:
                    dict = {'massage code': '201', 'massage': 'Inserted', 'status': False,
                        'emp_code': empdata['emp_code']}
                dicts.append(dict)
        return Response(dicts, status=status.HTTP_201_CREATED)




##################################################
#   json bulk upload employee national id
##################################################


class bulk_json_upload_employee_nationalid(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_NationalidSerializers


    def post(self, request):

        dicts=[]
        for empdata in request.data:
            employee = Employee_Nationalid.objects.filter(emp_code_id=empdata['emp_code']).first()
            if employee:
                serializer = Employee_NationalidSerializers(employee,data=empdata)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'massage code': '201', 'massage': 'Updated', 'status': True,
                        'emp_code': empdata['emp_code']}
                else:
                    dict = {'massage code': '201', 'massage': 'Updated', 'status': False,
                        'emp_code': empdata['emp_code']}
                dicts.append(dict)
            else:
                serializer = Employee_NationalidSerializers(data=empdata)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'massage code': '201', 'massage': 'Inserted', 'status': True,
                        'emp_code': empdata['emp_code']}
                else:
                    dict = {'massage code': '201', 'massage': 'Inserted', 'status': False,
                        'emp_code': empdata['emp_code']}
                dicts.append(dict)
        return Response(dicts, status=status.HTTP_201_CREATED)



############################################
# employee chat
#############################################

class employee_chat(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Message_ChatSerializers


    def post(self, request):
        sender_emp_code = request.data.get('sender_emp_code', None)
        receiver_emp_code = request.data.get('receiver_emp_code', None)
        chat_message = request.data.get('chat_message', None)
        ticket_id = request.data.get('ticket_id', None)
        thread_data = sender_emp_code + receiver_emp_code
        thread_data1 = receiver_emp_code + sender_emp_code


        if (sender_emp_code is None) or (receiver_emp_code is None) or (chat_message is None) or (ticket_id is None) or (ticket_id == '') or (sender_emp_code == '') or (receiver_emp_code == '') or (chat_message == ''):
            dict = {'message code': '201', 'status': False,
                    'message': 'Message sender emp id, receiver emp id, ticket id and message required'}
        else:
            checkThread = Message_Chat.objects.filter(Q(thread=thread_data) | Q(thread=thread_data1),ticket_id=ticket_id).values('thread').distinct()
            if checkThread:
                message_data = Message_Chat()
                message_data.thread = checkThread[0]['thread']
                message_data.sender_emp_code = sender_emp_code
                message_data.receiver_emp_code = receiver_emp_code
                message_data.chat_message = chat_message
                message_data.ticket_id = ticket_id
                message_data.save()
                result_data = Message_Chat.objects.get(pk=message_data.id)
                serializer = Message_ChatSerializers(result_data)
            else:
                message_data = Message_Chat()
                message_data.thread = thread_data
                message_data.sender_emp_code = sender_emp_code
                message_data.receiver_emp_code = receiver_emp_code
                message_data.chat_message = chat_message
                message_data.ticket_id = ticket_id
                message_data.save()
                result_data = Message_Chat.objects.get(pk=message_data.id)
                serializer = Message_ChatSerializers(result_data)

            if serializer.data:
                dict = {'message code': '201', 'status': True, 'data': serializer.data}
            else:
                dict = {'message code': '201', 'status': F, 'data': serializer.errors}

            return Response(dict, status=status.HTTP_201_CREATED)
        return Response(dict, status=status.HTTP_201_CREATED)


    def get(self, request):
        sender_emp_code = request.GET['sender_emp_code']
        receiver_emp_code = request.GET['receiver_emp_code']
        ticket_id = request.GET['ticket_id']
        thread_data = sender_emp_code + receiver_emp_code
        thread_data1 = receiver_emp_code + sender_emp_code


        if (sender_emp_code is None) or (receiver_emp_code is None) or (ticket_id is None) or (ticket_id == '') or (sender_emp_code == '') or (receiver_emp_code == ''):
            dict = {'message code': '201', 'status': True,
                    'message': 'Message sender emp id, receiver emp id, ticket id and message required'}

        else:
            checkThread = Message_Chat.objects.filter(Q(thread=thread_data) | Q(thread=thread_data1),
                                                      ticket_id=ticket_id).values('thread').distinct()
            if checkThread:
                thr_id = checkThread[0]['thread']
                message_query = Message_Chat.objects.filter(thread=thr_id, ticket_id=ticket_id).order_by('created_date')
                serializer = Message_ChatSerializers(message_query, many=True)
                if serializer.data:
                    dict = {'massage': 'data found', 'status': True, 'data': serializer.data}
                else:
                    dict = {'massage': 'data not found', 'status': False, 'data': []}
            else:
                dict = {'massage': 'Thread not found', 'status': False, 'data':[]}
            return Response(dict, status=status.HTTP_200_OK)
        return Response(dict, status=status.HTTP_200_OK)


class get_post_employee_address(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Employee_Address_VendorSerializers

    # Get all department
    def get(self, request):
        # org_id = self.request.GET.get('org_id',None)
        emp_address = Employee_Address_Vendor.objects.all().order_by('id')
        serializer = Employee_Address_VendorSerializers(emp_address,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = Employee_Address_VendorSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict = {"status": True,  "message": 'Successfully inserted', "data": serializer.data}
        else:
            dict = {"status": False, "message": 'Failed to insert data', "data": serializer.errors}
        return Response(dict, status=status.HTTP_200_OK)
