from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.master.models import Approval_Hierarchy ,Request_Approvals,Status_Master
from mobility_apps.employee.models import Employee
from mobility_apps.employee.serializer import EmployeeSerializers
from mobility_apps.master.models import Project
from mobility_apps.visa.models import Visa_Request , Visa_Request_Document,Visa_Request_Draft
from mobility_apps.visa.serializers import Visa_RequestSerializers,Visa_Request_DocumentSerializers,Visa_Request_DraftSerializers
from mobility_apps.travel.models import Travel_Request ,Travel_Request_Details,Travel_Request_Dependent,Travel_Request_Draft ,Travel_Request_Details_Draft,Travel_Request_Dependent_Draft,Travel_Request_Action_History,Visa_Request_Action_History,Assignment_Travel_Request_Status,Assignment_Travel_Tax_Grid
from mobility_apps.travel.serializers import Travel_RequestSerializers ,Travel_Request_DetailsSerializers,Travel_Request_DependentSerializers,Travel_Request_DraftSerializers ,Travel_Request_Details_DraftSerializers,Travel_Request_Dependent_DraftSerializers,Travel_Request_Action_HistorySerializers,Visa_Request_Action_HistorySerializers,Assignment_Travel_Request_StatusSerializers,Assignment_Travel_Tax_GridSerializers
from mobility_apps.master.models import Country,City,Per_Diem,Dial_Code,Country_Master,State_Master,Location_Master,Taxgrid_Master,Taxgrid_Country,Taxgrid,National_Id
from mobility_apps.master.models import Notification
from mobility_apps.master.serializers.notification import NotificationSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from django.core.mail import send_mail
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
from django.core.mail import send_mail
from django.conf import settings
#import pandas as pd
from mobility_apps.response_message import *
import pprint
import uuid
from datetime import datetime,date
from collections import Counter
from django.db.models import Q, Count
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from dateutil import tz
from cryptography.fernet import Fernet
from pagination import CustomPagination
import string
import random
class get_delete_update_travel_request(RetrieveDestroyAPIView):
    http_method_names = ['get', 'put', 'delete', 'head', 'options', 'trace']
    #permission_classes = (IsAuthenticated,)
    serializer_class = Travel_RequestSerializers

    def get_queryset(self, pk):
        try:
            travel_tequest = Travel_Request.objects.get(pk=self.kwargs['pk'])
        except travel_tequest.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return travel_tequest

    # Get a Visa
    def get(self, request, pk):
        Travel_Request = self.get_queryset(pk)
        serializer = Travel_RequestSerializers(Travel_Request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Delete a Visa
    def delete(self, request, pk):
        Travel_Request = self.get_queryset(pk)

        if (True):  # If creator is who makes request
            try:
                Travel_Request.delete()
            except ProtectedError:
                content = {
                    'status': 'This resource is related to other active record.'
                }
                return Response(content, status=status.HTTP_423_LOCKED)
            content = {
                'status': 'NO CONTENT'
            }
            return Response(content, status=status.HTTP_204_NO_CONTENT)
        else:
            content = {
                'status': 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)



class get_post_travel_request(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Travel_RequestSerializers
    # pagination_class = CustomPagination

    def get_queryset(self,emp_email,travel_req_status,org_id):
        try:
            if travel_req_status:
                travel_request= Travel_Request.objects.filter(emp_email=emp_email,travel_req_status=travel_req_status,organization_id=org_id).order_by('-date_modified')
                # if travel_request:
                #     queryset = self.filter_queryset(travel_request)
                #     page = self.paginate_queryset(queryset)
                #     if page is not None:
                #         serializer = self.get_serializer(page, many=True)
                #         result = self.get_paginated_response(serializer.data)
                #         data = result.data  # pagination data
                #     else:
                #         serializer = self.get_serializer(queryset, many=True)
                #         data = serializer.data
                #     dict = {"status": True, "Message": MSG_SUCESS, "data": data}
                # else:
                #     dict = {'status': "False", 'Message': MSG_FAILED}
                # # return Response(dict, status=status.HTTP_200_OK)
                # print(data)
                # return data
            else:
                travel_request= Travel_Request.objects.filter(emp_email=emp_email,organization_id=org_id).order_by('-date_modified')
        # print(visa)
        except Travel_Request.DoesNotExist:

            return []
        return travel_request


    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        travel_request = self.get_queryset(request.GET["emp_email"],request.GET["travel_req_status"],request.GET["org_id"])

        alldata=[]
        for data in travel_request:
            travel_requests=Travel_Request.objects.filter(travel_req_id=data)
            travel_requests = Travel_RequestSerializers(travel_requests,many=True)
            emp_code=Employee.objects.filter(emp_code=travel_requests.data[0]['emp_email']).values('emp_code','first_name','last_name')
            if emp_code[0]['emp_code']:
                travel_requests.data[0]['emp_code']=emp_code[0]['emp_code']
            else:
                travel_requests.data[0]['emp_codess']=""
            if emp_code[0]['first_name']:
                travel_requests.data[0]['first_name']=emp_code[0]['first_name']
            else:
                travel_requests.data[0]['first_name']=""

            if emp_code[0]['last_name']:
                travel_requests.data[0]['last_name']=emp_code[0]['last_name']
            else:
                travel_requests.data[0]['last_name']=""
            emp_codes=Employee.objects.filter(emp_code=travel_requests.data[0]['current_ticket_owner']).values('email')
            if emp_codes:
                travel_requests.data[0]['current_ticket_owner']=emp_codes[0]['email']
            else:
                travel_requests.data[0]['current_ticket_owner']=""
            visa_requests=Visa_Request.objects.filter(travel_req_id=data).values("visa_req_id")
            travel_requests.data[0]['visa_requests']=visa_requests
            travel_request_details=Travel_Request_Details.objects.filter(travel_req_id_id=data).values('id','travel_req_id_id','travelling_country', 'travelling_country_to','office_location','client_number','organization','source_city','destination_city','departure_date','return_date','is_accmodation_required','accmodation_start_date','accmodation_end_date','travel_purpose','assignment_type','applicable_visa','visa_number','visa_expiry_date','host_hr_name','host_country_head','host_attorney','host_phone_no','is_client_location','client_name','client_address','hotel_cost','per_diem_cost','airfare_cost','transportation_cost','total_cost','travel_request_status','travel_request_status_notes','is_dependent',)
            #print(travel_request_details)
            #travel_request_detail_serializers=Travel_RequestSerializers(travel_request_details,many=True)
            travel_requests.data[0]['details']=travel_request_details
            travel_request_dependent=Travel_Request_Dependent.objects.filter(travel_req_id_id=travel_requests.data[0]['travel_req_id'])
            travel_request_dependent=Travel_Request_DependentSerializers(travel_request_dependent,many=True)
            travel_requests.data[0]['dependent']=travel_request_dependent.data
            alldata.append(travel_requests.data[0])
        dict = {'massage': 'data found', 'status': True, 'data': alldata}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)
    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()
        travel_request= request.data['travel_req_id']
        print(request.data)
        
        if travel_request:
            travel_request_id=Travel_Request.objects.filter(travel_req_id=request.data.get('travel_req_id')).first()
            serializer = Travel_RequestSerializers(travel_request_id,data=request.data)
            data = request.data.copy()
            if serializer.is_valid():
                serializer.save()
            travel=Travel_Request_Details.objects.filter(travel_req_id_id=request.data['travel_req_id'])
            travel.delete()
            travel=Travel_Request_Dependent.objects.filter(travel_req_id_id=request.data['travel_req_id'])
            travel.delete()
            for data in data['travel_city']:
                #travel=Travel_Request_Details_Draft.objects.filter(travel_req_id_id=request.data['travel_req_id'])
                #travel.delete()
                data["travel_req_id"] = request.data['travel_req_id']
                travel_request_detail = Travel_Request_DetailsSerializers(data=data)
                if travel_request_detail.is_valid():
                    travel_request_detail.save()
                for data in data['dependentData']:
                    data["travel_req_id"] = request.data['travel_req_id']
                    travel_request_dependent = Travel_Request_DependentSerializers(data=data)
                    if travel_request_dependent.is_valid():
                        travel_request_dependent.save()
            visa=Visa_Request.objects.filter(travel_req_id=request.data['travel_req_id'])
            visa.delete()
            for data in request.data['travel_visa']:
                epoch=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                dt=str(epoch).replace(' ','')
                data['visa_req_id']="VR"+str(uuid.uuid4().int)[:6]
                data["travel_req_id"]= request.data['travel_req_id']
                visa_request = Visa_RequestSerializers(data=data)
                if visa_request.is_valid():
                    visa_req_id=visa_request.save().visa_req_id
                dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data':  request.data['travel_req_id']}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            alldata=[]
            epoch=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dt=str(epoch).replace(' ','')
            dt=str(dt).replace('-','')
            notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
            request.data['travel_req_id']="TR"+str(uuid.uuid4().int)[:6]
            request.data['approval_level']="0"
            employee=Project.objects.filter(pid=request.data['project']).values('business_lead','project_manager','expense_approver','client_executive_lead')
            supervisor=Employee.objects.filter(emp_code=request.data['emp_email']).values('supervisor')
            print(supervisor)
            if supervisor:
                request.data['supervisor']=supervisor[0]['supervisor']
            else:
                request.data['supervisor']=""
            if employee:
                request.data['business_lead']=employee[0]['business_lead']
                request.data['project_manager']=employee[0]['project_manager']
                request.data['expense_approver']=employee[0]['expense_approver']
                request.data['client_executive_lead']=employee[0]['client_executive_lead']
            else:
                request.data['business_lead']=""
                request.data['project_manager']=""
                request.data['expense_approver']=""
                request.data['client_executive_lead']=""
            #print(request.data['client_executive_lead'])
            curerent_status =""
            if  request.data['supervisor'] !="":
            
                curerent_status = supervisor[0]['supervisor']
            elif  request.data['expense_approver'] !="":
                curerent_status = employee[0]['expense_approver']
            elif request.data['project_manager'] !="":
                curerent_status =employee[0]['project_manager']
            elif request.data['business_lead'] !="":
                curerent_status =employee[0]['business_lead']
            elif request.data['client_executive_lead'] !="":
                curerent_status =employee[0]['client_executive_lead']
            request.data['current_ticket_owner']=curerent_status
            request.data['travel_req_status']="2"
            serializer =Travel_RequestSerializers(data=request.data)
            data=request.data.copy()
            if serializer.is_valid():
                travel_id=serializer.save().travel_req_id
                print(travel_id)
                request.data['Entity_Type']="Travel"
                request.data['Entity_ID']=travel_id
                request.data['Action_taken_by']=curerent_status
                request.data['Notification_Date']=""
                request.data['Message']=travel_id+" New travel request for approval"
                request.data['Notification_ID']=notificationid
                serializernotification = NotificationSerializers(data=request.data)
                if serializernotification.is_valid():
                    serializernotification.save()
                    costst=request.data['expence_estimatedCost']+" "+request.data['expence_cureency']
                    if request.data['is_billable']==True:
                            is_billable='Yes'
                    else:
                        is_billable='No'
                    ctxt = {
                        'first_name': self.approver_name(emp_code=request.data['emp_email']),
                        'approve_first_name':self.approver_name(emp_code=request.data['Action_taken_by']),
                        'project_id': request.data['project'],
                        'billable': is_billable,
                        'from_country':request.data['expence_fromCountry'],
                        'to_country':request.data['expence_toCountry'],
                        'departure_date':request.data['expence_departureDate'],
                        'return_date':request.data['expence_returnDate'],
                        'total_cost_master_currency':costst,
                        'supervisor':self.employee_name(emp_code=supervisor[0]['supervisor']),
                        'expense_approver':self.employee_name(emp_code=employee[0]['expense_approver']),
                        'project_manager': self.employee_name(emp_code=employee[0]['project_manager']),
                        'business_lead':self.employee_name(emp_code=employee[0]['business_lead']),
                        'client_executive_lead':self.employee_name(emp_code=employee[0]['client_executive_lead'])

                    }

                    # " create custom token for mail"
                    # custom_data = {
                    #     'travel_id':travel_id,
                    #     'org': request.data['organization']
                    # }
                    custom_data = approved_Reject_Travel_get_data(travel_id,request.data['organization'])
                    ctxt = {'custom_token': encryptDtata(str(custom_data))}


                    template='email/approve_travel_request.html'
                    emptemail=self.approver_name(emp_code=request.data['emp_email'])
                    emailsubject='Travel request for '+emptemail+' requires approval'
                    print(request.data['Action_taken_by'])
                    self.sendmails(ctxt,template,emailsubject,emailto=request.data['Action_taken_by'],id=request.data['travel_req_id'])
                    if request.data['emp_email']:
                        template='email/newtravel_request.html'
                        emailsubject='Your travel request '+request.data['travel_req_id']+' has been submitted for approval'
                        self.sendmails(ctxt,template,emailsubject,emailto=request.data['emp_email'],id=request.data['travel_req_id'])
                alldata.append(travel_id)
            else:
                print(serializer.errors)
                dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data': serializer.errors}
            for data in data['travel_city']:
                data["travel_req_id"] = travel_id
                travel_request_detail = Travel_Request_DetailsSerializers(data=data)
                if travel_request_detail.is_valid():
                    travel_request_detail.save()
                else:
                    #print(travel_request_detail.errors)
                    dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data': travel_request_detail.errors}
                for data in data['dependentData']:
                    data["travel_req_id"] = request.data['travel_req_id']
                    travel_request_dependent = Travel_Request_DependentSerializers(data=data)
                    if travel_request_dependent.is_valid():
                        travel_request_dependent.save()
                    else:
                        dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data': travel_request_dependent.errors}
            for data in request.data['travel_visa']:
                epoch=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                dt=str(epoch).replace(' ','')
                notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                data['visa_req_id']="VR"+str(uuid.uuid4().int)[:6]
                data["travel_req_id"]=travel_id
                data['supervisor']=supervisor[0]['supervisor']
                data['business_lead']=employee[0]['business_lead']
                data['project_manager']=employee[0]['project_manager']
                data['expense_approver']=employee[0]['expense_approver']
                data['client_executive_lead']=employee[0]['client_executive_lead']
                data['visa_status']="2"
                curerent_vstatus =""
                if  data['supervisor'] !="":
                    curerent_vstatus = supervisor[0]['supervisor']
                elif data['project_manager'] !="":
                    curerent_vstatus =employee[0]['project_manager']
                elif data['project_manager'] !="":
                    curerent_vstatus =employee[0]['project_manager']
                elif data['business_lead'] !="":
                    curerent_vstatus =employee[0]['business_lead']
                elif data['client_executive_lead'] !="":
                    curerent_vstatus =employee[0]['client_executive_lead']
                data['current_ticket_owner']=curerent_vstatus
                visa_request = Visa_RequestSerializers(data=data)
                if visa_request.is_valid():
                    visa_req_id=visa_request.save().visa_req_id
                    request.data['Entity_Type']="Visa"
                    request.data['Entity_ID']=visa_req_id
                    request.data['Action_taken_by']=curerent_vstatus
                    request.data['Notification_Date']=""
                    request.data['Message']=visa_req_id+" New visa request for approval"
                    request.data['Notification_ID']=notificationid
                    serializernotification = NotificationSerializers(data=request.data)
                    if serializernotification.is_valid():
                        serializernotification.save()
                        costst=request.data['expence_estimatedCost']+request.data['expence_cureency']
                        if request.data['is_billable']==True:
                            is_billable='Yes'
                        else:
                            is_billable='No'
                        country=Country_Master.objects.filter(country_id=data['country']).values("name")
                        x=self.date_format(date=data['travel_start_date'])
                        y=self.date_format(date=data['travel_end_date'])
                        ctxt = {
                            'first_name': self.approver_name(emp_code=request.data['emp_email']),
                            'approve_first_name':self.approver_name(emp_code=request.data['Action_taken_by']),
                            'project_id': request.data['project'],
                            'billable': is_billable,
                            'to_country':country[0]['name'],
                            'from_date':x,
                            'return_date':y,
                            'visa_type':data['applied_visa'],
                            'supervisor':self.employee_name(emp_code=supervisor[0]['supervisor']),
                            'expense_approver':self.employee_name(emp_code=employee[0]['expense_approver']),
                            'project_manager': self.employee_name(emp_code=employee[0]['project_manager']),
                            'business_lead':self.employee_name(emp_code=employee[0]['business_lead']),
                            'client_executive_lead':self.employee_name(emp_code=employee[0]['client_executive_lead'])

                        }
                        template='email/approve_visa_request.html'
                        emptemail=self.approver_name(emp_code=request.data['emp_email'])
                        emailsubject='Visa request for '+emptemail+' requires approval'
                        self.sendmails(ctxt,template,emailsubject,emailto=request.data['Action_taken_by'],id=visa_req_id)
                    if request.data['emp_email']:
                        template='email/newvisa_request.html'
                        emailsubject='Your Visa request '+visa_req_id+' has been submitted for approval'
                        self.sendmails(ctxt,template,emailsubject,emailto=request.data['emp_email'],id=visa_req_id)
                    alldata.append(visa_req_id)
                else:
                    dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data': visa_request.errors}
            dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data': alldata}
        return Response(dict, status=status.HTTP_200_OK)
        # except Exception as e:
        #     print(e)
        #     dict = {'massage code': 'already exists', 'massage': 'unsuccessful', 'status': False}
        #     return Response(dict, status=status.HTTP_200_OK)


    def sendmails(self,ctxt,template,emailsubject,emailto,id):
        #Action_taken_by=Action_taken_by
        #"rahulr@triazinesoft.com"
        ctxt = ctxt
        template=template
        travel_req_id=id
        emailsubject=emailsubject
        emp_code=Employee.objects.filter(emp_code=emailto).values('email','preferred_first_name','first_name','last_name')
        if emp_code[0]['email']:
            toemail=emp_code[0]['email']
        else:
            toemail=""
        print(toemail)
        subject, from_email, to = emailsubject,'',toemail
        print(toemail)
        html_content = render_to_string(template, ctxt)
        print(html_content)
        # render with dynamic value
        text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

        # create the email, and attach the HTML version as well.

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


    def approver_name(self,emp_code):
        if emp_code:
            emp_code=Employee.objects.filter(emp_code=emp_code).values('emp_code','preferred_first_name','first_name','last_name')
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
    
    def employee_name(self,emp_code):
        if emp_code:
            emp_code=Employee.objects.filter(emp_code=emp_code).values('emp_code','preferred_first_name','first_name','last_name')
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
            name=''
            return name
    
    def date_format(self,date):
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        date=date
        # utc = datetime.utcnow()
        utc = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        # Tell the datetime object that it's in UTC time zone since 
        # datetime objects are 'naive' by default
        utc = utc.replace(tzinfo=from_zone)
        # Convert time zone
        central = utc.astimezone(to_zone)
        string=str(central)
        demo= string[0:10].split("-")
        new_case_date = demo[2]+"/"+demo[1]+"/"+demo[0]
        return new_case_date

    
        
class get_count_travel_request(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Travel_RequestSerializers

    def get_queryset(self,travel_req_status,emp_email,org_id,pid):
        try:
            travel= Travel_Request.objects.filter(travel_req_status=travel_req_status,emp_email_id=emp_email,organization_id=org_id,project_id=pid)

        except Travel_Request.DoesNotExist:
            return []
        return travel

    # Get all visa_purpose
    def get(self, request):
        if request.GET['travel_req_status']=="all":
            travel=Travel_Request.objects.filter(emp_email_id=request.GET['emp_email'],organization_id=request.GET['org_id'],project_id=request.GET['pid'])
        else:
            travel = self.get_queryset(request.GET['travel_req_status'],request.GET['emp_email'],request.GET['org_id'],request.GET['pid'])
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        if travel:
            serializer =Travel_RequestSerializers(travel,many=True)
            dict = {"status": True, "message":MSG_SUCESS, "data": serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {"status": False,"status_code":200, "message":MSG_FAILED}
            return Response(dict, status=status.HTTP_200_OK)

class get_org_travel_request(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Travel_RequestSerializers

    def get_queryset(self,travel_req_status,current_ticket_email,org_id):
        try:
            if current_ticket_email:
               travel_request= Travel_Request.objects.filter(current_ticket_owner=current_ticket_email,travel_req_status=travel_req_status,organization_id=org_id).values("travel_req_id").order_by('-date_modified')
            else:
               travel_request= Travel_Request.objects.filter(current_ticket_owner="",travel_req_status=travel_req_status,organization_id=org_id).values("travel_req_id").order_by('-date_modified')
        except Travel_Request.DoesNotExist:
            return []
        return travel_request

    # Get all visa_purpose
    def get(self, request):
        travel_request = self.get_queryset(request.GET["travel_req_status"],request.GET['current_ticket_email'],request.GET["org_id"])
        alldata=[]
        print(travel_request)
        if travel_request:
            for data in travel_request:
                travel_request=Travel_Request.objects.filter(travel_req_id=data['travel_req_id'])
                travel_requests = Travel_RequestSerializers(travel_request,many=True)
                emp_code=Employee.objects.filter(emp_code=travel_requests.data[0]['emp_email']).values('emp_code','first_name','last_name')
                if emp_code[0]['emp_code']:
                    travel_requests.data[0]['emp_code']=emp_code[0]['emp_code']
                else:
                    travel_requests.data[0]['emp_code']=""
                if emp_code[0]['first_name']:
                    travel_requests.data[0]['first_name']=emp_code[0]['first_name']
                else:
                    travel_requests.data[0]['first_name']=""

                if emp_code[0]['last_name']:
                    travel_requests.data[0]['last_name']=emp_code[0]['last_name']
                else:
                    travel_requests.data[0]['last_name']=""
                emp_codes=Employee.objects.filter(emp_code=travel_requests.data[0]['current_ticket_owner']).values('email','first_name','last_name')
                if emp_codes:
                    travel_requests.data[0]['current_ticket_owner']=emp_codes[0]['email']
                else:
                    travel_requests.data[0]['current_ticket_owner']=""
                visa_requests=Visa_Request.objects.filter(travel_req_id=data['travel_req_id']).values("visa_req_id")
                travel_requests.data[0]['visa_requests']=visa_requests
                travel_request_detail=Travel_Request_Details.objects.filter(travel_req_id=travel_requests.data[0]['travel_req_id']).values('id','travel_req_id_id','travelling_country', 'travelling_country_to','office_location','client_number','organization','source_city','destination_city','departure_date','return_date','is_accmodation_required','accmodation_start_date','accmodation_end_date','travel_purpose','assignment_type','applicable_visa','visa_number','visa_expiry_date','host_hr_name','host_country_head','host_attorney','host_phone_no','is_client_location','client_name','client_address','hotel_cost','per_diem_cost','airfare_cost','transportation_cost','total_cost','travel_request_status','travel_request_status_notes','is_dependent',)
                #travel_request_detail=Travel_RequestSerializers(travel_request_detail,many=True)
                travel_requests.data[0]['details']=travel_request_detail
                travel_request_dependent=Travel_Request_Dependent.objects.filter(travel_req_id=travel_requests.data[0]['travel_req_id'])
                travel_request_dependent=Travel_Request_DependentSerializers(travel_request_dependent,many=True)
                travel_requests.data[0]['dependent']=travel_request_dependent.data
                alldata.append(travel_requests.data[0])
            dict = {'massage': 'data found', 'status': True, 'data': alldata}
            # responseList = [dict]
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {"status": False,"status_code":200, "message":"Data Not Found",'data':[]}
            return Response(dict, status=status.HTTP_200_OK)


class get_count_travel_requests(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Travel_RequestSerializers
    # Get all visa_purpose
    def get(self, request):
        travel= Travel_Request.objects.filter(Q(travel_req_status="2")|Q(travel_req_status="3")|Q(travel_req_status="5"),current_ticket_owner=request.GET['assignment_email'],organization_id=request.GET['org_id'])
        travels= Travel_Request.objects.filter(travel_req_status="2",current_ticket_owner="",organization_id=request.GET['org_id']).count()
        if travel or travels:
            serializer =Travel_RequestSerializers(travels,many=True)
            serializer =Travel_RequestSerializers(travel,many=True)
            dict=[]
            for data in serializer.data:
                dict.append(data['travel_req_status'])
            total=sum(Counter(dict).values())
            my_dict = Counter(dict)
            dict = {"status": True, "message":MSG_SUCESS, "data":  my_dict,"new_request":travels}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {"status": False,"status_code":200, "message":MSG_FAILED,"data":  travel,"new_request":travels}
            return Response(dict, status=status.HTTP_200_OK)
        


class get_view_travel_request(ListCreateAPIView):
    serializer_class = Travel_RequestSerializers

    def get_queryset(self,travel_req_id,org_id):
        try:
            visa_request= Travel_Request.objects.filter(travel_req_id=travel_req_id,organization_id=request.GET['org_id'])
        # print(visa)
        except Travel_Request.DoesNotExist:

            return []
        return visa_request
        # Get all employee
        # import ipdb;ipdb.set_trace()
    def get(self, request):
        id=request.GET['travel_req_id']
        travel_request= Travel_Request.objects.filter(travel_req_id =request.GET['travel_req_id'],organization_id=request.GET['org_id'])
        
        travel_request_serializer = Travel_RequestSerializers(travel_request,many=True)
        
        if travel_request_serializer.data:
            emp_code=Employee.objects.filter(emp_code=travel_request_serializer.data[0]['emp_email']).values('emp_code','first_name','last_name')
            if emp_code[0]['emp_code']:
                travel_request_serializer.data[0]['emp_code']=emp_code[0]['emp_code']
            else:
                travel_request_serializer.data[0]['emp_code']=""
            if emp_code[0]['first_name']:
                travel_request_serializer.data[0]['first_name']=emp_code[0]['first_name']
            else:
                travel_request_serializer.data[0]['first_name']=""

            if emp_code[0]['last_name']:
                travel_request_serializer.data[0]['last_name']=emp_code[0]['last_name']
            else:
                travel_request_serializer.data[0]['last_name']=""
            visa_requests=Visa_Request.objects.filter(travel_req_id=request.GET['travel_req_id']).values("visa_req_id")
            if visa_requests:
                travel_request_serializer.data[0]['visa_requests']=visa_requests
            else:
                travel_request_serializer.data[0]['visa_requests']=""
            travel_requests=Travel_Request_Details.objects.filter(travel_req_id_id =id)
            travel_request_serializers= Travel_Request_DetailsSerializers(travel_requests,many=True)
            if travel_request_serializers:
                travel_request_serializer.data[0]['details']=travel_request_serializers.data
            else:
                travel_request_serializer.data[0]['details']=""
            travel_requestss=Travel_Request_Dependent.objects.filter(travel_req_id_id =id)
            travel_request_serializerss = Travel_Request_DependentSerializers(travel_requestss,many=True)
            if travel_request_serializer.data:
                travel_request_serializer.data[0]['dependents']=travel_request_serializerss.data
            else:
                travel_request_serializer.data[0]['dependents']=""
            dict = {'massage': 'data found', 'status': True, 'data':travel_request_serializer.data[0]}
        else:
            dict = {'massage': 'data not found', 'status': False, 'data':[]}
        return Response(dict, status=status.HTTP_200_OK)






class get_view_travel_request_draft(ListCreateAPIView):
    serializer_class = Travel_Request_DraftSerializers

    def get_queryset(self,travel_req_id,org_id):
        try:
            visa_request= Travel_Request_Draft.objects.filter(travel_req_id=travel_req_id,organization_id=request.GET['org_id'])
        # print(visa)
        except Travel_Request.DoesNotExist:

            return []
        return visa_request
        # Get all employee
        # import ipdb;ipdb.set_trace()
    def get(self, request):
        id=request.GET['travel_req_id']
        travel_request= Travel_Request_Draft.objects.filter(travel_req_id =request.GET['travel_req_id'],organization_id=request.GET['org_id'])
        travel_request_serializer = Travel_Request_DraftSerializers(travel_request,many=True)
        if travel_request_serializer.data:
            visa_requests=Visa_Request_Draft.objects.filter(travel_req_id=request.GET['travel_req_id']).values("visa_req_id")
            if visa_requests:
                travel_request_serializer.data[0]['visa_requests']=visa_requests
            else:
                travel_request_serializer.data[0]['visa_requests']=""
            travel_requests=Travel_Request_Details_Draft.objects.filter(travel_req_id_id =id)
            travel_request_serializers= Travel_Request_Details_DraftSerializers(travel_requests,many=True)
            if travel_request_serializers:
                travel_request_serializer.data[0]['details']=travel_request_serializers.data
            else:
                travel_request_serializer.data[0]['details']=""
            travel_requestss=Travel_Request_Dependent_Draft.objects.filter(travel_req_id_id =id)
            travel_request_serializerss = Travel_Request_Dependent_DraftSerializers(travel_requestss,many=True)
            if travel_request_serializer.data:
                travel_request_serializer.data[0]['dependents']=travel_request_serializerss.data
            else:
                travel_request_serializer.data[0]['dependents']=""
            dict = {'massage': 'data found', 'status': True, 'data':travel_request_serializer.data[0]}
        else:
            dict = {'massage': 'data not found', 'status': False, 'data':[]}
        return Response(dict, status=status.HTTP_200_OK)






class get_post_travel_request_draft(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Travel_Request_DraftSerializers
    def get_queryset(self,emp_email,travel_req_status,org_id):
        try:
            travel_request= Travel_Request_Draft.objects.filter(emp_email=emp_email,travel_req_status=travel_req_status,organization_id=org_id).order_by('-date_modified')

        # print(visa)
        except Travel_Request.DoesNotExist:

            return []
        return travel_request


    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        travel_request = self.get_queryset(request.GET["emp_email"],request.GET["travel_req_status"],request.GET["org_id"])

        alldata=[]
        for data in travel_request:
            travel_requests=Travel_Request_Draft.objects.filter(travel_req_id=data)
            travel_requests = Travel_Request_DraftSerializers(travel_requests,many=True)
            emp_code=Employee.objects.filter(emp_code=travel_requests.data[0]['emp_email']).values('emp_code','first_name','last_name')
            if emp_code[0]['emp_code']:
                travel_requests.data[0]['emp_code']=emp_code[0]['emp_code']
            else:
                travel_requests.data[0]['emp_code']=""
            if emp_code[0]['first_name']:
                travel_requests.data[0]['first_name']=emp_code[0]['first_name']
            else:
                travel_requests.data[0]['first_name']=""
            
            if emp_code[0]['last_name']:
                travel_requests.data[0]['last_name']=emp_code[0]['last_name']
            else:
                travel_requests.data[0]['last_name']=""
            #visa_requests=Visa_Request.objects.filter(travel_req_id=data).values("visa_req_id")
            #travel_requests.data[0]['visa_requests']=visa_requests
            travel_request_details=Travel_Request_Details_Draft.objects.filter(travel_req_id_id=data).values('id','travel_req_id_id','travelling_country', 'travelling_country_to','office_location','client_number','organization','source_city','destination_city','departure_date','return_date','is_accmodation_required','accmodation_start_date','accmodation_end_date','travel_purpose','assignment_type','applicable_visa','visa_number','visa_expiry_date','host_hr_name','host_country_head','host_attorney','host_phone_no','is_client_location','client_name','client_address','hotel_cost','per_diem_cost','airfare_cost','transportation_cost','total_cost','travel_request_status','travel_request_status_notes','is_dependent',)
            #print(travel_request_details)
            #travel_request_detail_serializers=Travel_RequestSerializers(travel_request_details,many=True)
            travel_requests.data[0]['details']=travel_request_details
            travel_request_dependent=Travel_Request_Dependent_Draft.objects.filter(travel_req_id_id=travel_requests.data[0]['travel_req_id'])
            travel_request_dependent=Travel_Request_Dependent_DraftSerializers(travel_request_dependent,many=True)
            travel_requests.data[0]['dependent']=travel_request_dependent.data
            alldata.append(travel_requests.data[0])
        dict = {'massage': 'data found', 'status': True, 'data': alldata}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)
    def post(self, request):
        # import ipdb;ipdb.set_trace()
        travel_request= request.data['travel_req_id']
        try:
            if travel_request:
                travel_request_id=Travel_Request_Draft.objects.filter(travel_req_id=request.data.get('travel_req_id')).first()
                serializer = Travel_Request_DraftSerializers(travel_request_id,data=request.data)
                data = request.data.copy()
                if serializer.is_valid():
                    serializer.save()

                travel=Travel_Request_Details_Draft.objects.filter(travel_req_id_id=request.data['travel_req_id'])
                travel.delete()
                travel=Travel_Request_Dependent_Draft.objects.filter(travel_req_id_id=request.data['travel_req_id'])
                travel.delete()
                for data in data['travel_city']:
                    #travel=Travel_Request_Details_Draft.objects.filter(travel_req_id_id=request.data['travel_req_id'])
                    #travel.delete()
                    data["travel_req_id"] = request.data['travel_req_id']
                    travel_request_detail = Travel_Request_Details_DraftSerializers(data=data)
                    if travel_request_detail.is_valid():
                        travel_request_detail.save()
                    for data in data['dependentData']:
                        data["travel_req_id"] = request.data['travel_req_id']
                        travel_request_dependent = Travel_Request_Dependent_DraftSerializers(data=data)
                        if travel_request_dependent.is_valid():
                            travel_request_dependent.save()
                    dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data':  request.data['travel_req_id']}
                return Response(dict, status=status.HTTP_200_OK)
            else:
                alldata=[]
                epoch=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                dt=str(epoch).replace(' ','')
                dt=str(dt).replace('-','')
                request.data['travel_req_id']="TR"+str(uuid.uuid4().int)[:6]
                request.data['travel_req_status']="1"
                serializer =Travel_Request_DraftSerializers(data=request.data)
                data=request.data.copy()
                if serializer.is_valid():
                    travel_id=serializer.save().travel_req_id
                    alldata.append(travel_id)
                else:
                    dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data': serializer.errors}
                for data in data['travel_city']:
                    data["travel_req_id"] = travel_id
                    travel_request_detail = Travel_Request_Details_DraftSerializers(data=data)
                    if travel_request_detail.is_valid():
                        travel_request_detail.save()
                    for data in data['dependentData']:
                        data["travel_req_id"] = request.data['travel_req_id']
                        travel_request_dependent = Travel_Request_Dependent_DraftSerializers(data=data)
                        if travel_request_dependent.is_valid():
                            travel_request_dependent.save()
                        else:
                            dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data': travel_request_dependent.errors}
                    else:
                        dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data': travel_request_detail.errors}
                    dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data': alldata}
            return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            dict = {'massage code': 'already exists', 'massage': 'unsuccessful', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)

class get_travel_request_approver(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = Travel_RequestSerializers

    def get_queryset(self,emp_email,travel_req_status):
        try:
            travel_request= Travel_Request.objects.filter(Q(expense_approver=emp_email)|Q(project_manager=emp_email)|Q(business_lead=emp_email)|Q(client_executive_lead=emp_email)|Q(supervisor=emp_email)|Q(current_ticket_owner=emp_email),travel_req_status="6").values("travel_req_id")
        # print(visa)
        except Travel_Request.DoesNotExist:

            return []
        return travel_request


    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        alldata=[]
        if request.GET['type']=="Travel":
            travel_request= Travel_Request.objects.filter(Q(expense_approver=request.GET['emp_email'])|Q(project_manager=request.GET['emp_email'])|Q(business_lead=request.GET['emp_email'])|Q(client_executive_lead=request.GET['emp_email'])|Q(supervisor=request.GET['emp_email']),Q(travel_req_status=request.GET['travel_req_status'])|Q(travel_req_status="6"),current_ticket_owner=request.GET['emp_email'],organization_id=request.GET['org_id']).values("travel_req_id").order_by('-date_modified')
            for data in travel_request:
                print(data)
                travel_request=Travel_Request.objects.filter(travel_req_id=data['travel_req_id'])
                travel_requests = Travel_RequestSerializers(travel_request,many=True)
                emp_code=Employee.objects.filter(emp_code=travel_requests.data[0]['emp_email']).values('emp_code','first_name','last_name','email')
                if emp_code[0]['emp_code']:
                    travel_requests.data[0]['emp_code']=emp_code[0]['emp_code']
                else:
                    travel_requests.data[0]['emp_code']=""
                emp_codes=Employee.objects.filter(emp_code=travel_requests.data[0]['current_ticket_owner']).values('email')
                if emp_codes[0]['email']:
                    travel_requests.data[0]['current_ticket_owner']=emp_codes[0]['email']
                else:
                    travel_requests.data[0]['current_ticket_owner']=""
                if emp_code[0]['first_name']:
                    travel_requests.data[0]['first_name']=emp_code[0]['first_name']
                else:
                    travel_requests.data[0]['first_name']=""
                
                if emp_code[0]['last_name']:
                    travel_requests.data[0]['last_name']=emp_code[0]['last_name']
                else:
                    travel_requests.data[0]['last_name']=""
                travel_request_detail=Travel_Request_Details.objects.filter(travel_req_id=travel_requests.data[0]['travel_req_id']).values('id','travel_req_id_id','travelling_country', 'travelling_country_to','office_location','client_number','organization','source_city','destination_city','departure_date','return_date','is_accmodation_required','accmodation_start_date','accmodation_end_date','travel_purpose','assignment_type','applicable_visa','visa_number','visa_expiry_date','host_hr_name','host_country_head','host_attorney','host_phone_no','is_client_location','client_name','client_address','hotel_cost','per_diem_cost','airfare_cost','transportation_cost','total_cost','travel_request_status','travel_request_status_notes','is_dependent',)
                #travel_request_detail=Travel_RequestSerializers(travel_request_detail,many=True).values('id','travel_req_id_id','travelling_country', 'travelling_country_to','office_location','client_number','organization','source_city','destination_city','departure_date','return_date','is_accmodation_required','accmodation_start_date','accmodation_end_date','travel_purpose','assignment_type','applicable_visa','visa_number','visa_expiry_date','host_hr_name','host_country_head','host_attorney','host_phone_no','is_client_location','client_name','client_address','hotel_cost','per_diem_cost','airfare_cost','transportation_cost','total_cost','travel_request_status','travel_request_status_notes','is_dependent',)
                travel_requests.data[0]['details']=travel_request_detail
                travel_request_dependent=Travel_Request_Dependent.objects.filter(travel_req_id=travel_requests.data[0]['travel_req_id'])
                travel_request_dependent=Travel_Request_DependentSerializers(travel_request_dependent,many=True)
                travel_requests.data[0]['dependent']=travel_request_dependent.data
                alldata.append(travel_requests.data[0])
            dict = {'massage': 'data found', 'status': True, 'data': alldata}
        elif request.GET['type']=="Visa":
            visa_request= Visa_Request.objects.filter(Q(expense_approver=request.GET['emp_email'])|Q(project_manager=request.GET['emp_email'])|Q(business_lead=request.GET['emp_email'])|Q(client_executive_lead=request.GET['emp_email'])|Q(client_executive_lead=request.GET['emp_email'])|Q(supervisor=request.GET['emp_email']),Q(visa_status=request.GET['visa_status'])|Q(visa_status="6"),current_ticket_owner=request.GET['emp_email'],organization_id=request.GET['org_id']).values("visa_req_id").order_by('-date_modified')
            for data in visa_request:
                visa_request=Visa_Request.objects.filter(visa_req_id=data['visa_req_id'])
                visa_request = Visa_RequestSerializers(visa_request,many=True)
                emp_code=Employee.objects.filter(emp_code=visa_request.data[0]['emp_email']).values('emp_code','first_name','last_name')
                if emp_code[0]['emp_code']:
                    visa_request.data[0]['emp_code']=emp_code[0]['emp_code']
                else:
                    visa_request.data[0]['emp_code']=""
                emp_codes=Employee.objects.filter(emp_code=visa_request.data[0]['current_ticket_owner']).values('email')
                if emp_codes[0]['email']:
                    visa_request.data[0]['current_ticket_owner']=emp_codes[0]['email']
                else:
                    visa_request.data[0]['current_ticket_owner']=""
                if emp_code[0]['first_name']:
                    visa_request.data[0]['first_name']=emp_code[0]['first_name']
                else:
                    visa_request.data[0]['first_name']=""

                if emp_code[0]['last_name']:
                    visa_request.data[0]['last_name']=emp_code[0]['last_name']
                else:
                    visa_request.data[0]['last_name']=""
                alldata.append(visa_request.data[0])
            dict = {'massage': 'data found', 'status': True, 'data':alldata}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)


class get_travel_request_history(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Travel_RequestSerializers
    def get(self, request):
        alldata=[]
        if request.GET['type']=="Travel":
            travel_requestss=Travel_Request_Action_History.objects.filter(email_id=request.GET['email'],action=request.GET['status'],organization_id=request.GET['org_id']).values("travel_req_id").order_by('-date_modified')
            for data in travel_requestss:
                print(data['travel_req_id'])
                travel_request=Travel_Request.objects.filter(travel_req_id=data['travel_req_id'])
                travel_requests = Travel_RequestSerializers(travel_request,many=True)
                emp_code=Employee.objects.filter(emp_code=travel_requests.data[0]['emp_email']).values('emp_code','first_name','last_name')
                if emp_code[0]['emp_code']:
                    travel_requests.data[0]['emp_code']=emp_code[0]['emp_code']
                else:
                    travel_requests.data[0]['emp_code']=""
                if emp_code[0]['first_name']:
                    travel_requests.data[0]['first_name']=emp_code[0]['first_name']
                else:
                    travel_requests.data[0]['first_name']=""

                if emp_code[0]['last_name']:
                    travel_requests.data[0]['last_name']=emp_code[0]['last_name']
                else:
                    travel_requests.data[0]['last_name']=""
                emp_codes=Employee.objects.filter(emp_code=travel_requests.data[0]['current_ticket_owner']).values('email')
                if emp_codes:
                    travel_requests.data[0]['current_ticket_owner']=emp_codes[0]['email']
                else:
                    travel_requests.data[0]['current_ticket_owner']=""
                travel_request_detail=Travel_Request_Details.objects.filter(travel_req_id=travel_requests.data[0]['travel_req_id']).values('id','travel_req_id_id','travelling_country', 'travelling_country_to','office_location','client_number','organization','source_city','destination_city','departure_date','return_date','is_accmodation_required','accmodation_start_date','accmodation_end_date','travel_purpose','assignment_type','applicable_visa','visa_number','visa_expiry_date','host_hr_name','host_country_head','host_attorney','host_phone_no','is_client_location','client_name','client_address','hotel_cost','per_diem_cost','airfare_cost','transportation_cost','total_cost','travel_request_status','travel_request_status_notes','is_dependent',)
                #travel_request_detail=Travel_RequestSerializers(travel_request_detail,many=True)
                travel_requests.data[0]['details']=travel_request_detail
                travel_request_dependent=Travel_Request_Dependent.objects.filter(travel_req_id=travel_requests.data[0]['travel_req_id'])
                travel_request_dependent=Travel_Request_DependentSerializers(travel_request_dependent,many=True)
                travel_requests.data[0]['dependent']=travel_request_dependent.data
                alldata.append(travel_requests.data[0])
            dict = {'massage': 'data found', 'status': True, 'data': alldata}
        elif request.GET['type']=="Visa":
            visa_request= Visa_Request_Action_History.objects.filter(email_id=request.GET['email'],action=request.GET['status']).values("visa_req_id").order_by('-date_modified')
            for data in visa_request:
                visa_request=Visa_Request.objects.filter(visa_req_id=data['visa_req_id'])
                if visa_request:
                    visa_request = Visa_RequestSerializers(visa_request,many=True)
                    emp_code=Employee.objects.filter(emp_code=visa_request.data[0]['emp_email']).values('emp_code','first_name','last_name')
                    if emp_code[0]['emp_code']:
                        visa_request.data[0]['emp_code']=emp_code[0]['emp_code']
                    else:
                        visa_request.data[0]['emp_code']=""
                    if emp_code[0]['first_name']:
                        visa_request.data[0]['first_name']=emp_code[0]['first_name']
                    else:
                        visa_request.data[0]['first_name']=""
                        
                    if emp_code[0]['last_name']:
                        visa_request.data[0]['last_name']=emp_code[0]['last_name']
                    else:
                        visa_request.data[0]['last_name']=""
                    emp_codes=Employee.objects.filter(emp_code=visa_request.data[0]['current_ticket_owner']).values('email')
                    if emp_codes:
                        visa_request.data[0]['current_ticket_owner']=emp_codes[0]['email']
                    else:
                        visa_request.data[0]['current_ticket_owner']=""
                    alldata.append(visa_request.data[0])
                else:
                    dict = {'massage': 'data found', 'status': True, 'data':alldata}

            dict = {'massage': 'data found', 'status': True, 'data':alldata}
        return Response(dict, status=status.HTTP_200_OK)

class get_travel_action(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        travel=Travel_Request_Action_History.objects.filter(email=request.GET['email'],action=request.GET['status'],organization_id=request.GET['org_id'])
        travelserializers=Travel_Request_Action_HistorySerializers(travel,many=True)

        dict = {'massage': 'data found', 'status': True, 'data': travelserializers.data}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)



class get_travel_status_summary(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request):
        travelserializerss=Travel_Request.objects.filter(travel_req_id=request.GET['travel_req_id']).values("travel_req_id","supervisor","expense_approver","project_manager","business_lead","client_executive_lead","travel_req_status","current_ticket_owner","date_modified")
        alldata=[]
        travelserializersssts=Travel_Request_Action_History.objects.filter(travel_req_id_id=request.GET['travel_req_id'],email_id=travelserializerss[0]['supervisor'],approval_level="0").values(
            "action","email","date_modified",'approval_level')
        dicsts={}
        if travelserializersssts.exists():
            dicsts['supervisor_status']=travelserializersssts[0]['action']
            dicsts['approval_level']=travelserializersssts[0]['approval_level']
            dicsts['current_ticket_owner']=travelserializerss[0]['current_ticket_owner']
            empname=Employee.objects.filter(emp_code=travelserializersssts[0]['email']).values('first_name','last_name','email')
            if empname:
                dicsts['supervisor_name']=empname[0]['first_name'] + " " + empname[0]['last_name']
                dicsts['supervisor']=empname[0]['email']
            else:
                dicsts['supervisor_name']=""
                dicsts['supervisor']=""
            dicsts['action_date']=travelserializersssts[0]['date_modified']
        else:
            dicsts['supervisor_status']=""
            dicsts['approval_level']=""
            dicsts['supervisor']=travelserializerss[0]['supervisor']
            dicsts['current_ticket_owner']=travelserializerss[0]['current_ticket_owner']
            empname=Employee.objects.filter(emp_code=travelserializerss[0]['supervisor']).values('first_name','last_name','email')
            if empname:
                dicsts['supervisor_name']=empname[0]['first_name'] + " " + empname[0]['last_name']
                dicsts['supervisor']=empname[0]['email']
            else:
                dicsts['supervisor_name']=""
                dicsts['supervisor']=""
            #dicsts['supervisor_name']=empname[0]['first_name']
            dicsts['action_date']=travelserializerss[0]['date_modified']
        alldata.append(dicsts)
        travelserializersss=Travel_Request_Action_History.objects.filter(travel_req_id_id=request.GET['travel_req_id'],email_id=travelserializerss[0]['expense_approver'],approval_level="1").values(
            "action","email","date_modified","approval_level")
        dic={}
        if travelserializersss.exists():
            dic['expense_approver_status']=travelserializersss[0]['action']
            dic['approval_level']=travelserializersss[0]['approval_level']
            dic['expense_approver']=travelserializersss[0]['email']
            dic['current_ticket_owner']=travelserializerss[0]['current_ticket_owner']
            empname=Employee.objects.filter(emp_code=travelserializersss[0]['email']).values('first_name','last_name','email')
            if empname:
                dic['expense_approver_name']=empname[0]['first_name'] + " " + empname[0]['last_name']
                dic['expense_approver']=empname[0]['email']
            else:
                dic['expense_approver_name']=""
                dic['expense_approver']=""
            #dic['expense_approver_name']=empname[0]['first_name']
            dic['action_date']=travelserializersss[0]['date_modified']
        else:
            dic['expense_approver_status']=""
            dic['approval_level']=""
            dic['expense_approver']=travelserializerss[0]['expense_approver']
            dic['current_ticket_owner']=travelserializerss[0]['current_ticket_owner']
            empname=Employee.objects.filter(emp_code=travelserializerss[0]['expense_approver']).values('first_name','last_name','email')
            if empname:
                dic['expense_approver_name']=empname[0]['first_name'] + " " + empname[0]['last_name']
                dic['expense_approver']=empname[0]['email']
            else:
                dic['expense_approver_name']=""
                dic['expense_approver']=""
            #dic['expense_approver_name']=empname[0]['first_name']
            dic['action_date']=travelserializerss[0]['date_modified']
        alldata.append(dic)
        travelserializerssss=Travel_Request_Action_History.objects.filter(travel_req_id_id=request.GET['travel_req_id'],email_id=travelserializerss[0]['project_manager'],approval_level="2").values(
            "action","email","date_modified","approval_level")
        dics={}
        if travelserializerssss.exists():
            dics['project_manager_status']=travelserializerssss[0]['action']
            dics['approval_level']=travelserializerssss[0]['approval_level']
            
            dics['current_ticket_owner']=travelserializerss[0]['current_ticket_owner']
            empname=Employee.objects.filter(emp_code=travelserializerssss[0]['email']).values('first_name','last_name','email')
            if empname:
                dics['project_manager_name']=empname[0]['first_name'] + " " + empname[0]['last_name']
                dics['project_manager']=empname[0]['email']
            else:
                dics['project_manager_name']=""
                dics['project_manager']=""
            #dics['project_manager_name']=empname[0]['first_name']
            dics['action_date']=travelserializerssss[0]['date_modified']
        else:
            dics['project_manager_status']=""
            dics['approval_level']=""
           
            dics['current_ticket_owner']=travelserializerss[0]['current_ticket_owner']
            empname=Employee.objects.filter(emp_code=travelserializerss[0]['project_manager']).values('first_name','last_name','email')
            if empname:
                dics['project_manager_name']=empname[0]['first_name'] + " " + empname[0]['last_name']
                dics['project_manager']=empname[0]['email']
            else:
                dics['project_manager_name']=""
                dics['project_manager']=""
            #dics['project_manager_name']=empname[0]['first_name']
            dics['action_date']=travelserializerss[0]['date_modified']
        alldata.append(dics)
        travelserializersssss=Travel_Request_Action_History.objects.filter(travel_req_id_id=request.GET['travel_req_id'],email_id=travelserializerss[0]['business_lead'],approval_level="3").values(
            "action","email","date_modified","approval_level")
        dicss={}
        if travelserializersssss.exists():
            dicss['business_lead_status']=travelserializersssss[0]['action']
            dicss['approval_level']=travelserializersssss[0]['approval_level']
            dicss['current_ticket_owner']=travelserializerss[0]['current_ticket_owner']
            empname=Employee.objects.filter(emp_code=travelserializersssss[0]['email']).values('first_name','last_name','email')
            if empname:
                dicss['business_lead_name']=empname[0]['first_name'] + " " + empname[0]['last_name']
                dicss['business_lead']=empname[0]['email']
            else:
                dicss['business_lead_name']=""
                dicss['business_lead']=""
            #dicss['business_lead_name']=empname[0]['first_name']
            dicss['action_date']=travelserializersssss[0]['date_modified']
        else:
            dicss['business_lead_status']=""
            dicss['approval_level']=""
            dicss['current_ticket_owner']=travelserializerss[0]['current_ticket_owner']
            empname=Employee.objects.filter(emp_code=travelserializerss[0]['business_lead']).values('first_name','last_name','email')
            if empname:
                dicss['business_lead_name']=empname[0]['first_name'] + " " + empname[0]['last_name']
                dicss['business_lead']=empname[0]['email']
            else:
                dicss['business_lead_name']=""
                dicss['business_lead']=""
            #dicss['business_lead_name']=empname[0]['first_name']
            dicss['action_date']=travelserializerss[0]['date_modified']
        alldata.append(dicss)
        travelserializerssssss=Travel_Request_Action_History.objects.filter(travel_req_id_id=request.GET['travel_req_id'],email_id=travelserializerss[0]['client_executive_lead'],approval_level="4").values(
            "action","email","date_modified","approval_level")
        dicsss={}
        if travelserializerssssss.exists():
            dicsss['client_executive_lead_status']=travelserializerssssss[0]['action']
            dicsss['approval_level']=travelserializerssssss[0]['approval_level']
            
            dicsss['current_ticket_owner']=travelserializerss[0]['current_ticket_owner']
            empname=Employee.objects.filter(emp_code=travelserializerssssss[0]['email']).values('first_name','last_name','email')
            if empname:
                dicsss['client_executive_lead_name']=empname[0]['first_name'] + " " + empname[0]['last_name']
                dicsss['client_executive_lead']=empname[0]['email']
            else:
                dicsss['client_executive_lead_name']=""
                dicsss['client_executive_lead']=""
            #dicsss['client_executive_lead_name']=empname[0]['first_name']
            dicsss['action_date']=travelserializerssssss[0]['date_modified']
        else:
            dicsss['client_executive_lead_status']=""
            dicsss['approval_level']=""
            
            dicsss['current_ticket_owner']=travelserializerss[0]['current_ticket_owner']
            empname=Employee.objects.filter(emp_code=travelserializerss[0]['client_executive_lead']).values('first_name','last_name','email')
            if empname:
                dicsss['client_executive_lead_name']=empname[0]['first_name'] + " " + empname[0]['last_name']
                dicsss['client_executive_lead']=empname[0]['email']
            else:
                dicsss['client_executive_lead_name']=""
                dicsss['client_executive_lead']=""
            #dicsss['client_executive_lead_name']=empname[0]['first_name']
            dicsss['action_date']=travelserializerss[0]['date_modified']
        transfer_trvel=Travel_Request_Action_History.objects.filter(travel_req_id_id=request.GET['travel_req_id'],action="6").values(
            "action","email","date_modified","approval_level").exclude(approval_level=None)
        i=0    
        for transfer_trvel_email in transfer_trvel:
            empname=Employee.objects.filter(emp_code=transfer_trvel_email['email']).values('first_name','last_name','email')
            if empname:
                transfer_trvel[i]['Frist_name']=empname[0]['first_name'] + " " + empname[0]['last_name']
            else:
                transfer_trvel[i]['Frist_name']=""
            i=i+1
        alldata.append(dicsss)
        #travelserializers=Travel_RequestSerializers(travelserializers,many=True)
        dict = {'massage': 'data found', 'status': True, 'data': alldata,'tranfer':transfer_trvel}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)

class get_post_approve_travelvisa_request(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Travel_RequestSerializers
    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()
        if request.data.get('travel_req_id'):

            notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
            travel_request_id= request.data['travel_req_id']
            travel_request_id=Travel_Request.objects.filter(travel_req_id=request.data.get('travel_req_id'),organization_id=request.data.get('org_id')).first()
            employee=Travel_Request.objects.filter(travel_req_id=request.data.get('travel_req_id')).values('supervisor','business_lead','project_manager','expense_approver','client_executive_lead','emp_email_id','approval_level')
            supervisor=employee[0]['supervisor']
            business_lead=employee[0]['business_lead']
            project_manager=employee[0]['project_manager']
            expense_approver=employee[0]['expense_approver']
            client_executive_lead=employee[0]['client_executive_lead']
            current_ticket_owner= request.data['current_ticket_owner']
            emp_email_id= employee[0]['emp_email_id']

            request.data['current_ticket_owner']=""
            teemp_status=employee[0]['approval_level']
            if request.data['approve_action']=="A":
                travel_req_status=Status_Master.objects.filter(name="Approved").values("value")
                if employee[0]['approval_level']=="0":
                    if employee[0]['expense_approver']:
                        request.data['current_ticket_owner'] =employee[0]['expense_approver']
                        request.data['approval_level']="1"
                    elif employee[0]['project_manager']:
                        request.data['current_ticket_owner'] =employee[0]['project_manager']
                        request.data['approval_level']="2"
                    elif employee[0]['business_lead']:
                        request.data['current_ticket_owner'] =employee[0]['business_lead']
                        request.data['approval_level']="3"
                    elif employee[0]['client_executive_lead']:
                        request.data['current_ticket_owner'] =employee[0]['client_executive_lead']
                        request.data['approval_level']="4"
                    else:
                        request.data['current_ticket_owner'] = ""
                elif employee[0]['approval_level']=="1":
                    if employee[0]['project_manager']:
                        request.data['current_ticket_owner'] =employee[0]['project_manager']
                        request.data['approval_level']="2"
                    elif employee[0]['business_lead']:
                        request.data['current_ticket_owner'] =employee[0]['business_lead']
                        request.data['approval_level']="3"
                    elif employee[0]['client_executive_lead']:
                        request.data['current_ticket_owner'] =employee[0]['client_executive_lead']
                        request.data['approval_level']="4"
                    else:
                        request.data['current_ticket_owner'] = ""
                
                elif employee[0]['approval_level']=="2":
                    if employee[0]['business_lead']:
                        request.data['current_ticket_owner'] =employee[0]['business_lead']
                        request.data['approval_level']="3"
                    elif employee[0]['client_executive_lead']:
                        request.data['current_ticket_owner'] =employee[0]['client_executive_lead']
                        request.data['approval_level']="4"
                    else:
                        request.data['current_ticket_owner'] = ""
                elif employee[0]['approval_level']=="3":
                    if employee[0]['client_executive_lead']:
                        request.data['current_ticket_owner'] =employee[0]['client_executive_lead']
                        request.data['approval_level']="4"
                    else:
                        request.data['current_ticket_owner'] = ""
                elif employee[0]['approval_level']=="4":
                    if employee[0]['client_executive_lead']:
                        request.data['current_ticket_owner'] =""
                        request.data['approval_level']="5"
                    else:
                        request.data['current_ticket_owner'] = ""
                    request.data['travel_req_status']="4"
                request.data['travel_req_status']="2"
                request.data['Entity_Type']="Travel"
                request.data['Entity_ID']=request.data['travel_req_id']
                request.data['Action_taken_by']=request.data['current_ticket_owner']
                request.data['Notification_Date']=""
                request.data['Message']=request.data['travel_req_id']+" New travel request for approval"
                request.data['Notification_ID']=notificationid
                request.data['organization']=request.data['org_id']
                serializernotificationss = NotificationSerializers(data=request.data)
                if serializernotificationss.is_valid():
                    serializernotificationss.save()
                    travelid=Travel_Request.objects.filter(travel_req_id=request.data['travel_req_id']).values('is_billable','project','expence_cureency','expence_departureDate','expence_estimatedCost','expence_fromCountry','expence_returnDate','expence_toCountry')
                    
                    if travelid[0]['expence_estimatedCost']:
                        costs=travelid[0]['expence_estimatedCost']+' '+travelid[0]['expence_cureency']
                    else:
                        costs='0'
                    if travelid[0]['is_billable']==True:
                        is_billable='Yes'
                    else:
                        is_billable='No'
                    ctxt = {
                        'first_name': self.employee_name(emp_code=employee[0]['emp_email_id']),
                        'approve_first_name':self.approver_name(emp_code=request.data['Action_taken_by']),
                        'project_id': travelid[0]['project'],
                        'billable': is_billable,
                        'from_country':travelid[0]['expence_fromCountry'],
                        'to_country':travelid[0]['expence_toCountry'],
                        'departure_date':travelid[0]['expence_departureDate'],
                        'return_date':travelid[0]['expence_returnDate'],
                        'total_cost_master_currency':costs,
                        'supervisor':self.employee_name(emp_code=employee[0]['supervisor']),
                        'expense_approver':self.employee_name(emp_code=employee[0]['expense_approver']),
                        'project_manager': self.employee_name(emp_code=employee[0]['project_manager']),
                        'business_lead':self.employee_name(emp_code=employee[0]['business_lead']),
                        'client_executive_lead':self.employee_name(emp_code=employee[0]['client_executive_lead'])
                    }


                    if request.data['current_ticket_owner']!="":
                        template='email/approve_travel_request.html'
                        emailsubject='Travel request for '+self.employee_name(emp_code=employee[0]['emp_email_id'])+' requires approval'
                        self.sendmails(ctxt,template,emailsubject,emailto=request.data['current_ticket_owner'],id=request.data['travel_req_id'])
                    notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                    request.data['Entity_Type']="Travel"
                    request.data['Entity_ID']=request.data['travel_req_id']
                    request.data['Action_taken_by']=emp_email_id
                    request.data['Notification_Date']=""
                    request.data['Message']=request.data['travel_req_id']+" Travel request approved by "+request.data['modified_by']
                    request.data['Notification_ID']=notificationid
                    request.data['organization']=request.data['org_id']
                    
                    serializernotifications = NotificationSerializers(data=request.data)
                    if serializernotifications.is_valid():
                        serializernotifications.save()
                        if current_ticket_owner !="":
                            approver_name=self.employee_name(emp_code=current_ticket_owner)
                        else:
                            approver_name="Assignment Team"
                        ctxt = {
                                'approver_name': approver_name,
                                'next_approver_name':self.employee_name(emp_code=request.data['current_ticket_owner']),
                                'preferred_first_name':self.approver_name(emp_code=request.data['Action_taken_by']),
                                'travel_request_id':request.data['travel_req_id'],

                        }
                        template='email/approvedtravelrequest.html'
                        emailsubject='Your travel request '+request.data['travel_req_id']+' have been approved'
                        self.sendmails(ctxt,template,emailsubject,emailto=employee[0]['emp_email_id'],id=request.data['travel_req_id'])
            elif request.data['approve_action']=="R":
                travel_req_status=Status_Master.objects.filter(name="Rejected").values("value")
                request.data['travel_req_status']=travel_req_status[0]['value']
                request.data['current_ticket_owner']=current_ticket_owner
                request.data['Entity_Type']="Travel"
                request.data['Entity_ID']=request.data['travel_req_id']
                request.data['Action_taken_by']=emp_email_id
                request.data['Notification_Date']=""
                request.data['Message']=request.data['travel_req_id']+" Travel Request Rejected"
                request.data['Notification_ID']=notificationid
                request.data['organization']=request.data['org_id']
                serializernotification = NotificationSerializers(data=request.data)
                if serializernotification.is_valid():
                    serializernotification.save()
                    ctxt = {
                            'approver_name': self.employee_name(emp_code=current_ticket_owner),
                            'preferred_first_name':self.approver_name(emp_code=request.data['Action_taken_by']),
                            'travel_request_id': request.data['travel_req_id'],
                            'msg': request.data['request_notes']

                    }
                    template='email/travelreject.html'
                    emailsubject='Your travel request '+request.data['travel_req_id']+' has been rejected'
                    self.sendmails(ctxt,template,emailsubject,emailto=employee[0]['emp_email_id'],id=request.data['travel_req_id'])
            elif request.data['approve_action']=="T":
                travel_req_status=Status_Master.objects.filter(name="Transferred").values("value")
                request.data['travel_req_status']=travel_req_status[0]['value']
                if request.data['approval_level']=="1":
                    request.data['expense_approver'] = request.data['transfer_to']
                    request.data['current_ticket_owner']=request.data['transfer_to']
                elif request.data['approval_level']=="2":
                    request.data['project_manager'] =request.data['transfer_to']
                    request.data['current_ticket_owner']=request.data['transfer_to']
                elif request.data['approval_level']=="3":
                    request.data['business_lead'] =request.data['transfer_to']
                    request.data['current_ticket_owner']=request.data['transfer_to']
                elif request.data['approval_level']=="4":
                    request.data['client_executive_lead'] =request.data['transfer_to']
                    request.data['current_ticket_owner']=request.data['transfer_to']
                request.data['Entity_Type']="Travel"
                request.data['Entity_ID']=request.data['travel_req_id']
                request.data['Action_taken_by']=request.data['transfer_to']
                request.data['Notification_Date']=""
                request.data['Message']=request.data['travel_req_id']+" Travel request transferred"
                request.data['Notification_ID']=notificationid
                request.data['organization']=request.data['org_id']
                serializernotificationss = NotificationSerializers(data=request.data)
                if serializernotificationss.is_valid():
                    serializernotificationss.save()
                    ctxt = {
                        'approver_name': self.employee_name(emp_code=current_ticket_owner),
                        'preferred_first_name':self.approver_name(emp_code=request.data['Action_taken_by']),
                        'travel_request_id': request.data['travel_req_id'],
                        'msg': request.data['request_notes']

                    }
                    template='email/traveltransferforapproval.html'
                    emailsubject='New travel request '+request.data['travel_req_id']+' has been transferred for your approval'
                    self.sendmails(ctxt,template,emailsubject,emailto=request.data['Action_taken_by'],id=request.data['travel_req_id'])
                    notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                    request.data['Entity_Type']="Travel"
                    request.data['Entity_ID']=request.data['travel_req_id']
                    request.data['Action_taken_by']=emp_email_id
                    request.data['Notification_Date']=""
                    request.data['Message']=request.data['travel_req_id']+" Travel request transferred to "+request.data['current_ticket_owner']
                    request.data['Notification_ID']=notificationid
                    request.data['organization']=request.data['org_id']
                    serializernotifications = NotificationSerializers(data=request.data)
                    if serializernotifications.is_valid():
                        serializernotifications.save()
                    ctxt = {
                        'approver_name': self.employee_name(emp_code=request.data['current_ticket_owner']),
                        'preferred_first_name':self.approver_name(emp_code=request.data['Action_taken_by']),
                        'travel_request_id': request.data['travel_req_id'],
                        'msg': request.data['request_notes']

                    }
                    template='email/traveltransfer.html'
                    emailsubject='Your travel request '+request.data['travel_req_id']+' has been transferred to '+self.employee_name(emp_code=request.data['current_ticket_owner'])
                    self.sendmails(ctxt,template,emailsubject,emailto=employee[0]['emp_email_id'],id=request.data['travel_req_id'])
            if request.data['take_ownership']:
                request.data['current_ticket_owner']=request.data['take_ownership']
                notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                request.data['Entity_Type']="Travel"
                request.data['Entity_ID']=request.data['travel_req_id']
                request.data['Action_taken_by']=emp_email_id
                request.data['Notification_Date']=""
                request.data['Message']=request.data['travel_req_id']+" Travel request Assigned to "+request.data['current_ticket_owner']
                request.data['Notification_ID']=notificationid
                request.data['organization']=request.data['org_id']
                serializernotifications = NotificationSerializers(data=request.data)
                if serializernotifications.is_valid():
                    serializernotifications.save()
                    msg="Travel request  assigned"
                    self.sendmails(msg,request.data['Message'],request.data['Action_taken_by'])
            travel_request_id_ids=Travel_Request.objects.filter(travel_req_id=request.data['travel_req_id']).first()
            serializer = Travel_RequestSerializers(travel_request_id_ids,data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data':  serializer.errors}
            if request.data['approve_action']=="A":
                travel_req_status=Status_Master.objects.filter(name="Approved").values("value")
                request.data['action']="4"
            else:
                request.data['action']=request.data['travel_req_status']
            request.data['action_notes']=request.data['request_notes']
            request.data['email']=current_ticket_owner
            request.data['module']=request.data['module']
            request.data['travel_req_id_id']=request.data['travel_req_id']
            request.data['organization']=request.data['org_id']
            # subject = 'Request Update'
            # message = ''
            # html_message = '<h3>Your Request Hasapproved By:</h3>'
            # html_message += '<p> User Name <b>: '+current_ticket_owner+'</b> </p>'
            # #html_message += '<p>User Name : <b>' +password+ '</b> </p>'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [emp_email_id,current_ticket_owner,]
            # send_mail(subject, message, email_from, recipient_list, fail_silently=False, html_message=html_message)
            request.data['approval_level']=teemp_status
            serializeraction=Travel_Request_Action_HistorySerializers(data=request.data)
            if serializeraction.is_valid():
                serializeraction.save()
            else:
                dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data':  serializeraction.errors}

        visa_request_id=Visa_Request.objects.filter(travel_req_id=request.data['travel_req_id']).values("visa_req_id")
        if visa_request_id:
            for data in visa_request_id:
                employee=Visa_Request.objects.filter(visa_req_id=data['visa_req_id']).values('supervisor','business_lead','project_manager','expense_approver','client_executive_lead','current_ticket_owner','emp_email_id','approval_level','country','travel_start_date','travel_end_date','applied_visa','is_billable','project_id')

                supervisor=employee[0]['supervisor']
                business_lead=employee[0]['business_lead']
                project_manager=employee[0]['project_manager']
                expense_approver=employee[0]['expense_approver']
                client_executive_lead=employee[0]['client_executive_lead']
                current_ticket_owner=employee[0]['current_ticket_owner']
                data['current_ticket_owner']=request.data['current_ticket_owner']
                data['request_notes']=request.data['request_notes']
                data['approve_action']=request.data['approve_action']
                data['take_ownership']=request.data['take_ownership']
                data['transfer_to']=request.data['transfer_to']
                data['organization']=request.data['org_id']
                data['modified_by']=request.data['modified_by']
                teemp_status=employee[0]['approval_level']
                emp_email_id=employee[0]['emp_email_id']
                data['module']="Visa"
                if data['approve_action']=="A":
                    if employee[0]['approval_level']=="0":
                        if employee[0]['expense_approver']:
                            data['current_ticket_owner']=employee[0]['expense_approver']
                            data['approval_level']="1"
                        elif employee[0]['project_manager']:
                            data['current_ticket_owner'] =employee[0]['project_manager']
                            data['approval_level']="2"
                        elif employee[0]['business_lead']:
                            data['current_ticket_owner'] =employee[0]['business_lead']
                            data['approval_level']="3"
                        elif employee[0]['client_executive_lead']:
                            data['current_ticket_owner'] =employee[0]['client_executive_lead']
                            data['approval_level']="4"
                        else:
                            data['current_ticket_owner'] = ""
                    elif employee[0]['approval_level']=="1":
                        if employee[0]['project_manager']:
                            data['current_ticket_owner'] =employee[0]['project_manager']
                            data['approval_level']="2"
                        elif employee[0]['business_lead']:
                            data['current_ticket_owner'] =employee[0]['business_lead']
                            data['approval_level']="3"
                        elif employee[0]['client_executive_lead']:
                            data['current_ticket_owner'] =employee[0]['client_executive_lead']
                            data['approval_level']="4"
                        else:
                            data['current_ticket_owner'] = ""
                    
                    elif employee[0]['approval_level']=="2":
                        if employee[0]['business_lead']:
                            data['current_ticket_owner'] =employee[0]['business_lead']
                            data['approval_level']="3"
                        elif employee[0]['client_executive_lead']:
                            data['current_ticket_owner'] =employee[0]['client_executive_lead']
                            data['approval_level']="4"
                        else:
                            data['current_ticket_owner'] = ""
                    elif employee[0]['approval_level']=="3":
                        if employee[0]['client_executive_lead']:
                            data['current_ticket_owner'] =employee[0]['client_executive_lead']
                            data['approval_level']="4"
                        else:
                            data['current_ticket_owner'] = ""
                    elif employee[0]['approval_level']=="4":
                        if employee[0]['client_executive_lead']:
                            data['current_ticket_owner'] =""
                            data['approval_level']="5"
                        else:
                            data['current_ticket_owner'] = ""
                        data['visa_status']="4"
                    data['visa_status']="2"
                    data['Entity_Type']="Visa"
                    notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                    data['Entity_ID']=data['visa_req_id']
                    data['Action_taken_by']=data['current_ticket_owner']
                    data['Notification_Date']=""
                    data['Message']=data['visa_req_id']+" New Visa request for approval"
                    data['Notification_ID']=notificationid
                    data['organization']=data['organization']
                    serializernotificationss = NotificationSerializers(data=data)
                    if serializernotificationss.is_valid():
                        serializernotificationss.save()
                        country=Country_Master.objects.filter(country_id=employee[0]['country']).values("name")
                        if employee[0]['is_billable']==True:
                            is_billable='Yes'
                        else:
                            is_billable='No'
                        ctxt = {
                                'first_name': self.employee_name(emp_code=employee[0]['emp_email_id']),
                                'approve_first_name':self.approver_name(emp_code=data['current_ticket_owner']),
                                'project_id': employee[0]['project_id'],
                                'billable': is_billable,
                                'to_country':country[0]['name'],
                                'from_date':self.date_format(date=employee[0]['travel_start_date']),
                                'return_date':self.date_format(date=employee[0]['travel_end_date']),
                                'visa_type':employee[0]['applied_visa'],
                                'supervisor':self.employee_name(emp_code=employee[0]['supervisor']),
                                'expense_approver':self.employee_name(emp_code=employee[0]['expense_approver']),
                                'project_manager': self.employee_name(emp_code=employee[0]['project_manager']),
                                'business_lead':self.employee_name(emp_code=employee[0]['business_lead']),
                                'client_executive_lead':self.employee_name(emp_code=employee[0]['client_executive_lead'])
                        }
                        if data['current_ticket_owner'] !="":
                            template='email/approve_visa_request.html'
                            emailsubject='Visa request for '+self.employee_name(emp_code=employee[0]['emp_email_id'])+' requires approval'
                            self.sendmails(ctxt,template,emailsubject,emailto=data['current_ticket_owner'],id=data['visa_req_id'])
                        notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                        data['Entity_Type']="Visa"
                        data['Entity_ID']=data['visa_req_id']
                        data['Action_taken_by']=emp_email_id
                        data['Notification_Date']=""
                        data['Message']=data['visa_req_id']+" Visa request approved by "+data['modified_by']
                        data['Notification_ID']=notificationid
                        data['organization']=data['organization']
                       
                        serializernotifications = NotificationSerializers(data=data)
                        if serializernotifications.is_valid():
                            serializernotifications.save()
                            if current_ticket_owner !="":
                               approver_name=self.employee_name(emp_code=current_ticket_owner)
                            else:
                               approver_name="Assignment Team"
                            ctxt = {
                                'approver_name': approver_name,
                                'next_approver_name':self.employee_name(emp_code=data['current_ticket_owner']),
                                'preferred_first_name':self.approver_name(emp_code=data['Action_taken_by']),
                                'visa_request_id': data['visa_req_id'],      
                            }
                            template='email/approvedvisarequest.html'
                            emailsubject='Your visa request '+data['visa_req_id']+' have been approved'
                            self.sendmails(ctxt,template,emailsubject,emailto=employee[0]['emp_email_id'],id=data['visa_req_id'])
                elif data['approve_action']=="R":
                    visa_status=Status_Master.objects.filter(name="Rejected").values("value")
                    data['approval_level']=request.data['approval_level']
                    data['visa_status']=visa_status[0]['value']
                    data['current_ticket_owner']=request.data['current_ticket_owner']
                    notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                    data['Entity_Type']="Visa"
                    data['Entity_ID']=data['visa_req_id']
                    data['Action_taken_by']=emp_email_id
                    data['Notification_Date']=""
                    data['Message']=data['visa_req_id']+" Visa Request Rejected"
                    data['Notification_ID']=notificationid
                    data['organization']=data['organization']
                    serializernotification = NotificationSerializers(data=data)
                    if serializernotification.is_valid():
                        serializernotification.save()
                        ctxt = {
                            'approver_name': self.employee_name(emp_code=current_ticket_owner),
                            'preferred_first_name':self.approver_name(emp_code=data['Action_taken_by']),
                            'visa_request_id': data['visa_req_id'],
                            'msg': request.data['request_notes']

                        }
                        template='email/visareject.html'
                        emailsubject='Your visa request '+data['visa_req_id']+' has been rejected'
                        self.sendmails(ctxt,template,emailsubject,emailto=employee[0]['emp_email_id'],id=data['visa_req_id'])
                elif data['approve_action']=="T":
                    visa_status=Status_Master.objects.filter(name="Transferred").values("value")
                    data['approval_level']=request.data['approval_level']
                    data['visa_status']=visa_status[0]['value']
                    if data['approval_level']=="1":
                        data['expense_approver'] =data['transfer_to']
                        data['current_ticket_owner']=data['transfer_to']
                    elif data['approval_level']=="2":
                        data['project_manager'] =data['transfer_to']
                        data['current_ticket_owner']=data['transfer_to']
                    elif data['approval_level']=="3":
                        data['business_lead'] =data['transfer_to']
                        data['current_ticket_owner']=data['transfer_to']
                    elif data['approval_level']=="4":
                        data['client_executive_lead'] =data['transfer_to']
                        data['current_ticket_owner']=data['transfer_to']
                    notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                    data['Entity_Type']="Visa"
                    data['Entity_ID']=data['visa_req_id']
                    data['Action_taken_by']=data['transfer_to']
                    data['Notification_Date']=""
                    data['Message']=data['visa_req_id']+" Visa request transferred"
                    data['Notification_ID']=notificationid
                    data['organization']=data['organization']
                    serializernotificationss = NotificationSerializers(data=data)
                    if serializernotificationss.is_valid():
                        serializernotificationss.save()
                        ctxt = {
                                'approver_name': self.employee_name(emp_code=current_ticket_owner),
                                'preferred_first_name':self.approver_name(emp_code=data['Action_taken_by']),
                                'visa_request_id': data['visa_req_id'],
                                'msg': request.data['request_notes']

                        }
                        template='email/visatransferforapproval.html'
                        emailsubject='New visa request '+data['visa_req_id']+' has been transferred for your approval'
                        self.sendmails(ctxt,template,emailsubject,emailto=data['Action_taken_by'],id=data['visa_req_id'])
                        notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                        data['Entity_Type']="Visa"
                        data['Entity_ID']=data['visa_req_id']
                        data['Action_taken_by']=emp_email_id
                        data['Notification_Date']=""
                        data['Message']=data['visa_req_id']+" Visa request  transferred to "+data['current_ticket_owner']
                        data['Notification_ID']=notificationid
                        data['organization']=data['organization']
                        serializernotifications = NotificationSerializers(data=data)
                        if serializernotifications.is_valid():
                            serializernotifications.save()
                        ctxt = {
                            'approver_name': self.employee_name(emp_code=data['current_ticket_owner']),
                            'preferred_first_name':self.approver_name(emp_code=data['Action_taken_by']),
                            'visa_request_id': data['visa_req_id'],
                            'msg': request.data['request_notes']

                        }
                        template='email/visatransfer.html'
                        emailsubject='Your visa request '+data['visa_req_id']+' has been transferred to '+self.employee_name(emp_code=data['current_ticket_owner'])
                        self.sendmails(ctxt,template,emailsubject,emailto=emp_email_id,id=data['visa_req_id'])
                if data['take_ownership']:

                    if data['approve_action']=="":
                        data['current_ticket_owner']=data['take_ownership']
                        notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                        data['Entity_Type']="Visa"
                        data['Entity_ID']=data['visa_req_id']
                        data['Action_taken_by']=emp_email_id
                        data['Notification_Date']=""
                        data['Message']=data['visa_req_id']+" Visa request assigned to "+data['current_ticket_owner']
                        data['Notification_ID']=notificationid
                        data['organization']=data['organization']
                        serializernotifications = NotificationSerializers(data=data)
                        if serializernotifications.is_valid():
                            serializernotifications.save()
                            msg="Visa request assigned"
                            self.sendmails(msg,data['Message'],data['Action_taken_by'])
                if data['approve_action']=="U":
                    data['current_ticket_owner']=data['take_ownership']

                visa_request_ids=Visa_Request.objects.filter(visa_req_id=data['visa_req_id']).first()
                serializer = Visa_RequestSerializers(visa_request_ids,data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    #print(serializer.errors)
                    dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data': serializer.errors}
                if request.data['approve_action']=="A":
                    visa_status=Status_Master.objects.filter(name="Approved").values("value")
                    data['action']="4"
                else:
                    data['action']=visa_status[0]['value']
                data['action_notes']=request.data['request_notes']
                data['email']=current_ticket_owner
                data['visa_req_id']=data['visa_req_id']
                data['organization']=data['organization']
                # subject = 'Request Update'
                # message = ''
                # html_message = '<h3>Your Request Hasapproved By:</h3>'
                # html_message += '<p> User Name <b>: '+current_ticket_owner+'</b> </p>'
                # #html_message += '<p>User Name : <b>' +password+ '</b> </p>'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [emp_email_id,current_ticket_owner,]
                # send_mail(subject, message, email_from, recipient_list, fail_silently=False, html_message=html_message)
                data['approval_level']=request.data['approval_level']
                data['email_id']=request.data['modified_by']
                print(data['email_id'])
                actionserializer =Visa_Request_Action_HistorySerializers(data=data)
                if actionserializer.is_valid():
                    actionserializer.save()
                    dict = {'massage code': '200', 'massage': 'successful', 'status': True}
                else:
                    dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data': actionserializer.errors}
        else:
            dict = {'massage code': '200', 'massage': 'successful', 'status': True}
        return Response(dict, status=status.HTTP_200_OK)


    def sendmails(self,ctxt,template,emailsubject,emailto,id):
        #Action_taken_by=Action_taken_by
        #"rahulr@triazinesoft.com"
        ctxt = ctxt
        template=template
        travel_req_id=id
        emailsubject=emailsubject
        emp_code=Employee.objects.filter(emp_code=emailto).values('email','preferred_first_name','first_name','last_name')
        print(emp_code)
        if emp_code[0]['email']:
            toemail=emp_code[0]['email']
        else:
            toemail=""
        subject, from_email, to = emailsubject,'',toemail
        print(toemail)
        html_content = render_to_string(template, ctxt)
        print(html_content)
        # render with dynamic value
        text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

        # create the email, and attach the HTML version as well.

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


    def approver_name(self,emp_code):
        if emp_code:
            emp_code=Employee.objects.filter(emp_code=emp_code).values('emp_code','preferred_first_name','first_name','last_name')
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
    def employee_name(self,emp_code):
        if emp_code:
            emp_code=Employee.objects.filter(emp_code=emp_code).values('emp_code','preferred_first_name','first_name','last_name')
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
            name=''
            return name
    def date_format(self,date):
        print(date)
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        date=str(date)[0:19]
        # utc = datetime.utcnow()
        utc = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        # Tell the datetime object that it's in UTC time zone since 
        # datetime objects are 'naive' by default
        utc = utc.replace(tzinfo=from_zone)
        # Convert time zone
        central = utc.astimezone(to_zone)
        string=str(central)
        demo= string[0:10].split("-")
        new_case_date = demo[2]+"/"+demo[1]+"/"+demo[0]
        return new_case_date


class assignment_travel_request_status(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Assignment_Travel_Request_StatusSerializers
    def get(self, request):
        travel_requests=Assignment_Travel_Request_Status.objects.filter(travel_req_id=request.GET["travel_req_id"],organization=request.GET["org_id"])
        travel_request_dependent=Assignment_Travel_Request_StatusSerializers(travel_requests,many=True)
        dict = {'massage': 'data found', 'status': True, 'data': travel_request_dependent.data}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)
    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()


        try:
            ditsct=[]
            for data in request.data:
                if data['update_id']:

                    ditsct.append(data['update_id'])
                    assignments=Assignment_Travel_Request_Status.objects.filter(id=data['update_id']).first()
                    assignment_update=Assignment_Travel_Request_StatusSerializers(assignments,data=data)
                    if assignment_update.is_valid():
                        assignment_update.save()
                        dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data':ditsct}
                    else:
                        dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data':assignment_update.errors}
                else:
                    assignment_travel=Assignment_Travel_Request_StatusSerializers(data=data)
                    if assignment_travel.is_valid():
                        assignment_travel.save()
                        dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data':data['travel_req_id']}
                    else:
                        dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data':assignment_travel.errors}
            return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            dict = {'massage code': 'already exists', 'massage': 'unsuccessful', 'status': False,data:str(e)}
            return Response(dict, status=status.HTTP_200_OK)

class assignment_travel_request_status(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = Assignment_Travel_Request_StatusSerializers
    def get(self, request):
        travel_requests=Assignment_Travel_Request_Status.objects.filter(travel_req_id=request.GET["travel_req_id"],organization=request.GET["org_id"])
        travel_request_dependent=Assignment_Travel_Request_StatusSerializers(travel_requests,many=True)
        dict = {'massage': 'data found', 'status': True, 'data': travel_request_dependent.data}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)
    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()


        try:
            ditsct=[]
            for data in request.data:
                if data['update_id']:

                    ditsct.append(data['update_id'])
                    assignments=Assignment_Travel_Request_Status.objects.filter(id=data['update_id']).first()
                    assignment_update=Assignment_Travel_Request_StatusSerializers(assignments,data=data)
                    if assignment_update.is_valid():
                        assignment_update.save()
                        notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                        data['Entity_Type']="Travel"
                        data['Entity_ID']=data['travel_req_id']
                        data['Action_taken_by']="employee@gmail.com"
                        data['Notification_Date']=""
                        data['Message']="Updated by Assignment"
                        data['Notification_ID']=notificationid
                        serializernotification = NotificationSerializers(data=data)
                        if serializernotification.is_valid():
                            serializernotification.save()
                        dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data':ditsct}
                    else:
                        dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data':assignment_update.errors}
                else:
                    assignment_travel=Assignment_Travel_Request_StatusSerializers(data=data)
                    if assignment_travel.is_valid():
                        assignment_travel.save()
                        notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                        data['Entity_Type']="Travel"
                        data['Entity_ID']=data['travel_req_id']
                        data['Action_taken_by']="employee@gmail.com"
                        data['Notification_Date']=""
                        data['Message']="Approved by Assignment"
                        data['Notification_ID']=notificationid
                        serializernotification = NotificationSerializers(data=data)
                        if serializernotification.is_valid():
                            serializernotification.save()
                        dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data':data['travel_req_id']}
                    else:
                        dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data':assignment_travel.errors}
            return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            dict = {'massage code': 'already exists', 'massage': 'unsuccessful', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)


class assignment_travel_tax_grid(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = Assignment_Travel_Tax_GridSerializers
    def get(self, request):
        travel_requests=Assignment_Travel_Tax_Grid.objects.filter(travel_req_id=request.GET["travel_req_id"],organization=request.GET["org_id"])
        travel_request_dependent=Assignment_Travel_Tax_GridSerializers(travel_requests,many=True)
        dict = {'massage': 'data found', 'status': True, 'data': travel_request_dependent.data}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)
    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()


        try:
            ditsct=[]
            for data in request.data:
                if data['update_id']:

                    ditsct.append(data['update_id'])
                    assignments=Assignment_Travel_Tax_Grid.objects.filter(id=data['update_id']).first()
                    assignment_update=Assignment_Travel_Tax_GridSerializers(assignments,data=data)
                    if assignment_update.is_valid():
                        assignment_update.save()
                        dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data':ditsct}
                    else:
                        dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data':assignment_update.errors}
                else:
                    assignment_travel=Assignment_Travel_Tax_GridSerializers(data=data)
                    if assignment_travel.is_valid():
                        assignment_travel.save()
                        dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data':data['travel_req_id']}
                    else:
                        dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data':assignment_travel.errors}
            return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            dict = {'massage code': 'already exists', 'massage': 'unsuccessful', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)

class get_org_count_travel_requests(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Travel_RequestSerializers
    # Get all visa_purpose
    def get(self, request):
        travel= Travel_Request.objects.filter(travel_req_status="2",organization_id=request.GET['org_id']).count()
        if travel:
            travel=travel
        else:
            travel=""

        travels= Travel_Request.objects.filter(travel_req_status="5",organization_id=request.GET['org_id']).count()
        if travels:
            travels=travels
        else:
            travels=""
        travelss= Travel_Request.objects.filter(travel_req_status="3",organization_id=request.GET['org_id']).count()
        if travelss:
            travelss=travelss
        else:
            travelss=""
        #travels= Travel_Request.objects.filter(travel_req_status="2",current_ticket_owner="").count()

        dict = {"status": True, "message":MSG_SUCESS, "Inprogress":travel,"Rejected":travels,"Closed":travelss}
        return Response(dict, status=status.HTTP_200_OK)


class assignment_post_approve_travelvisa_request(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Travel_RequestSerializers
    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()
        if request.data.get('travel_req_id'):
            try:
                print(request.data['travel_req_id'])
                notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                travel_request_id= request.data['travel_req_id']
                travel_request_id=Travel_Request.objects.filter(travel_req_id=request.data.get('travel_req_id'),organization_id=request.data.get('org_id')).first()
                employee=Travel_Request.objects.filter(travel_req_id=request.data.get('travel_req_id')).values('supervisor','business_lead','project_manager','expense_approver','client_executive_lead','emp_email_id')
                supervisor=employee[0]['supervisor']
                business_lead=employee[0]['business_lead']
                project_manager=employee[0]['project_manager']
                expense_approver=employee[0]['expense_approver']
                client_executive_lead=employee[0]['client_executive_lead']
                current_ticket_owner= request.data['current_ticket_owner']
                emp_email_id= employee[0]['emp_email_id']

                request.data['current_ticket_owner']=""
                if  current_ticket_owner==supervisor:
                    request.data['current_ticket_owner'] = employee[0]['expense_approver']
                if  current_ticket_owner==expense_approver:
                    if expense_approver==project_manager:
                        request.data['current_ticket_owner'] =employee[0]['business_lead']
                    elif expense_approver==business_lead:
                        request.data['current_ticket_owner'] =employee[0]['client_executive_lead']
                    elif expense_approver==client_executive_lead:
                        request.data['current_ticket_owner'] =""
                    else:
                        request.data['current_ticket_owner'] = employee[0]['project_manager']
                elif current_ticket_owner ==project_manager:
                    if project_manager==expense_approver:
                        request.data['current_ticket_owner'] =employee[0]['business_lead']
                    if project_manager==business_lead:
                        request.data['current_ticket_owner'] =employee[0]['client_executive_lead']
                    elif project_manager==client_executive_lead:
                        request.data['current_ticket_owner'] =""
                    else:
                        request.data['current_ticket_owner'] =employee[0]['business_lead']
                elif current_ticket_owner ==business_lead:
                    if business_lead==expense_approver:
                        request.data['current_ticket_owner'] =employee[0]['client_executive_lead']
                    if business_lead==project_manager:
                        request.data['current_ticket_owner'] =employee[0]['client_executive_lead']
                    elif business_lead==client_executive_lead:
                        request.data['current_ticket_owner'] =""
                    else:
                        request.data['current_ticket_owner'] =employee[0]['client_executive_lead']
                elif current_ticket_owner==client_executive_lead:
                    if client_executive_lead==expense_approver:
                        request.data['current_ticket_owner'] =""
                    if client_executive_lead==project_manager:
                        request.data['current_ticket_owner'] =""
                    elif client_executive_lead==business_lead:
                        request.data['current_ticket_owner'] =""
                    else:
                        request.data['current_ticket_owner'] =""
                    request.data['travel_req_status']="4"
                if request.data['approve_action']=="A":
                    travel_req_status=Status_Master.objects.filter(name="Approved").values("value")
                    request.data['travel_req_status']="2"
                    request.data['Entity_Type']="Travel"
                    request.data['Entity_ID']=request.data['travel_req_id']
                    request.data['Action_taken_by']=request.data['current_ticket_owner']
                    request.data['Notification_Date']=""
                    request.data['Message']=request.data['travel_req_id']+" New travel request for approval"
                    request.data['Notification_ID']=notificationid
                    request.data['organization']=request.data['org_id']
                    serializernotificationss = NotificationSerializers(data=request.data)
                    if serializernotificationss.is_valid():
                        serializernotificationss.save()
                        msg="New  travel request for approval"
                        self.sendmails(msg,request.data['Message'],request.data['Action_taken_by'])
                        notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                        request.data['Entity_Type']="Travel"
                        request.data['Entity_ID']=request.data['travel_req_id']
                        request.data['Action_taken_by']=emp_email_id
                        request.data['Notification_Date']=""
                        request.data['Message']=request.data['travel_req_id']+" Travel request approved by "+request.data['modified_by']
                        request.data['Notification_ID']=notificationid
                        request.data['organization']=request.data['org_id']
                        serializernotifications = NotificationSerializers(data=request.data)
                        if serializernotifications.is_valid():
                            serializernotifications.save()
                            msg="Travel request  approved"
                            self.sendmails(msg,request.data['Message'],request.data['Action_taken_by'])
                elif request.data['approve_action']=="R":
                    travel_req_status=Status_Master.objects.filter(name="Rejected").values("value")
                    request.data['travel_req_status']=travel_req_status[0]['value']
                    request.data['current_ticket_owner']=current_ticket_owner
                    request.data['Entity_Type']="Travel"
                    request.data['Entity_ID']=request.data['travel_req_id']
                    request.data['Action_taken_by']=emp_email_id
                    request.data['Notification_Date']=""
                    request.data['Message']=request.data['travel_req_id']+" Travel Request Rejected"
                    request.data['Notification_ID']=notificationid
                    request.data['organization']=request.data['org_id']
                    serializernotification = NotificationSerializers(data=request.data)
                    if serializernotification.is_valid():
                        serializernotification.save()
                        msg="Travel Request Rejected"
                        self.sendmails(msg,request.data['Message'],request.data['Action_taken_by'])
                elif request.data['approve_action']=="T":
                    travel_req_status=Status_Master.objects.filter(name="Transferred").values("value")
                    request.data['travel_req_status']=travel_req_status[0]['value']
                    if request.data['current_ticket_owner']==expense_approver:
                        request.data['expense_approver'] = request.data['transfer_to']
                        request.data['current_ticket_owner']=request.data['transfer_to']
                    elif request.data['current_ticket_owner'] ==project_manager:
                        request.data['project_manager'] =request.data['transfer_to']
                        request.data['current_ticket_owner']=request.data['transfer_to']
                    elif request.data['current_ticket_owner'] ==business_lead:
                        request.data['business_lead'] =request.data['transfer_to']
                        request.data['current_ticket_owner']=request.data['transfer_to']
                    elif request.data['current_ticket_owner']==client_executive_lead:
                        request.data['client_executive_lead'] =request.data['transfer_to']
                        request.data['current_ticket_owner']=request.data['transfer_to']
                    request.data['Entity_Type']="Travel"
                    request.data['Entity_ID']=request.data['travel_req_id']
                    request.data['Action_taken_by']=request.data['transfer_to']
                    request.data['Notification_Date']=""
                    request.data['Message']=request.data['travel_req_id']+" Travel request transferred"
                    request.data['Notification_ID']=notificationid
                    request.data['organization']=request.data['org_id']
                    serializernotificationss = NotificationSerializers(data=request.data)
                    if serializernotificationss.is_valid():
                        serializernotificationss.save()
                        msg="Travel request  transferred"
                        self.sendmails(msg,request.data['Message'],request.data['Action_taken_by'])
                        notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                        request.data['Entity_Type']="Travel"
                        request.data['Entity_ID']=request.data['travel_req_id']
                        request.data['Action_taken_by']=emp_email_id
                        request.data['Notification_Date']=""
                        request.data['Message']=request.data['travel_req_id']+" Travel request transferred to "+request.data['current_ticket_owner']
                        request.data['Notification_ID']=notificationid
                        request.data['organization']=request.data['org_id']
                        serializernotifications = NotificationSerializers(data=request.data)
                        if serializernotifications.is_valid():
                            serializernotifications.save()
                            msg="Travel request  transferred"
                            self.sendmails(msg,request.data['Message'],request.data['Action_taken_by'])
                if request.data['take_ownership']:
                    request.data['current_ticket_owner']=request.data['take_ownership']
                    notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                    request.data['Entity_Type']="Travel"
                    request.data['Entity_ID']=request.data['travel_req_id']
                    request.data['Action_taken_by']=emp_email_id
                    request.data['Notification_Date']=""
                    request.data['Message']=request.data['travel_req_id']+" Travel request Assigned to "+request.data['current_ticket_owner']
                    request.data['Notification_ID']=notificationid
                    request.data['organization']=request.data['org_id']
                    serializernotifications = NotificationSerializers(data=request.data)
                    if serializernotifications.is_valid():
                        serializernotifications.save()
                        msg="Travel request  assigned"
                        self.sendmails(msg,request.data['Message'],request.data['Action_taken_by'])
                travel_request_id_ids=Travel_Request.objects.filter(travel_req_id=request.data['travel_req_id']).first()
                serializer = Travel_RequestSerializers(travel_request_id_ids,data=request.data)
                if serializer.is_valid():
                    serializer.save()

                else:
                    dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data':  serializer.errors}
                if request.data['approve_action']=="A":
                    travel_req_status=Status_Master.objects.filter(name="Approved").values("value")
                    request.data['action']="4"
                else:
                    request.data['action']=request.data['travel_req_status']
                request.data['action_notes']=request.data['request_notes']
                request.data['email']=current_ticket_owner
                request.data['module']=request.data['module']
                request.data['travel_req_id_id']=request.data['travel_req_id']
                request.data['organization']=request.data['org_id']
                subject = 'Request Update'
                message = ''
                html_message = '<h3>Your Request Hasapproved By:</h3>'
                html_message += '<p> User Name <b>: '+current_ticket_owner+'</b> </p>'
                #html_message += '<p>User Name : <b>' +password+ '</b> </p>'
                email_from = settings.EMAIL_HOST_USER
                emp_code=Employee.objects.filter(emp_code=emp_email_id).values('email','preferred_first_name','first_name','last_name')
                print(emp_code)
                if emp_code:
                    emp_email_id=emp_code[0]['email']
                else:
                    emp_email_id=""
                emp_codes=Employee.objects.filter(emp_code=current_ticket_owner).values('email','preferred_first_name','first_name','last_name')
                print(emp_code)
                if emp_codes:
                    current_ticket_owner=emp_codes[0]['email']
                else:
                    current_ticket_owner=""
                recipient_list = [emp_email_id,current_ticket_owner,]
                send_mail(subject, message, email_from, recipient_list, fail_silently=False, html_message=html_message)
                serializeraction=Travel_Request_Action_HistorySerializers(data=request.data)
                if serializeraction.is_valid():
                    serializeraction.save()
                    dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data':  request.data['travel_req_id']}
                else:
                    dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data':  serializeraction.errors}
            except:
                dict = {'massage code': '200', 'massage': 'Invalid Data', 'status': False}
        else:
            #try:
            visa_request_id=Visa_Request.objects.filter(visa_req_id=request.data['visa_req_id']).first()
            employee=Visa_Request.objects.filter(visa_req_id=request.data['visa_req_id']).values('supervisor','business_lead','project_manager','expense_approver','client_executive_lead','emp_email_id')

            supervisor=employee[0]['supervisor']
            business_lead=employee[0]['business_lead']
            project_manager=employee[0]['project_manager']
            expense_approver=employee[0]['expense_approver']
            client_executive_lead=employee[0]['client_executive_lead']
            current_ticket_owner= request.data['current_ticket_owner']
            emp_email_id=employee[0]['emp_email_id']
            request.data['current_ticket_owner'] =""
            if  current_ticket_owner==supervisor:
                request.data['current_ticket_owner'] = employee[0]['expense_approver']
            elif  current_ticket_owner==expense_approver:
                if expense_approver==project_manager:
                    request.data['current_ticket_owner'] =employee[0]['business_lead']
                elif expense_approver==business_lead:
                    request.data['current_ticket_owner'] =employee[0]['client_executive_lead']
                elif expense_approver==client_executive_lead:
                    request.data['current_ticket_owner'] =""
                else:
                    request.data['current_ticket_owner'] = employee[0]['project_manager']
            elif current_ticket_owner ==project_manager:
                if project_manager==expense_approver:
                    request.data['current_ticket_owner'] =employee[0]['business_lead']
                if project_manager==business_lead:
                    request.data['current_ticket_owner'] =employee[0]['client_executive_lead']
                elif project_manager==client_executive_lead:
                    request.data['current_ticket_owner'] =""
                else:
                    request.data['current_ticket_owner'] =employee[0]['business_lead']
            elif current_ticket_owner ==business_lead:
                if business_lead==expense_approver:
                    request.data['current_ticket_owner'] =employee[0]['client_executive_lead']
                if business_lead==project_manager:
                    request.data['current_ticket_owner'] =employee[0]['client_executive_lead']
                elif business_lead==client_executive_lead:
                    request.data['current_ticket_owner'] =""
                else:
                    request.data['current_ticket_owner'] =employee[0]['client_executive_lead']
            elif current_ticket_owner==client_executive_lead:
                if client_executive_lead==expense_approver:
                    request.data['current_ticket_owner'] =""
                if client_executive_lead==project_manager:
                    request.data['current_ticket_owner'] =""
                elif client_executive_lead==business_lead:
                    request.data['current_ticket_owner'] =""
                else:
                    request.data['current_ticket_owner'] =""
            if request.data['approve_action']=="A":
                request.data['visa_status']="2"
                request.data['Entity_Type']="Visa"
                notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                request.data['Entity_ID']=request.data['visa_req_id']
                request.data['Action_taken_by']=request.data['current_ticket_owner']
                request.data['Notification_Date']=""
                request.data['Message']=request.data['visa_req_id']+" New Visa request for approval"
                request.data['Notification_ID']=notificationid
                request.data['organization']=request.data['org_id']
                serializernotificationss = NotificationSerializers(data=request.data)
                if serializernotificationss.is_valid():
                    serializernotificationss.save()
                    msg="New  Visa request for approval"
                    self.sendmails(msg,request.data['Message'],request.data['Action_taken_by'])
                    notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                    request.data['Entity_Type']="Visa"
                    request.data['Entity_ID']=request.data['visa_req_id']
                    request.data['Action_taken_by']=emp_email_id
                    request.data['Notification_Date']=""
                    request.data['Message']=request.data['visa_req_id']+" Visa request approved by "+request.data['modified_by']
                    request.data['Notification_ID']=notificationid
                    request.data['organization']=request.data['org_id']
                    serializernotifications = NotificationSerializers(data=request.data)
                    if serializernotifications.is_valid():
                        serializernotifications.save()
                        msg="Visa request  approved"
                        self.sendmails(msg,request.data['Message'],request.data['Action_taken_by'])
            elif request.data['approve_action']=="R":
                visa_status=Status_Master.objects.filter(name="Rejected").values("value")
                request.data['visa_status']=visa_status[0]['value']
                request.data['current_ticket_owner']=current_ticket_owner
                notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                request.data['Entity_Type']="Visa"
                request.data['Entity_ID']=request.data['visa_req_id']
                request.data['Action_taken_by']=emp_email_id
                request.data['Notification_Date']=""
                request.data['Message']=request.data['visa_req_id']+" Visa Request Rejected"
                request.data['Notification_ID']=notificationid
                request.data['organization']=request.data['org_id']
                serializernotification = NotificationSerializers(data=request.data)
                print(request.data['Action_taken_by'])
                if serializernotification.is_valid():
                    serializernotification.save()
                    msg="Visa Request Rejected"
                    self.sendmails(msg,request.data['Message'],request.data['Action_taken_by'])
            elif request.data['approve_action']=="T":
                visa_status=Status_Master.objects.filter(name="Transferred").values("value")
                #print(visa_status)
                request.data['visa_status']=visa_status[0]['value']
                if request.data['current_ticket_owner']==supervisor:
                    request.data['supervisor'] = request.data['transfer_to']
                    request.data['current_ticket_owner']=request.data['transfer_to']
                elif request.data['current_ticket_owner'] ==expense_approver:
                    request.data['expense_approver'] =request.data['transfer_to']
                    request.data['current_ticket_owner']=request.data['transfer_to']
                elif request.data['current_ticket_owner'] ==project_manager:
                    request.data['project_manager'] =request.data['transfer_to']
                    request.data['current_ticket_owner']=request.data['transfer_to']
                elif request.data['current_ticket_owner'] ==business_lead:
                    request.data['business_lead'] =request.data['transfer_to']
                    request.data['current_ticket_owner']=request.data['transfer_to']
                elif request.data['current_ticket_owner']==client_executive_lead:
                    request.data['client_executive_lead'] =request.data['transfer_to']
                    request.data['current_ticket_owner']=request.data['transfer_to']
                notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                request.data['Entity_Type']="Visa"
                request.data['Entity_ID']=request.data['visa_req_id']
                request.data['Action_taken_by']=request.data['transfer_to']
                request.data['Notification_Date']=""
                request.data['Message']=request.data['visa_req_id']+" Visa request transferred"
                request.data['Notification_ID']=notificationid
                request.data['organization']=request.data['org_id']
                serializernotificationss = NotificationSerializers(data=request.data)
                if serializernotificationss.is_valid():
                    serializernotificationss.save()
                    msg="Visa request transfered"
                    self.sendmails(msg,request.data['Message'],request.data['Action_taken_by'])
                    notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                    request.data['Entity_Type']="Visa"
                    request.data['Entity_ID']=request.data['visa_req_id']
                    request.data['Action_taken_by']=emp_email_id
                    request.data['Notification_Date']=""
                    request.data['Message']=request.data['visa_req_id']+" Visa request  transferred to "+request.data['current_ticket_owner']
                    request.data['Notification_ID']=notificationid
                    request.data['organization']=request.data['org_id']
                    serializernotifications = NotificationSerializers(data=request.data)
                    if serializernotifications.is_valid():
                        serializernotifications.save()
                        msg="Visa request transfered"
                        self.sendmails(msg,request.data['Message'],request.data['Action_taken_by'])
            if request.data['take_ownership']:
                
                if request.data['approve_action']=="":
                    request.data['current_ticket_owner']=request.data['take_ownership']
                    notificationid="NOTIF"+str(uuid.uuid4().int)[:6]
                    request.data['Entity_Type']="Visa"
                    request.data['Entity_ID']=request.data['visa_req_id']
                    request.data['Action_taken_by']=emp_email_id
                    request.data['Notification_Date']=""
                    request.data['Message']=request.data['visa_req_id']+" Visa request assigned to "+request.data['current_ticket_owner']
                    request.data['Notification_ID']=notificationid
                    request.data['organization']=request.data['org_id']
                    serializernotifications = NotificationSerializers(data=request.data)
                    if serializernotifications.is_valid():
                        serializernotifications.save()
                        msg="Visa request assigned"
                        self.sendmails(msg,request.data['Message'],request.data['Action_taken_by'])
            if request.data['approve_action']=="U":
                request.data['current_ticket_owner']=request.data['take_ownership']  
            visa_request_ids=Visa_Request.objects.filter(visa_req_id=request.data['visa_req_id']).first()
            serializer = Visa_RequestSerializers(visa_request_ids,data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)
                dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data': serializer.errors}
            if request.data['approve_action']=="A":
                visa_status=Status_Master.objects.filter(name="Approved").values("value")
                request.data['action']="4"
            else:
                visa_status=Status_Master.objects.filter(name="Approved").values("value")
                request.data['action']=visa_status[0]['value']
            request.data['action_notes']=request.data['request_notes']
            request.data['email']=current_ticket_owner
            request.data['visa_req_id_id']=request.data['visa_req_id']
            request.data['organization']=request.data['org_id']
            subject = 'Request Update'
            message = ''
            html_message = '<h3>Your Request Hasapproved By:</h3>'
            html_message += '<p> User Name <b>: '+current_ticket_owner+'</b> </p>'
            #html_message += '<p>User Name : <b>' +password+ '</b> </p>'
            email_from = settings.EMAIL_HOST_USER
            emp_code=Employee.objects.filter(emp_code=emp_email_id).values('email','preferred_first_name','first_name','last_name')
            
            if emp_code:
                emp_email_id=emp_code[0]['email']
            else:
                emp_email_id=""
            emp_codes=Employee.objects.filter(emp_code=current_ticket_owner).values('email','preferred_first_name','first_name','last_name')
            
            if emp_codes:
                current_ticket_owner=emp_codes[0]['email']
            else:
                current_ticket_owner=""
            recipient_list = [emp_email_id,current_ticket_owner,]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False, html_message=html_message)
            actionserializer =Visa_Request_Action_HistorySerializers(data=request.data)
            if actionserializer.is_valid():
                actionserializer.save()
                dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data': request.data['visa_req_id']}
            else:
                dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data': actionserializer.errors}
            # except:
            #     dict = {'massage code': '200', 'massage': 'Invalid id', 'status': False}
        return Response(dict, status=status.HTTP_200_OK)


    def sendmails(self,msg,Message,Action_taken_by):
        emp_code=Employee.objects.filter(emp_code=Action_taken_by).values('email','preferred_first_name','first_name','last_name')
        print(emp_code)
        if emp_code:
            Action_taken_by=emp_code[0]['email']
        else:
            Action_taken_by=""
        #Action_taken_by=Action_taken_by
        #"rahulr@triazinesoft.com"
        Message = Message
        #"123456"
        subject = msg
        message = ''
        html_message = '<h3>'+Message+'</h3>'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [Action_taken_by]
        send_mail(subject, message, email_from, recipient_list, fail_silently=False, html_message=html_message)


class org_travel_requests(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Travel_RequestSerializers
    def get(self, request):
        travel_request_count= Travel_Request.objects.filter(organization_id=request.GET['org_id']).count()
        if travel_request_count:
            travel_request_count=travel_request_count
        else:
            travel_request_count=""
        travel_request= Travel_Request.objects.filter(travel_req_status=request.GET['travel_req_status'],organization_id=request.GET['org_id']).values("travel_req_id")
        alldata=[]
        print(travel_request)
        if travel_request:
            for data in travel_request:
                travel_request=Travel_Request.objects.filter(travel_req_id=data['travel_req_id'])
                travel_requests = Travel_RequestSerializers(travel_request,many=True)
                emp_code=Employee.objects.filter(emp_code=travel_requests.data[0]['emp_email']).values('emp_code','first_name','last_name')
                if emp_code[0]['emp_code']:
                    travel_requests.data[0]['emp_code']=emp_code[0]['emp_code']
                else:
                    travel_requests.data[0]['emp_code']=""
                if emp_code[0]['first_name']:
                    travel_requests.data[0]['first_name']=emp_code[0]['first_name']
                else:
                    travel_requests.data[0]['first_name']=""

                if emp_code[0]['last_name']:
                    travel_requests.data[0]['last_name']=emp_code[0]['last_name']
                else:
                    travel_requests.data[0]['last_name']=""
                emp_codes=Employee.objects.filter(emp_code=travel_requests.data[0]['current_ticket_owner']).values('email','first_name','last_name')
                if emp_codes:
                    travel_requests.data[0]['current_ticket_owner']=emp_codes[0]['email']
                else:
                    travel_requests.data[0]['current_ticket_owner']=""
                visa_requests=Visa_Request.objects.filter(travel_req_id=data['travel_req_id']).values("visa_req_id")
                travel_requests.data[0]['visa_requests']=visa_requests
                travel_request_detail=Travel_Request_Details.objects.filter(travel_req_id=travel_requests.data[0]['travel_req_id']).values('id','travel_req_id_id','travelling_country', 'travelling_country_to','office_location','client_number','organization','source_city','destination_city','departure_date','return_date','is_accmodation_required','accmodation_start_date','accmodation_end_date','travel_purpose','assignment_type','applicable_visa','visa_number','visa_expiry_date','host_hr_name','host_country_head','host_attorney','host_phone_no','is_client_location','client_name','client_address','hotel_cost','per_diem_cost','airfare_cost','transportation_cost','total_cost','travel_request_status','travel_request_status_notes','is_dependent',)
                #travel_request_detail=Travel_RequestSerializers(travel_request_detail,many=True)
                travel_requests.data[0]['details']=travel_request_detail
                travel_request_dependent=Travel_Request_Dependent.objects.filter(travel_req_id=travel_requests.data[0]['travel_req_id'])
                travel_request_dependent=Travel_Request_DependentSerializers(travel_request_dependent,many=True)
                travel_requests.data[0]['dependent']=travel_request_dependent.data
                alldata.append(travel_requests.data[0])
            dict = {'massage': 'data found', 'status': True, 'data': alldata,'total':travel_request_count}
            # responseList = [dict]
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {"status": False,"status_code":200, "message":"Data Not Found",'data':[]}
            return Response(dict, status=status.HTTP_200_OK)


class delete_save(APIView):

    def get(self,request, *args, **kwargs):

        travel=Travel_Request_Draft.objects.filter(travel_req_id=request.GET['travel_req_id'])
        travel.delete()
        travels=Travel_Request_Details_Draft.objects.filter(travel_req_id=request.GET['travel_req_id'])
        travels.delete()
        travelss=Travel_Request_Dependent_Draft.objects.filter(travel_req_id=request.GET['travel_req_id'])
        travelss.delete()
        dict = {'massage': 'Deleted', 'status': True}

        #dict = {'massage': 'data found', 'status': True, 'data': travel_request_serializer.data[0] }
        return Response(dict, status=status.HTTP_200_OK)



class get_upcoming_travel_request(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Travel_RequestSerializers

    def get_queryset(self,emp_email,org_id):
        try:
            t = date.today()
            print(t)
            travel_request= Travel_Request.objects.filter(date_created__gte=t,emp_email=emp_email,organization_id=org_id).order_by('-date_modified')

        # print(visa)
        except Travel_Request.DoesNotExist:

            return []
        return travel_request


    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        travel_request = self.get_queryset(request.GET["emp_email"],request.GET["org_id"])
        
        alldata=[]
        for data in travel_request:
            travel_requests=Travel_Request.objects.filter(travel_req_id=data)
            travel_requests = Travel_RequestSerializers(travel_requests,many=True)
            emp_code=Employee.objects.filter(emp_code=travel_requests.data[0]['emp_email']).values('emp_code','first_name','last_name')
            if emp_code[0]['emp_code']:
                travel_requests.data[0]['emp_code']=emp_code[0]['emp_code']
            else:
                travel_requests.data[0]['emp_codess']=""
            if emp_code[0]['first_name']:
                travel_requests.data[0]['first_name']=emp_code[0]['first_name']
            else:
                travel_requests.data[0]['first_name']=""

            if emp_code[0]['last_name']:
                travel_requests.data[0]['last_name']=emp_code[0]['last_name']
            else:
                travel_requests.data[0]['last_name']=""
            emp_codes=Employee.objects.filter(emp_code=travel_requests.data[0]['current_ticket_owner']).values('email')
            if emp_codes:
                travel_requests.data[0]['current_ticket_owner']=emp_codes[0]['email']
            else:
                travel_requests.data[0]['current_ticket_owner']=""
            #visa_requests=Visa_Request.objects.filter(travel_req_id=data).values("visa_req_id")
            #travel_requests.data[0]['visa_requests']=visa_requests
            travel_request_details=Travel_Request_Details.objects.filter(travel_req_id_id=data).values('id','travel_req_id_id','travelling_country', 'travelling_country_to','office_location','client_number','organization','source_city','destination_city','departure_date','return_date','is_accmodation_required','accmodation_start_date','accmodation_end_date','travel_purpose','assignment_type','applicable_visa','visa_number','visa_expiry_date','host_hr_name','host_country_head','host_attorney','host_phone_no','is_client_location','client_name','client_address','hotel_cost','per_diem_cost','airfare_cost','transportation_cost','total_cost','travel_request_status','travel_request_status_notes','is_dependent',)
            #print(travel_request_details)
            #travel_request_detail_serializers=Travel_RequestSerializers(travel_request_details,many=True)
            travel_requests.data[0]['details']=travel_request_details
            travel_request_dependent=Travel_Request_Dependent.objects.filter(travel_req_id_id=travel_requests.data[0]['travel_req_id'])
            travel_request_dependent=Travel_Request_DependentSerializers(travel_request_dependent,many=True)
            travel_requests.data[0]['dependent']=travel_request_dependent.data
            alldata.append(travel_requests.data[0])
        dict = {'massage': 'data found', 'status': True, 'data': alldata}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)




##############################
'Encrypt data'
###############################

def encryptDtata(data):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    # data = str(data)
    encMessage = fernet.encrypt(data.encode())
    custom_token = encMessage
    custom_token_ = str(custom_token)+"["+str(key)+"]"
    # custom_token_ = encode(data,"password")
    return custom_token_



##################################################
# approve and reject travel request bget data
##################################################

def approved_Reject_Travel_get_data(travel_req_id,org_id):
    travel_request = Travel_Request.objects.filter(travel_req_id=travel_req_id,
                                                   organization_id=org_id)

    travel_request_serializer = Travel_RequestSerializers(travel_request, many=True)

    if travel_request_serializer.data:
        visa_requests = Visa_Request.objects.filter(travel_req_id=travel_req_id).values(
            "visa_req_id")
        if visa_requests:
            travel_request_serializer.data[0]['visa_requests'] = visa_requests
        else:
            travel_request_serializer.data[0]['visa_requests'] = ""

        travel_data = {
                'travel_req_status':travel_request_serializer.data[0]['travel_req_status'],
                'approval_level':travel_request_serializer.data[0]['approval_level'],
                'current_ticket_owner':travel_request_serializer.data[0]['current_ticket_owner'],
                'take_ownership':'',
                'transfer_to':'',
                'module':'Travel',
                'travel_req_id':travel_req_id,
                'org_id':org_id,
                'modified_by': travel_request_serializer.data[0]['current_ticket_owner']
        }

    return travel_data


################################
# appreve and reject by mail
################################
class approved_Reject_TravelRequestByMail(ListCreateAPIView):
    serializer_class = Travel_RequestSerializers

    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()
        if request.data.get('travel_req_id'):
            print(request.data)
            # return Response(status=status.HTTP_200_OK)
            notificationid = "NOTIF" + str(uuid.uuid4().        int)[:6]
            travel_request_id = request.data['travel_req_id']
            travel_request_id = Travel_Request.objects.filter(travel_req_id=request.data.get('travel_req_id'),
                                                              organization_id=request.data.get('org_id')).first()
            employee = Travel_Request.objects.filter(travel_req_id=request.data.get('travel_req_id')).values(
                'supervisor', 'business_lead', 'project_manager', 'expense_approver', 'client_executive_lead',
                'emp_email_id', 'approval_level')

            current_ticket_owner = request.data['current_ticket_owner']
            emp_email_id = employee[0]['emp_email_id']

            request.data['current_ticket_owner'] = ""
            teemp_status = employee[0]['approval_level']
            if request.data['approve_action'] == "A":
                travel_req_status = Status_Master.objects.filter(name="Approved").values("value")
                if employee[0]['approval_level'] == "0":
                    if employee[0]['expense_approver']:
                        request.data['current_ticket_owner'] = employee[0]['expense_approver']
                        request.data['approval_level'] = "1"
                    elif employee[0]['project_manager']:
                        request.data['current_ticket_owner'] = employee[0]['project_manager']
                        request.data['approval_level'] = "2"
                    elif employee[0]['business_lead']:
                        request.data['current_ticket_owner'] = employee[0]['business_lead']
                        request.data['approval_level'] = "3"
                    elif employee[0]['client_executive_lead']:
                        request.data['current_ticket_owner'] = employee[0]['client_executive_lead']
                        request.data['approval_level'] = "4"
                    else:
                        request.data['current_ticket_owner'] = ""
                elif employee[0]['approval_level'] == "1":
                    if employee[0]['project_manager']:
                        request.data['current_ticket_owner'] = employee[0]['project_manager']
                        request.data['approval_level'] = "2"
                    elif employee[0]['business_lead']:
                        request.data['current_ticket_owner'] = employee[0]['business_lead']
                        request.data['approval_level'] = "3"
                    elif employee[0]['client_executive_lead']:
                        request.data['current_ticket_owner'] = employee[0]['client_executive_lead']
                        request.data['approval_level'] = "4"
                    else:
                        request.data['current_ticket_owner'] = ""

                elif employee[0]['approval_level'] == "2":
                    if employee[0]['business_lead']:
                        request.data['current_ticket_owner'] = employee[0]['business_lead']
                        request.data['approval_level'] = "3"
                    elif employee[0]['client_executive_lead']:
                        request.data['current_ticket_owner'] = employee[0]['client_executive_lead']
                        request.data['approval_level'] = "4"
                    else:
                        request.data['current_ticket_owner'] = ""
                elif employee[0]['approval_level'] == "3":
                    if employee[0]['client_executive_lead']:
                        request.data['current_ticket_owner'] = employee[0]['client_executive_lead']
                        request.data['approval_level'] = "4"
                    else:
                        request.data['current_ticket_owner'] = ""
                elif employee[0]['approval_level'] == "4":
                    if employee[0]['client_executive_lead']:
                        request.data['current_ticket_owner'] = ""
                        request.data['approval_level'] = "5"
                    else:
                        request.data['current_ticket_owner'] = ""
                    request.data['travel_req_status'] = "4"
                request.data['travel_req_status'] = "2"
                request.data['Entity_Type'] = "Travel"
                request.data['Entity_ID'] = request.data['travel_req_id']
                request.data['Action_taken_by'] = request.data['current_ticket_owner']
                request.data['Notification_Date'] = ""
                request.data['Message'] = request.data['travel_req_id'] + " New travel request for approval"
                request.data['Notification_ID'] = notificationid
                request.data['organization'] = request.data['org_id']
                serializernotificationss = NotificationSerializers(data=request.data)
                if serializernotificationss.is_valid():
                    serializernotificationss.save()
                    travelid = Travel_Request.objects.filter(travel_req_id=request.data['travel_req_id']).values(
                        'is_billable', 'project', 'expence_cureency', 'expence_departureDate', 'expence_estimatedCost',
                        'expence_fromCountry', 'expence_returnDate', 'expence_toCountry')

                    if travelid[0]['expence_estimatedCost']:
                        costs = travelid[0]['expence_estimatedCost'] + ' ' + travelid[0]['expence_cureency']
                    else:
                        costs = '0'
                    if travelid[0]['is_billable'] == True:
                        is_billable = 'Yes'
                    else:
                        is_billable = 'No'
                    ctxt = {
                        'first_name': self.employee_name(emp_code=employee[0]['emp_email_id']),
                        'approve_first_name': self.approver_name(emp_code=request.data['Action_taken_by']),
                        'project_id': travelid[0]['project'],
                        'billable': is_billable,
                        'from_country': travelid[0]['expence_fromCountry'],
                        'to_country': travelid[0]['expence_toCountry'],
                        'departure_date': travelid[0]['expence_departureDate'],
                        'return_date': travelid[0]['expence_returnDate'],
                        'total_cost_master_currency': costs,
                        'supervisor': self.employee_name(emp_code=employee[0]['supervisor']),
                        'expense_approver': self.employee_name(emp_code=employee[0]['expense_approver']),
                        'project_manager': self.employee_name(emp_code=employee[0]['project_manager']),
                        'business_lead': self.employee_name(emp_code=employee[0]['business_lead']),
                        'client_executive_lead': self.employee_name(emp_code=employee[0]['client_executive_lead'])
                    }

                    if request.data['current_ticket_owner'] != "":
                        template = 'email/approve_travel_request.html'
                        emailsubject = 'Travel request for ' + self.employee_name(
                            emp_code=employee[0]['emp_email_id']) + ' requires approval'
                        self.sendmails(ctxt, template, emailsubject, emailto=request.data['current_ticket_owner'],
                                       id=request.data['travel_req_id'])
                    notificationid = "NOTIF" + str(uuid.uuid4().int)[:6]
                    request.data['Entity_Type'] = "Travel"
                    request.data['Entity_ID'] = request.data['travel_req_id']
                    request.data['Action_taken_by'] = emp_email_id
                    request.data['Notification_Date'] = ""
                    request.data['Message'] = request.data['travel_req_id'] + " Travel request approved by " + \
                                              request.data['modified_by']
                    request.data['Notification_ID'] = notificationid
                    request.data['organization'] = request.data['org_id']

                    serializernotifications = NotificationSerializers(data=request.data)
                    if serializernotifications.is_valid():
                        serializernotifications.save()
                        if current_ticket_owner != "":
                            approver_name = self.employee_name(emp_code=current_ticket_owner)
                        else:
                            approver_name = "Assignment Team"
                        ctxt = {
                            'approver_name': approver_name,
                            'next_approver_name': self.employee_name(emp_code=request.data['current_ticket_owner']),
                            'preferred_first_name': self.approver_name(emp_code=request.data['Action_taken_by']),
                            'travel_request_id': request.data['travel_req_id'],

                        }
                        template = 'email/approvedtravelrequest.html'
                        emailsubject = 'Your travel request ' + request.data['travel_req_id'] + ' have been approved'
                        self.sendmails(ctxt, template, emailsubject, emailto=employee[0]['emp_email_id'],
                                       id=request.data['travel_req_id'])
            elif request.data['approve_action'] == "R":
                travel_req_status = Status_Master.objects.filter(name="Rejected").values("value")
                request.data['travel_req_status'] = travel_req_status[0]['value']
                request.data['current_ticket_owner'] = current_ticket_owner
                request.data['Entity_Type'] = "Travel"
                request.data['Entity_ID'] = request.data['travel_req_id']
                request.data['Action_taken_by'] = emp_email_id
                request.data['Notification_Date'] = ""
                request.data['Message'] = request.data['travel_req_id'] + " Travel Request Rejected"
                request.data['Notification_ID'] = notificationid
                request.data['organization'] = request.data['org_id']
                serializernotification = NotificationSerializers(data=request.data)
                if serializernotification.is_valid():
                    serializernotification.save()
                    ctxt = {
                        'approver_name': self.employee_name(emp_code=current_ticket_owner),
                        'preferred_first_name': self.approver_name(emp_code=request.data['Action_taken_by']),
                        'travel_request_id': request.data['travel_req_id'],
                        'msg': request.data['request_notes']

                    }
                    template = 'email/travelreject.html'
                    emailsubject = 'Your travel request ' + request.data['travel_req_id'] + ' has been rejected'
                    self.sendmails(ctxt, template, emailsubject, emailto=employee[0]['emp_email_id'],
                                   id=request.data['travel_req_id'])
            elif request.data['approve_action'] == "T":
                travel_req_status = Status_Master.objects.filter(name="Transferred").values("value")
                request.data['travel_req_status'] = travel_req_status[0]['value']
                if request.data['approval_level'] == "1":
                    request.data['expense_approver'] = request.data['transfer_to']
                    request.data['current_ticket_owner'] = request.data['transfer_to']
                elif request.data['approval_level'] == "2":
                    request.data['project_manager'] = request.data['transfer_to']
                    request.data['current_ticket_owner'] = request.data['transfer_to']
                elif request.data['approval_level'] == "3":
                    request.data['business_lead'] = request.data['transfer_to']
                    request.data['current_ticket_owner'] = request.data['transfer_to']
                elif request.data['approval_level'] == "4":
                    request.data['client_executive_lead'] = request.data['transfer_to']
                    request.data['current_ticket_owner'] = request.data['transfer_to']
                request.data['Entity_Type'] = "Travel"
                request.data['Entity_ID'] = request.data['travel_req_id']
                request.data['Action_taken_by'] = request.data['transfer_to']
                request.data['Notification_Date'] = ""
                request.data['Message'] = request.data['travel_req_id'] + " Travel request transferred"
                request.data['Notification_ID'] = notificationid
                request.data['organization'] = request.data['org_id']
                serializernotificationss = NotificationSerializers(data=request.data)
                if serializernotificationss.is_valid():
                    serializernotificationss.save()
                    ctxt = {
                        'approver_name': self.employee_name(emp_code=current_ticket_owner),
                        'preferred_first_name': self.approver_name(emp_code=request.data['Action_taken_by']),
                        'travel_request_id': request.data['travel_req_id'],
                        'msg': request.data['request_notes']

                    }
                    template = 'email/traveltransferforapproval.html'
                    emailsubject = 'New travel request ' + request.data[
                        'travel_req_id'] + ' has been transferred for your approval'
                    self.sendmails(ctxt, template, emailsubject, emailto=request.data['Action_taken_by'],
                                   id=request.data['travel_req_id'])
                    notificationid = "NOTIF" + str(uuid.uuid4().int)[:6]
                    request.data['Entity_Type'] = "Travel"
                    request.data['Entity_ID'] = request.data['travel_req_id']
                    request.data['Action_taken_by'] = emp_email_id
                    request.data['Notification_Date'] = ""
                    request.data['Message'] = request.data['travel_req_id'] + " Travel request transferred to " + \
                                              request.data['current_ticket_owner']
                    request.data['Notification_ID'] = notificationid
                    request.data['organization'] = request.data['org_id']
                    serializernotifications = NotificationSerializers(data=request.data)
                    if serializernotifications.is_valid():
                        serializernotifications.save()
                    ctxt = {
                        'approver_name': self.employee_name(emp_code=request.data['current_ticket_owner']),
                        'preferred_first_name': self.approver_name(emp_code=request.data['Action_taken_by']),
                        'travel_request_id': request.data['travel_req_id'],
                        'msg': request.data['request_notes']

                    }
                    template = 'email/traveltransfer.html'
                    emailsubject = 'Your travel request ' + request.data[
                        'travel_req_id'] + ' has been transferred to ' + self.employee_name(
                        emp_code=request.data['current_ticket_owner'])
                    self.sendmails(ctxt, template, emailsubject, emailto=employee[0]['emp_email_id'],
                                   id=request.data['travel_req_id'])
            if request.data['take_ownership']:
                request.data['current_ticket_owner'] = request.data['take_ownership']
                notificationid = "NOTIF" + str(uuid.uuid4().int)[:6]
                request.data['Entity_Type'] = "Travel"
                request.data['Entity_ID'] = request.data['travel_req_id']
                request.data['Action_taken_by'] = emp_email_id
                request.data['Notification_Date'] = ""
                request.data['Message'] = request.data['travel_req_id'] + " Travel request Assigned to " + request.data[
                    'current_ticket_owner']
                request.data['Notification_ID'] = notificationid
                request.data['organization'] = request.data['org_id']
                serializernotifications = NotificationSerializers(data=request.data)
                if serializernotifications.is_valid():
                    serializernotifications.save()
                    msg = "Travel request  assigned"
                    self.sendmails(msg, request.data['Message'], request.data['Action_taken_by'])
            travel_request_id_ids = Travel_Request.objects.filter(travel_req_id=request.data['travel_req_id']).first()
            serializer = Travel_RequestSerializers(travel_request_id_ids, data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data': serializer.errors}
            if request.data['approve_action'] == "A":
                travel_req_status = Status_Master.objects.filter(name="Approved").values("value")
                request.data['action'] = "4"
            else:
                request.data['action'] = request.data['travel_req_status']
            request.data['action_notes'] = request.data['request_notes']
            request.data['email'] = current_ticket_owner
            request.data['module'] = request.data['module']
            request.data['travel_req_id_id'] = request.data['travel_req_id']
            request.data['organization'] = request.data['org_id']
            request.data['approval_level'] = teemp_status
            serializeraction = Travel_Request_Action_HistorySerializers(data=request.data)
            if serializeraction.is_valid():
                serializeraction.save()
            else:
                dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False,
                        'data': serializeraction.errors}

        visa_request_id = Visa_Request.objects.filter(travel_req_id=request.data['travel_req_id']).values("visa_req_id")
        if visa_request_id:
            for data in visa_request_id:
                employee = Visa_Request.objects.filter(visa_req_id=data['visa_req_id']).values('supervisor',
                                                                                               'business_lead',
                                                                                               'project_manager',
                                                                                               'expense_approver',
                                                                                               'client_executive_lead',
                                                                                               'current_ticket_owner',
                                                                                               'emp_email_id',
                                                                                               'approval_level',
                                                                                               'country',
                                                                                               'travel_start_date',
                                                                                               'travel_end_date',
                                                                                               'applied_visa',
                                                                                               'is_billable',
                                                                                               'project_id')

                supervisor = employee[0]['supervisor']
                business_lead = employee[0]['business_lead']
                project_manager = employee[0]['project_manager']
                expense_approver = employee[0]['expense_approver']
                client_executive_lead = employee[0]['client_executive_lead']
                current_ticket_owner = employee[0]['current_ticket_owner']
                data['current_ticket_owner'] = request.data['current_ticket_owner']
                data['request_notes'] = request.data['request_notes']
                data['approve_action'] = request.data['approve_action']
                data['take_ownership'] = request.data['take_ownership']
                data['transfer_to'] = request.data['transfer_to']
                data['organization'] = request.data['org_id']
                data['modified_by'] = request.data['modified_by']
                teemp_status = employee[0]['approval_level']
                emp_email_id = employee[0]['emp_email_id']
                data['module'] = "Visa"
                if data['approve_action'] == "A":
                    if employee[0]['approval_level'] == "0":
                        if employee[0]['expense_approver']:
                            data['current_ticket_owner'] = employee[0]['expense_approver']
                            data['approval_level'] = "1"
                        elif employee[0]['project_manager']:
                            data['current_ticket_owner'] = employee[0]['project_manager']
                            data['approval_level'] = "2"
                        elif employee[0]['business_lead']:
                            data['current_ticket_owner'] = employee[0]['business_lead']
                            data['approval_level'] = "3"
                        elif employee[0]['client_executive_lead']:
                            data['current_ticket_owner'] = employee[0]['client_executive_lead']
                            data['approval_level'] = "4"
                        else:
                            data['current_ticket_owner'] = ""
                    elif employee[0]['approval_level'] == "1":
                        if employee[0]['project_manager']:
                            data['current_ticket_owner'] = employee[0]['project_manager']
                            data['approval_level'] = "2"
                        elif employee[0]['business_lead']:
                            data['current_ticket_owner'] = employee[0]['business_lead']
                            data['approval_level'] = "3"
                        elif employee[0]['client_executive_lead']:
                            data['current_ticket_owner'] = employee[0]['client_executive_lead']
                            data['approval_level'] = "4"
                        else:
                            data['current_ticket_owner'] = ""

                    elif employee[0]['approval_level'] == "2":
                        if employee[0]['business_lead']:
                            data['current_ticket_owner'] = employee[0]['business_lead']
                            data['approval_level'] = "3"
                        elif employee[0]['client_executive_lead']:
                            data['current_ticket_owner'] = employee[0]['client_executive_lead']
                            data['approval_level'] = "4"
                        else:
                            data['current_ticket_owner'] = ""
                    elif employee[0]['approval_level'] == "3":
                        if employee[0]['client_executive_lead']:
                            data['current_ticket_owner'] = employee[0]['client_executive_lead']
                            data['approval_level'] = "4"
                        else:
                            data['current_ticket_owner'] = ""
                    elif employee[0]['approval_level'] == "4":
                        if employee[0]['client_executive_lead']:
                            data['current_ticket_owner'] = ""
                            data['approval_level'] = "5"
                        else:
                            data['current_ticket_owner'] = ""
                        data['visa_status'] = "4"
                    data['visa_status'] = "2"
                    data['Entity_Type'] = "Visa"
                    notificationid = "NOTIF" + str(uuid.uuid4().int)[:6]
                    data['Entity_ID'] = data['visa_req_id']
                    data['Action_taken_by'] = data['current_ticket_owner']
                    data['Notification_Date'] = ""
                    data['Message'] = data['visa_req_id'] + " New Visa request for approval"
                    data['Notification_ID'] = notificationid
                    data['organization'] = data['organization']
                    serializernotificationss = NotificationSerializers(data=data)
                    if serializernotificationss.is_valid():
                        serializernotificationss.save()
                        country = Country_Master.objects.filter(country_id=employee[0]['country']).values("name")
                        if employee[0]['is_billable'] == True:
                            is_billable = 'Yes'
                        else:
                            is_billable = 'No'
                        ctxt = {
                            'first_name': self.employee_name(emp_code=employee[0]['emp_email_id']),
                            'approve_first_name': self.approver_name(emp_code=data['current_ticket_owner']),
                            'project_id': employee[0]['project_id'],
                            'billable': is_billable,
                            'to_country': country[0]['name'],
                            'from_date': self.date_format(date=employee[0]['travel_start_date']),
                            'return_date': self.date_format(date=employee[0]['travel_end_date']),
                            'visa_type': employee[0]['applied_visa'],
                            'supervisor': self.employee_name(emp_code=employee[0]['supervisor']),
                            'expense_approver': self.employee_name(emp_code=employee[0]['expense_approver']),
                            'project_manager': self.employee_name(emp_code=employee[0]['project_manager']),
                            'business_lead': self.employee_name(emp_code=employee[0]['business_lead']),
                            'client_executive_lead': self.employee_name(emp_code=employee[0]['client_executive_lead'])
                        }
                        if data['current_ticket_owner'] != "":
                            template = 'email/approve_visa_request.html'
                            emailsubject = 'Visa request for ' + self.employee_name(
                                emp_code=employee[0]['emp_email_id']) + ' requires approval'
                            self.sendmails(ctxt, template, emailsubject, emailto=data['current_ticket_owner'],
                                           id=data['visa_req_id'])
                        notificationid = "NOTIF" + str(uuid.uuid4().int)[:6]
                        data['Entity_Type'] = "Visa"
                        data['Entity_ID'] = data['visa_req_id']
                        data['Action_taken_by'] = emp_email_id
                        data['Notification_Date'] = ""
                        data['Message'] = data['visa_req_id'] + " Visa request approved by " + data['modified_by']
                        data['Notification_ID'] = notificationid
                        data['organization'] = data['organization']

                        serializernotifications = NotificationSerializers(data=data)
                        if serializernotifications.is_valid():
                            serializernotifications.save()
                            if current_ticket_owner != "":
                                approver_name = self.employee_name(emp_code=current_ticket_owner)
                            else:
                                approver_name = "Assignment Team"
                            ctxt = {
                                'approver_name': approver_name,
                                'next_approver_name': self.employee_name(emp_code=data['current_ticket_owner']),
                                'preferred_first_name': self.approver_name(emp_code=data['Action_taken_by']),
                                'visa_request_id': data['visa_req_id'],
                            }
                            template = 'email/approvedvisarequest.html'
                            emailsubject = 'Your visa request ' + data['visa_req_id'] + ' have been approved'
                            self.sendmails(ctxt, template, emailsubject, emailto=employee[0]['emp_email_id'],
                                           id=data['visa_req_id'])
                elif data['approve_action'] == "R":
                    visa_status = Status_Master.objects.filter(name="Rejected").values("value")
                    data['approval_level'] = request.data['approval_level']
                    data['visa_status'] = visa_status[0]['value']
                    data['current_ticket_owner'] = request.data['current_ticket_owner']
                    notificationid = "NOTIF" + str(uuid.uuid4().int)[:6]
                    data['Entity_Type'] = "Visa"
                    data['Entity_ID'] = data['visa_req_id']
                    data['Action_taken_by'] = emp_email_id
                    data['Notification_Date'] = ""
                    data['Message'] = data['visa_req_id'] + " Visa Request Rejected"
                    data['Notification_ID'] = notificationid
                    data['organization'] = data['organization']
                    serializernotification = NotificationSerializers(data=data)
                    if serializernotification.is_valid():
                        serializernotification.save()
                        ctxt = {
                            'approver_name': self.employee_name(emp_code=current_ticket_owner),
                            'preferred_first_name': self.approver_name(emp_code=data['Action_taken_by']),
                            'visa_request_id': data['visa_req_id'],
                            'msg': request.data['request_notes']

                        }
                        template = 'email/visareject.html'
                        emailsubject = 'Your visa request ' + data['visa_req_id'] + ' has been rejected'
                        self.sendmails(ctxt, template, emailsubject, emailto=employee[0]['emp_email_id'],
                                       id=data['visa_req_id'])
                elif data['approve_action'] == "T":
                    visa_status = Status_Master.objects.filter(name="Transferred").values("value")
                    data['approval_level'] = request.data['approval_level']
                    data['visa_status'] = visa_status[0]['value']
                    if data['approval_level'] == "1":
                        data['expense_approver'] = data['transfer_to']
                        data['current_ticket_owner'] = data['transfer_to']
                    elif data['approval_level'] == "2":
                        data['project_manager'] = data['transfer_to']
                        data['current_ticket_owner'] = data['transfer_to']
                    elif data['approval_level'] == "3":
                        data['business_lead'] = data['transfer_to']
                        data['current_ticket_owner'] = data['transfer_to']
                    elif data['approval_level'] == "4":
                        data['client_executive_lead'] = data['transfer_to']
                        data['current_ticket_owner'] = data['transfer_to']
                    notificationid = "NOTIF" + str(uuid.uuid4().int)[:6]
                    data['Entity_Type'] = "Visa"
                    data['Entity_ID'] = data['visa_req_id']
                    data['Action_taken_by'] = data['transfer_to']
                    data['Notification_Date'] = ""
                    data['Message'] = data['visa_req_id'] + " Visa request transferred"
                    data['Notification_ID'] = notificationid
                    data['organization'] = data['organization']
                    serializernotificationss = NotificationSerializers(data=data)
                    if serializernotificationss.is_valid():
                        serializernotificationss.save()
                        ctxt = {
                            'approver_name': self.employee_name(emp_code=current_ticket_owner),
                            'preferred_first_name': self.approver_name(emp_code=data['Action_taken_by']),
                            'visa_request_id': data['visa_req_id'],
                            'msg': request.data['request_notes']

                        }
                        template = 'email/visatransferforapproval.html'
                        emailsubject = 'New visa request ' + data[
                            'visa_req_id'] + ' has been transferred for your approval'
                        self.sendmails(ctxt, template, emailsubject, emailto=data['Action_taken_by'],
                                       id=data['visa_req_id'])
                        notificationid = "NOTIF" + str(uuid.uuid4().int)[:6]
                        data['Entity_Type'] = "Visa"
                        data['Entity_ID'] = data['visa_req_id']
                        data['Action_taken_by'] = emp_email_id
                        data['Notification_Date'] = ""
                        data['Message'] = data['visa_req_id'] + " Visa request  transferred to " + data[
                            'current_ticket_owner']
                        data['Notification_ID'] = notificationid
                        data['organization'] = data['organization']
                        serializernotifications = NotificationSerializers(data=data)
                        if serializernotifications.is_valid():
                            serializernotifications.save()
                        ctxt = {
                            'approver_name': self.employee_name(emp_code=data['current_ticket_owner']),
                            'preferred_first_name': self.approver_name(emp_code=data['Action_taken_by']),
                            'visa_request_id': data['visa_req_id'],
                            'msg': request.data['request_notes']

                        }
                        template = 'email/visatransfer.html'
                        emailsubject = 'Your visa request ' + data[
                            'visa_req_id'] + ' has been transferred to ' + self.employee_name(
                            emp_code=data['current_ticket_owner'])
                        self.sendmails(ctxt, template, emailsubject, emailto=emp_email_id, id=data['visa_req_id'])
                if data['take_ownership']:

                    if data['approve_action'] == "":
                        data['current_ticket_owner'] = data['take_ownership']
                        notificationid = "NOTIF" + str(uuid.uuid4().int)[:6]
                        data['Entity_Type'] = "Visa"
                        data['Entity_ID'] = data['visa_req_id']
                        data['Action_taken_by'] = emp_email_id
                        data['Notification_Date'] = ""
                        data['Message'] = data['visa_req_id'] + " Visa request assigned to " + data[
                            'current_ticket_owner']
                        data['Notification_ID'] = notificationid
                        data['organization'] = data['organization']
                        serializernotifications = NotificationSerializers(data=data)
                        if serializernotifications.is_valid():
                            serializernotifications.save()
                            msg = "Visa request assigned"
                            self.sendmails(msg, data['Message'], data['Action_taken_by'])
                if data['approve_action'] == "U":
                    data['current_ticket_owner'] = data['take_ownership']

                visa_request_ids = Visa_Request.objects.filter(visa_req_id=data['visa_req_id']).first()
                serializer = Visa_RequestSerializers(visa_request_ids, data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    # print(serializer.errors)
                    dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False,
                            'data': serializer.errors}
                if request.data['approve_action'] == "A":
                    visa_status = Status_Master.objects.filter(name="Approved").values("value")
                    data['action'] = "4"
                else:
                    data['action'] = visa_status[0]['value']
                data['action_notes'] = request.data['request_notes']
                data['email'] = current_ticket_owner
                data['visa_req_id'] = data['visa_req_id']
                data['organization'] = data['organization']
                data['approval_level'] = request.data['approval_level']
                data['email_id'] = request.data['modified_by']
                print(data['email_id'])
                actionserializer = Visa_Request_Action_HistorySerializers(data=data)
                if actionserializer.is_valid():
                    actionserializer.save()
                    dict = {'massage code': '200', 'massage': 'successful', 'status': True}
                else:
                    dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False,
                            'data': actionserializer.errors}
        else:
            dict = {'massage code': '200', 'massage': 'successful', 'status': True}
        return Response(dict, status=status.HTTP_200_OK)

    def sendmails(self, ctxt, template, emailsubject, emailto, id):
        # Action_taken_by=Action_taken_by
        # "rahulr@triazinesoft.com"
        ctxt = ctxt
        template = template
        travel_req_id = id
        emailsubject = emailsubject
        emp_code = Employee.objects.filter(emp_code=emailto).values('email', 'preferred_first_name', 'first_name',
                                                                    'last_name')
        print(emp_code)
        if emp_code[0]['email']:
            toemail = emp_code[0]['email']
        else:
            toemail = ""
        subject, from_email, to = emailsubject, '', toemail
        print(toemail)
        html_content = render_to_string(template, ctxt)
        print(html_content)
        # render with dynamic value
        text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

        # create the email, and attach the HTML version as well.

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def approver_name(self, emp_code):
        if emp_code:
            emp_code = Employee.objects.filter(emp_code=emp_code).values('emp_code', 'preferred_first_name',
                                                                         'first_name', 'last_name')
            if emp_code[0]['preferred_first_name']:
                first_name = emp_code[0]['preferred_first_name']
            else:
                first_name = emp_code[0]['first_name']

            # if emp_code[0]['last_name']:
            #     last_name=emp_code[0]['last_name']
            # else:
            #     last_name=""
            name = first_name
            return name
        else:
            name = ''
            return name

    def employee_name(self, emp_code):
        if emp_code:
            emp_code = Employee.objects.filter(emp_code=emp_code).values('emp_code', 'preferred_first_name',
                                                                         'first_name', 'last_name')
            if emp_code[0]['first_name']:
                first_name = emp_code[0]['first_name']
            else:
                first_name = ''

            if emp_code[0]['last_name']:
                last_name = emp_code[0]['last_name']
            else:
                last_name = ""
            name = first_name + " " + last_name
            return name
        else:
            name = ''
            return name

    def date_format(self, date):
        print(date)
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        date = str(date)[0:19]
        # utc = datetime.utcnow()
        utc = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        # Tell the datetime object that it's in UTC time zone since
        # datetime objects are 'naive' by default
        utc = utc.replace(tzinfo=from_zone)
        # Convert time zone
        central = utc.astimezone(to_zone)
        string = str(central)
        demo = string[0:10].split("-")
        new_case_date = demo[2] + "/" + demo[1] + "/" + demo[0]
        return new_case_date

#########################################
#  get travel count for employee
#########################################


class getTravelCountUser(APIView):
    serializer_class = Travel_RequestSerializers
    permission_classes = (IsAuthenticated,)

    def get(self, request, emp_code=None):
        emp_code = request.GET.get('emp_code', '')
        if (emp_code is None) or (emp_code == ''):
            dict = {'massage': 'Please send me employee code', 'status': False, 'data': []}

        else:
            inprogress = Travel_Request.objects.filter(created_by=emp_code,travel_req_status=2).count()
            close = Travel_Request.objects.filter(created_by=emp_code, travel_req_status=3).count()
            saved = Travel_Request_Draft.objects.filter(emp_email=emp_code).count()
            data = {
                'inprogress':inprogress,
                    'close':close,
                    'saved':saved,
            }
            # data = Travel_Request.objects.values('travel_req_status').filter(created_by=emp_code).annotate(total=Count('travel_req_status'))
            dict = {'massage': 'data found', 'status': True, 'data': data}
        return Response(dict, status=status.HTTP_200_OK)


#######################################################
# get travel request approver top
#######################################################

class get_travel_request_approver_top(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Travel_RequestSerializers

    def get(self, request):
        alldata = []
        limit = int(request.GET['limit'])
        if request.GET['type'] == "Travel":
            travel_request = Travel_Request.objects.filter(
                Q(expense_approver=request.GET['emp_email']) | Q(project_manager=request.GET['emp_email']) | Q(
                    business_lead=request.GET['emp_email']) | Q(client_executive_lead=request.GET['emp_email']) | Q(
                    supervisor=request.GET['emp_email']),
                Q(travel_req_status=request.GET['travel_req_status']) | Q(travel_req_status="6"),
                current_ticket_owner=request.GET['emp_email'], organization_id=request.GET['org_id']).values(
                "travel_req_id").order_by('-date_modified')[:limit]
            for data in travel_request:
                print(data)
                travel_request = Travel_Request.objects.filter(travel_req_id=data['travel_req_id'])
                travel_requests = Travel_RequestSerializers(travel_request, many=True)
                emp_code = Employee.objects.filter(emp_code=travel_requests.data[0]['emp_email']).values('emp_code',
                                                                                                         'first_name',
                                                                                                         'last_name',
                                                                                                         'email')
                if emp_code[0]['emp_code']:
                    travel_requests.data[0]['emp_code'] = emp_code[0]['emp_code']
                else:
                    travel_requests.data[0]['emp_code'] = ""
                # emp_codes = Employee.objects.filter(emp_code=travel_requests.data[0]['current_ticket_owner']).values(
                #     'email')
                # if emp_codes[0]['email']:
                #     travel_requests.data[0]['current_ticket_owner'] = emp_codes[0]['email']
                # else:
                #     travel_requests.data[0]['current_ticket_owner'] = ""
                if emp_code[0]['first_name']:
                    travel_requests.data[0]['first_name'] = emp_code[0]['first_name']
                else:
                    travel_requests.data[0]['first_name'] = ""

                if emp_code[0]['last_name']:
                    travel_requests.data[0]['last_name'] = emp_code[0]['last_name']
                else:
                    travel_requests.data[0]['last_name'] = ""
                travel_request_detail = Travel_Request_Details.objects.filter(
                    travel_req_id=travel_requests.data[0]['travel_req_id']).values('id', 'travel_req_id_id',
                                                                                   'travelling_country',
                                                                                   'travelling_country_to',
                                                                                   # 'office_location', 'client_number',
                                                                                   # 'organization', 'source_city',
                                                                                   # 'destination_city',
                                                                                   'departure_date',
                                                                                   'return_date',
                                                                                   # 'is_accmodation_required',
                                                                                   # 'accmodation_start_date',
                                                                                   # 'accmodation_end_date',
                                                                                   # 'travel_purpose', 'assignment_type',
                                                                                   # 'applicable_visa', 'visa_number',
                                                                                   # 'visa_expiry_date', 'host_hr_name',
                                                                                   # 'host_country_head', 'host_attorney',
                                                                                   # 'host_phone_no',
                                                                                   # 'is_client_location', 'client_name',
                                                                                   # 'client_address', 'hotel_cost',
                                                                                   # 'per_diem_cost', 'airfare_cost',
                                                                                   # 'transportation_cost', 'total_cost',
                                                                                   'travel_request_status',
                                                                                   # 'travel_request_status_notes',
                                                                                   # 'is_dependent',
                                                                                   )
                # travel_request_detail=Travel_RequestSerializers(travel_request_detail,many=True).values('id','travel_req_id_id','travelling_country', 'travelling_country_to','office_location','client_number','organization','source_city','destination_city','departure_date','return_date','is_accmodation_required','accmodation_start_date','accmodation_end_date','travel_purpose','assignment_type','applicable_visa','visa_number','visa_expiry_date','host_hr_name','host_country_head','host_attorney','host_phone_no','is_client_location','client_name','client_address','hotel_cost','per_diem_cost','airfare_cost','transportation_cost','total_cost','travel_request_status','travel_request_status_notes','is_dependent',)
                travel_requests.data[0]['details'] = travel_request_detail
                travel_request_dependent = Travel_Request_Dependent.objects.filter(
                    travel_req_id=travel_requests.data[0]['travel_req_id'])
                travel_request_dependent = Travel_Request_DependentSerializers(travel_request_dependent, many=True)
                travel_requests.data[0]['dependent'] = travel_request_dependent.data
                alldata.append(travel_requests.data[0])
            dict = {'massage': 'data found', 'status': True, 'data': alldata}
        elif request.GET['type'] == "Visa":
            visa_request = Visa_Request.objects.filter(
                Q(expense_approver=request.GET['emp_email']) | Q(project_manager=request.GET['emp_email']) | Q(
                    business_lead=request.GET['emp_email']) | Q(client_executive_lead=request.GET['emp_email']) | Q(
                    client_executive_lead=request.GET['emp_email']) | Q(supervisor=request.GET['emp_email']),
                Q(visa_status=request.GET['visa_status']) | Q(visa_status="6"),
                current_ticket_owner=request.GET['emp_email'], organization_id=request.GET['org_id']).values(
                "visa_req_id").order_by('-date_modified')[:limit]
            for data in visa_request:
                visa_request = Visa_Request.objects.filter(visa_req_id=data['visa_req_id'])
                visa_request = Visa_RequestSerializers(visa_request, many=True)
                emp_code = Employee.objects.filter(emp_code=visa_request.data[0]['emp_email']).values('emp_code',
                                                                                                      'first_name',
                                                                                                      'last_name')
                if emp_code[0]['emp_code']:
                    visa_request.data[0]['emp_code'] = emp_code[0]['emp_code']
                else:
                    visa_request.data[0]['emp_code'] = ""
                emp_codes = Employee.objects.filter(emp_code=visa_request.data[0]['current_ticket_owner']).values(
                    'email')
                if emp_codes[0]['email']:
                    visa_request.data[0]['current_ticket_owner'] = emp_codes[0]['email']
                else:
                    visa_request.data[0]['current_ticket_owner'] = ""
                if emp_code[0]['first_name']:
                    visa_request.data[0]['first_name'] = emp_code[0]['first_name']
                else:
                    visa_request.data[0]['first_name'] = ""

                if emp_code[0]['last_name']:
                    visa_request.data[0]['last_name'] = emp_code[0]['last_name']
                else:
                    visa_request.data[0]['last_name'] = ""
                alldata.append(visa_request.data[0])
            dict = {'massage': 'data found', 'status': True, 'data': alldata}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)




##################################################
# Travel request priority update
##################################################


class travel_request_priority(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Travel_RequestSerializers

    def get_object(self, travel_req_id):
        return Travel_Request.objects.filter(travel_req_id=travel_req_id).first()

    def patch(self, request):
        travel_req_id = request.GET.get('travel_req_id','')
        instance = self.get_object(travel_req_id)
        serializer = Travel_RequestSerializers(instance, data=request.data,partial=True)  # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            dict = {'massage': 'Updated', 'status': True, 'data': serializer.data}
        else:
            dict = {'massage': 'Failed to update', 'status': False}
        return Response(dict, status=status.HTTP_200_OK)


