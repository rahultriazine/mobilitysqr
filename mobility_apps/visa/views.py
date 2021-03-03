from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.employee.models import Employee
from mobility_apps.employee.serializer import EmployeeSerializers
from mobility_apps.master.models import Approval_Hierarchy ,Request_Approvals,Status_Master
from mobility_apps.visa.models import Visa_Request , Visa_Request_Document
from mobility_apps.travel.models import Visa_Request_Action_History
from mobility_apps.visa.serializers import Visa_RequestSerializers , Visa_Request_DocumentSerializers
from mobility_apps.travel.serializers import Travel_RequestSerializers ,Travel_Request_DetailsSerializers,Travel_Request_DependentSerializers,Travel_Request_DraftSerializers ,Travel_Request_Details_DraftSerializers,Travel_Request_Dependent_DraftSerializers,Travel_Request_Action_HistorySerializers,Visa_Request_Action_HistorySerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
from rest_framework.parsers import MultiPartParser, FormParser
#import pandas as pd
import uuid
from datetime import datetime
from mobility_apps.response_message import *
from collections import Counter
from django.db import connection
from django.db.models import Q, Count
class get_delete_update_visa_request(RetrieveDestroyAPIView):
    http_method_names = ['get', 'put', 'delete', 'head', 'options', 'trace']
    #permission_classes = (IsAuthenticated,)
    serializer_class = Visa_RequestSerializers

    def get_queryset(self, pk):
        try:
            Visa_Request = Visa_Request.objects.get(pk=self.kwargs['pk'])
        except Visa_Request.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return Visa_Request

    # Get a Visa
    def get(self, request, pk):
        Visa_Request = self.get_queryset(pk)
        serializer = Visa_RequestSerializers(Visa_Request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Delete a Visa
    def delete(self, request, pk):
        Visa_Request = self.get_queryset(pk)

        if (True):  # If creator is who makes request
            try:
                Visa_Request.delete()
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


class get_post_visa_request(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Visa_RequestSerializers

    def get_queryset(self,emp_email,visa_status,org_id):
        try:
            visa_request= Visa_Request.objects.filter(emp_email=emp_email,visa_status=visa_status,organization_id=org_id).order_by('-date_modified')
        # print(visa)
        except Visa_Request.DoesNotExist:

            return []
        return visa_request
    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        visa_request = self.get_queryset(request.GET["emp_email"],request.GET["visa_status"],request.GET["org_id"])
        print(visa_request)
        alldata=[]
        for data in visa_request:
            dic={}
            id=data.visa_req_id
            print(id)

            visa_request=Visa_Request.objects.filter(visa_req_id=id).first()
            visa_request = Visa_RequestSerializers(visa_request)
            print(visa_request.data['emp_email'])
            emp_code=Employee.objects.filter(emp_code=visa_request.data['emp_email']).values('emp_code','first_name','last_name')
            print(emp_code[0]['emp_code'])
            if emp_code[0]['emp_code']:
                dic['emp_code']=emp_code[0]['emp_code']
            else:
                dic['emp_code']=""
            if emp_code[0]['first_name']:
                dic['first_name']=emp_code[0]['first_name']
            else:
                dic['first_name']=""

            if emp_code[0]['last_name']:
                dic['last_name']=emp_code[0]['last_name']
            else:
                dic['last_name']=""
            dic.update(visa_request.data)
            visa_request_document=Visa_Request_Document.objects.filter(visa_request=id).first()
            if visa_request_document:
                visa_request_document_serializer = Visa_Request_DocumentSerializers(visa_request_document)
                dic.update(visa_request_document_serializer.data)
            alldata.append(dic)

        dict = {'massage': 'data found', 'status': True, 'data':alldata}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)

    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace(
        alldata=[]
        for data in request.data:
            print(data)
            if data['visa_req_id']:
                epoch=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                dt=str(epoch).replace(' ','')
                visa_request_id=Visa_Request.objects.filter(visa_req_id=data['visa_req_id']).first()
                employee=Visa_Request.objects.filter(visa_req_id=data['visa_req_id']).values('business_lead','project_manager','expense_approver','client_executive_lead')

                business_lead=employee[0]['business_lead']
                project_manager=employee[0]['project_manager']
                expense_approver=employee[0]['expense_approver']
                client_executive_lead=employee[0]['client_executive_lead']
                current_ticket_owner= data['current_ticket_owner']
                if data['approve_action']=="A":
                    visa_status=Status_Master.objects.filter(name="Approved").values("value")
                    data['visa_status']=visa_status[0]['value']
                elif data['approve_action']=="R":
                    visa_status=Status_Master.objects.filter(name="Rejected").values("value")
                    data['visa_status']=visa_status[0]['value']
                    data['current_ticket_owner']=current_ticket_owner
                elif data['approve_action']=="T":
                    visa_status=Status_Master.objects.filter(name="Transferred").values("value")
                    data['visa_status']=visa_status[0]['value']
                    print(expense_approver)
                if data['current_ticket_owner']==expense_approver:
                    data['expense_approver'] = request.data['transfer_to']
                    data['current_ticket_owner']=request.data['transfer_to']
                elif data['current_ticket_owner'] ==project_manager:
                    data['project_manager'] =request.data['transfer_to']
                    data['current_ticket_owner']=request.data['transfer_to']
                elif data['current_ticket_owner'] ==business_lead:
                    data['business_lead'] =request.data['transfer_to']
                    data['current_ticket_owner']=request.data['transfer_to']
                elif data['current_ticket_owner']==client_executive_lead:
                    data['client_executive_lead'] =request.data['transfer_to']
                    data['current_ticket_owner']=request.data['transfer_to']
                data['action']=data['visa_status']
                data['action_notes']=data['request_notes']
                data['email']=data['current_ticket_owner']
                data['visa_req_id_id']=data['visa_req_id']
                print(data['email'])
                actionserializer =Visa_Request_Action_HistorySerializers(data=data)

                if actionserializer.is_valid():
                    actionserializer.save()

                data['current_ticket_owner']=""
                if  current_ticket_owner==expense_approver:
                    data['current_ticket_owner'] = employee[0]['project_manager']
                elif current_ticket_owner ==project_manager:
                    data['current_ticket_owner'] =employee[0]['business_lead']
                elif current_ticket_owner ==business_lead:
                    data['current_ticket_owner'] =employee[0]['client_executive_lead']
                elif current_ticket_owner==client_executive_lead:
                    data['current_ticket_owner'] =""

                serializer = Visa_RequestSerializers(visa_request_id,data=data)
                if serializer.is_valid():
                    visa_req_id=serializer.save().visa_req_id
                    alldata.append(visa_req_id)
                    dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data': alldata}
                else:
                    dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False, 'data': serializer.errors}
            else:
                dict = {'massage code': '200', 'massage': 'unsuccessful', 'status': False}
        return Response(dict, status=status.HTTP_200_OK)
        # return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class get_post_visa_document(ListCreateAPIView):
    serializer_class = Visa_Request_DocumentSerializers
    parser_classes = (MultiPartParser, FormParser)
    # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace
        
        vid=request.data['id']
        uploaded_document_name=request.data['uploaded_document_name']
        visa_request=request.data['visa_request']
        document_name=request.data['document_name']
        request_status=request.data['request_status']
        visa_main_id=request.data['visa_main_id']
        if vid:
            vid=vid
        else:
            vidvisa=Visa_Request_Document.objects.filter(visa_request=visa_request,visa_main_id=visa_main_id).values("id")    
            if vidvisa:
                vid =vidvisa[0]["id"]
            else:
                vid=""
        #visa_request=request.data['visa_request']
        
        try:
        
            if vid:
                #cursor = connection.cursor()
                #cursors=cursor.execute("UPDATE visa_visa_request_document SET uploaded_document_name='"+object(uploaded_document_name)+"',visa_request_id='"+str(visa_request)+"',document_name='"+str(document_name)+"',request_status='"+str(request_status)+"' WHERE id='"+str(id)+"'")

                visa = Visa_Request_Document.objects.filter(id=vid).first()
                visa_request_documentss = Visa_Request_DocumentSerializers(visa,data=request.data)
                if visa_request_documentss.is_valid():
                    visa_request_documentss.save()
                    dict = {'massage code': '200', 'massage': 'updated successfully', 'status': True, 'data':request.data.get('visa_request')}
                else:
                   
                    dict = {'massage code': '201', 'massage': 'unsuccessfull', 'status': False, 'data':visa_request_documentss.errors}
                return Response(dict, status=status.HTTP_201_CREATED)
            else:
                
                visa_request_document = Visa_Request_DocumentSerializers(data=request.data)

                if visa_request_document.is_valid():
                    id=visa_request_document.save().id
                    dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data': id}
                else:
                    dict = {'massage code': '201', 'massage': 'unsuccessful', 'status': False, 'data': visa_request_document.errors}
                return Response(dict, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'massage code': 'already exists', 'massage': 'unsuccessful', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)

class get_count_visa_request(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Visa_RequestSerializers

    def get_queryset(self,status,org_id):
        try:
            visa= Visa_Request.objects.filter(visa_status=status,current_ticket_owner="",organization_id=org_id)
        except visa.DoesNotExist:
            return []
        return visa

    # Get all visa_purpose
    def get(self, request):
        visa = self.get_queryset(request.GET['status'],request.GET['org_id'])
        print(visa)
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer =Visa_RequestSerializers(visa,many=True)
        dict = {"status": True, "message":MSG_SUCESS, "data": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)


class get_org_visa_request(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Visa_RequestSerializers

    def get_queryset(self,visa_status,current_ticket_email,org_id):
        try:
            if current_ticket_email:
                visa= Visa_Request.objects.filter(current_ticket_owner=current_ticket_email,visa_status=visa_status,organization_id=org_id).order_by('-date_modified')
            else:
                visa= Visa_Request.objects.filter(current_ticket_owner="",visa_status=visa_status,organization_id=org_id).order_by('-date_modified')

        except Visa_Request.DoesNotExist:
            return []
        return visa

    # Get all visa_purpose
    def get(self, request):
        if request.GET['visa_status']=="all":
            visa=Visa_Request.objects.all()
        else:
            visa = self.get_queryset(request.GET['visa_status'],request.GET['current_ticket_email'],request.GET['org_id'])
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        if visa:
            serializer =Visa_RequestSerializers(visa,many=True)
            print(serializer.data)
            i=0
            for data in serializer.data:
                print(data['emp_email'])
                emp_code=Employee.objects.filter(emp_code=data['emp_email']).values('emp_code','first_name','last_name')
                if emp_code[0]['emp_code']:
                    serializer.data[i]['emp_code']=emp_code[0]['emp_code']
                else:
                    serializer.data[i]['emp_code']=""

                if emp_code[0]['first_name']:
                    serializer.data[i]['first_name']=emp_code[0]['first_name']

                else:
                    serializer.data[i]['first_name']=""

                if emp_code[0]['last_name']:
                    serializer.data[i]['last_name']=emp_code[0]['last_name']

                else:
                    serializer.data[i]['last_name']=""
                i=i+1
                dict = {"status": True, "message":MSG_SUCESS, "data": serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {"status": False,"status_code":200, "message":MSG_FAILED}
            return Response(dict, status=status.HTTP_200_OK)

class get_count_visa_requests(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Visa_RequestSerializers
    def get(self, request):
        visa= Visa_Request.objects.filter(Q(visa_status="2")|Q(visa_status="3")|Q(visa_status="5"),current_ticket_owner=request.GET['assignment_email'],organization_id=request.GET['org_id'])
        visas= Visa_Request.objects.filter(visa_status="2",current_ticket_owner="",organization_id=request.GET['org_id']).count()
        try:
            if visa or visas:
                serializer =Visa_RequestSerializers(visas,many=True)
                serializer =Visa_RequestSerializers(visa,many=True)
                dict=[]
                for data in serializer.data:
                    dict.append(data['visa_status'])
                total=sum(Counter(dict).values())
                my_dict = Counter(dict)
                dict = {"status": True, "message":MSG_SUCESS, "data":  my_dict,"new_request":visas}
                return Response(dict, status=status.HTTP_200_OK)
            else:
                dict = {"status":False,"status_code":200, "message":MSG_FAILED,"data":[]}
                return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            dict = {'massage code': '200', 'massage': MSG_FAILED, 'status': False}
            return Response(dict, status=status.HTTP_200_OK)



class get_view_visa_request(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Visa_RequestSerializers

    def get_queryset(self,visa_req_id,org_id):
        try:
            visa_request= Visa_Request.objects.filter(visa_req_id=visa_req_id,organization_id=org_id)
        # print(visa)
        except Visa_Request.DoesNotExist:

            return []
        return visa_request
        # Get all employee
        # import ipdb;ipdb.set_trace()
    def get(self, request):
        id=request.GET['visa_req_id']
        print(id)
        visa_request= Visa_Request.objects.filter(visa_req_id =request.GET['visa_req_id'],organization_id=request.GET['org_id'])
        visa_request_serializer = Visa_RequestSerializers(visa_request,many=True)
        visa_requetst=visa_request_serializer.data
        if visa_requetst!=[]:
            visa_request_document=Visa_Request_Document.objects.raw('SELECT * FROM visa_visa_request_document where visa_request_id =%s',[id])
            visa_request_document_serializer = Visa_Request_DocumentSerializers(visa_request_document,many=True)
            visa_requetst_doc=visa_request_document_serializer.data
            print(visa_requetst_doc.count)
            visa_requetst[0]['doc']=visa_requetst_doc
            dict = {'massage': 'data found', 'status': True, 'data':visa_requetst[0]}
            # responseList = [dict]
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'massage': MSG_FAILED, 'status': False}
            # responseList = [dict]
            return Response(dict, status=status.HTTP_200_OK)


class get_visa_request(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Visa_RequestSerializers

    def get_queryset(self,emp_email,current_ticket_owner,org_id):

        try:
            visa_request= Visa_Request.objects.filter(Q(emp_email=emp_email)|Q(expense_approver=emp_email)|Q(project_manager=emp_email)|Q(business_lead=emp_email)|Q(client_executive_lead=emp_email),current_ticket_owner=current_ticket_owner,organization_id=org_id)

        # print(visa)
        except Visa_Request.DoesNotExist:

            return []
        return visa_request
    # Get all employee
    # import ipdb;ipdb.set_trace()
    def get(self, request):
        visa_request = self.get_queryset(request.GET["emp_email"],request.GET["current_ticket_owner"],request.GET["org_id"])
        print(visa_request)
        alldata=[]
        for data in visa_request:
            dic={}
            id=data.visa_req_id
            print(id)

            visa_request=Visa_Request.objects.filter(visa_req_id=id).first()
            visa_request = Visa_RequestSerializers(visa_request)
            emp_code=Employee.objects.filter(email=visa_request.data['emp_email']).values('emp_code','first_name','last_name')
            print(emp_code[0]['emp_code'])
            if emp_code[0]['emp_code']:
                dic['emp_code']=emp_code[0]['emp_code']
            else:
                dic['emp_code']=""
            if emp_code[0]['first_name']:
                dic['first_name']=emp_code[0]['first_name']
            else:
                dic['first_name']=""

            if emp_code[0]['last_name']:
                dic['last_name']=emp_code[0]['last_name']
            else:
                dic['last_name']=""
            dic.update(visa_request.data)
            visa_request_document=Visa_Request_Document.objects.filter(visa_request=id).first()
            if visa_request_document:
                visa_request_document_serializer = Visa_Request_DocumentSerializers(visa_request_document)
                dic.update(visa_request_document_serializer.data)
            alldata.append(dic)

        dict = {'massage': 'data found', 'status': True, 'data':alldata}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)


class get_visa_action(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        visa=Visa_Request_Action_History.objects.filter(email=request.GET['email'],organization_id=request.GET['org_id'])
        visaserializers=Visa_Request_Action_HistorySerializers(visa,many=True)

        dict = {'massage': 'data found', 'status': True, 'data': visaserializers.data}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)



class get_visa_status_summary(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        travelserializerss=Visa_Request.objects.filter(visa_req_id=request.GET['visa_req_id']).values("visa_req_id","supervisor","expense_approver","project_manager","business_lead","client_executive_lead","visa_status","current_ticket_owner","date_modified")
        alldata=[]
        print(travelserializerss[0]['supervisor'])
        travelserializersssts=Visa_Request_Action_History.objects.filter(visa_req_id_id=request.GET['visa_req_id'],email_id=travelserializerss[0]['supervisor'],approval_level="0").values("id","action","action_notes","email","date_modified","approval_level")
        dicsts={}
        test="eieirei"
        if travelserializersssts.exists():
            print(travelserializersssts)
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
           
            dicsts['current_ticket_owner']=travelserializerss[0]['current_ticket_owner']
            empname=Employee.objects.filter(emp_code=travelserializerss[0]['supervisor']).values('first_name','last_name','email')
            if empname:
                dicsts['supervisor_name']=empname[0]['first_name'] + " " + empname[0]['last_name']
                dicsts['supervisor']=empname[0]['email']
            else:
                dicsts['supervisor_name']=""
            dicsts['action_date']=travelserializerss[0]['date_modified']
        alldata.append(dicsts)
        travelserializersss=Visa_Request_Action_History.objects.filter(visa_req_id_id=request.GET['visa_req_id'],email_id=travelserializerss[0]['expense_approver'],approval_level="1").values("id","action","action_notes","email","date_modified","approval_level")
        dic={}
        if travelserializersss.exists():
            dic['expense_approver_status']=travelserializersss[0]['action']
            dic['approval_level']=travelserializersss[0]['approval_level']
            
            dic['current_ticket_owner']=travelserializerss[0]['current_ticket_owner']
            empname=Employee.objects.filter(emp_code=travelserializersss[0]['email']).values('first_name','last_name','email')
            if empname:
                dic['expense_approver_name']=empname[0]['first_name'] + " " + empname[0]['last_name']
                dic['expense_approver']=empname[0]['email']
            else:
                dic['expense_approver_name']=""
                dic['expense_approver']=""
            dic['action_date']=travelserializersss[0]['date_modified']
        else:
            dic['expense_approver_status']=""
            dic['approval_level']=""
            
            dic['current_ticket_owner']=travelserializerss[0]['current_ticket_owner']
            empname=Employee.objects.filter(emp_code=travelserializerss[0]['expense_approver']).values('first_name','last_name','email')
            if empname:
                dic['expense_approver_name']=empname[0]['first_name'] + " " + empname[0]['last_name']
                dic['expense_approver']=empname[0]['email']
            else:
                dic['expense_approver_name']=""
                dic['expense_approver']=""
            dic['action_date']=travelserializerss[0]['date_modified']
        alldata.append(dic)
        travelserializerssss=Visa_Request_Action_History.objects.filter(visa_req_id_id=request.GET['visa_req_id'],email_id=travelserializerss[0]['project_manager'],approval_level="2").values("id","action","action_notes","email","date_modified","approval_level")
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
            dics['action_date']=travelserializerssss[0]['date_modified']
        else:
            dics['project_manager_status']=""
            dics['approval_level']=""
            dics['project_manager']=travelserializerss[0]['project_manager']
            dics['current_ticket_owner']=travelserializerss[0]['current_ticket_owner']
            empname=Employee.objects.filter(emp_code=travelserializerss[0]['project_manager']).values('first_name','last_name','email')
            if empname:
                dics['project_manager_name']=empname[0]['first_name'] + " " +  empname[0]['last_name']
                dics['project_manager']=empname[0]['email']
            else:
                dics['project_manager_name']=""
                dics['project_manager']=""
            dics['action_date']=travelserializerss[0]['date_modified']
        alldata.append(dics)
        travelserializersssss=Visa_Request_Action_History.objects.filter(visa_req_id_id=request.GET['visa_req_id'],email_id=travelserializerss[0]['business_lead'],approval_level="3").values("id","action","action_notes","email","date_modified","approval_level")
        dicss={}
        if travelserializersssss.exists():
            dicss['business_lead_status']=travelserializersssss[0]['action']
            dicss['approval_level']=travelserializersssss[0]['approval_level']
            dicss['business_lead']=travelserializersssss[0]['email']
            dicss['current_ticket_owner']=travelserializerss[0]['current_ticket_owner']
            empname=Employee.objects.filter(emp_code=travelserializersssss[0]['email']).values('first_name','last_name','email')
            if empname:
                dicss['business_lead_name']=empname[0]['first_name'] + " " + empname[0]['last_name']
                dicss['business_lead']=empname[0]['email']
            else:
                dicss['business_lead_name']=""
                dicss['business_lead']=""
            dicss['action_date']=travelserializersssss[0]['date_modified']
        else:
            dicss['business_lead_status']=""
            dicss['approval_level']=""
            dicss['business_lead']=travelserializerss[0]['business_lead']
            dicss['current_ticket_owner']=travelserializerss[0]['current_ticket_owner']
            empname=Employee.objects.filter(emp_code=travelserializerss[0]['business_lead']).values('first_name','last_name','email')
            if empname:
                dicss['business_lead_name']=empname[0]['first_name'] + " " + empname[0]['last_name']
                dicss['business_lead']=empname[0]['email']
            else:
                dicss['business_lead_name']=""
                dicss['business_lead']=""
            dicss['action_date']=travelserializerss[0]['date_modified']
        alldata.append(dicss)
        travelserializerssssss=Visa_Request_Action_History.objects.filter(
            visa_req_id_id=request.GET['visa_req_id'],email_id=travelserializerss[0]['client_executive_lead'],approval_level="4").values("id","action","action_notes","email","date_modified","approval_level")
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
            dicsss['action_date']=travelserializerss[0]['date_modified']
        transfer_trvel=Visa_Request_Action_History.objects.filter(visa_req_id_id=request.GET['visa_req_id'],action="6").values(
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
        dict = {'massage': 'data found', 'status': True, 'data': alldata,'transfer':transfer_trvel}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)

class get_post_visa_document_request_update(APIView):
    serializer_class = Visa_Request_DocumentSerializers
    # Create a new employee
    def post(self, request, *args, **kwargs):
        # import ipdb;ipdb.set_trace(
        visa_request = Visa_Request_Document.objects.filter(document_name=request.data.get('document_name'),visa_request=request.data.get('visa_request_id')).values("id")
        id=visa_request[0]['id']
        note=request.data.get('request_note')
        req_status=request.data.get('request_status')
        print(id)
        #visa_request_id = Visa_Request_Document.objects.filter(visa_request_id=visa_request).first()
        cursor = connection.cursor()
        cursors=cursor.execute("UPDATE visa_visa_request_document SET request_note='"+str(note)+"',request_status='"+req_status+"' WHERE id='"+str(id)+"'")
        print(cursors)
        dict = {'massage': 'Updated Sucussefull', 'status': True, 'data': request.data.get('visa_request_id')}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)
		
		
class get_org_count_visa_requests(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Visa_RequestSerializers
    # Get all visa_purpose
    def get(self, request):
        travel= Visa_Request.objects.filter(visa_status="2",organization_id=request.GET['org_id']).count()
        if travel:
            travel=travel
        else:
            travel=""

        travels= Visa_Request.objects.filter(visa_status="5",organization_id=request.GET['org_id']).count()
        if travels:
            travels=travels
        else:
            travels=""
        travelss= Visa_Request.objects.filter(visa_status="3",organization_id=request.GET['org_id']).count()
        if travelss:
            travelss=travelss
        else:
            travelss=""
        #travels= Travel_Request.objects.filter(travel_req_status="2",current_ticket_owner="").count()

        dict = {"status": True, "message":MSG_SUCESS, "Inprogress":travel,"Rejected":travels,"Closed":travelss}
        return Response(dict, status=status.HTTP_200_OK)
		
class org_visa_requests(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Visa_RequestSerializers
    def get(self, request):
        visa_request_count= Visa_Request.objects.filter(organization_id=request.GET['org_id']).count()
        if visa_request_count:
           visa_request_count=visa_request_count
        else:
           visa_request_count=""
        visa_request= Visa_Request.objects.filter(visa_status=request.GET['visa_status'],organization_id=request.GET['org_id'])
        print(visa_request)
        alldata=[]
        for data in visa_request:
            dic={}
            id=data.visa_req_id
            print(id)

            visa_request=Visa_Request.objects.filter(visa_req_id=id).first()
            visa_request = Visa_RequestSerializers(visa_request)
            emp_code=Employee.objects.filter(emp_code=visa_request.data['emp_email']).values('emp_code','first_name','last_name')
            print(emp_code[0]['emp_code'])
            if emp_code[0]['emp_code']:
                dic['emp_code']=emp_code[0]['emp_code']
            else:
                dic['emp_code']=""
            if emp_code[0]['first_name']:
                dic['first_name']=emp_code[0]['first_name']
            else:
                dic['first_name']=""

            if emp_code[0]['last_name']:
                dic['last_name']=emp_code[0]['last_name']
            else:
                dic['last_name']=""
            emp_codes=Employee.objects.filter(emp_code=visa_request.data['current_ticket_owner']).values('email','first_name','last_name')
            if emp_codes:
                visa_request.data['current_ticket_owner']=emp_codes[0]['email']
            else:
                visa_request.data['current_ticket_owner']=""
            dic.update(visa_request.data)
            visa_request_document=Visa_Request_Document.objects.filter(visa_request=id).first()
            if visa_request_document:
                visa_request_document_serializer = Visa_Request_DocumentSerializers(visa_request_document)
                dic.update(visa_request_document_serializer.data)
            alldata.append(dic)

        dict = {'massage': 'data found', 'status': True, 'data':alldata,'total':visa_request_count}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)