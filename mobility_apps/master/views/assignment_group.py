from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.master.models import Assignment_Group,Assignment_Status
from mobility_apps.employee.models import Employee
from mobility_apps.employee.serializer import EmployeeSerializers
from mobility_apps.visa.models import Visa_Request , Visa_Request_Document
from mobility_apps.visa.serializers import Visa_RequestSerializers , Visa_Request_DocumentSerializers
from mobility_apps.travel.models import Travel_Request ,Travel_Request_Details
from mobility_apps.travel.serializers import Travel_RequestSerializers ,Travel_Request_DetailsSerializers
from mobility_apps.master.serializers.assignment_group import Assignment_GroupSerializers,Assignment_StatusSerializers

from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
import pandas as pd
from django.db import connection
from mobility_apps.response_message import *
import pprint
class get_delete_update_assignment_group(RetrieveDestroyAPIView):
    http_method_names = ['get', 'put', 'delete', 'post' , 'head', 'options', 'trace']
    #permission_classes = (IsAuthenticated,)
    serializer_class = Assignment_GroupSerializers

    def get_queryset(self,id):
        try:
            assignment_group = Assignment_Group.objects.get(id=id)
        except Assignment_Group.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return assignment_group

    # Get a group
    def get(self, request):
        assignment_group = self.get_queryset(id=id)
        serializer = Assignment_GroupSerializers()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Delete a coutry
    def post(self, request):
        assignment_group = self.get_queryset(request.data["id"])
        if (True):  # If creator is who makes request
            try:
                assignment_group.delete()
                cursor = connection.cursor()
                sql="UPDATE employee_employee SET assignment_role='' WHERE emp_code='"+request.data['emp_code']+"'"
                cursor=cursor.execute(sql)
            except ProtectedError:
                content = {
                    'status': 'This resource is related to other active record.'
                }
                return Response(content, status=status.HTTP_423_LOCKED)
            content = {
                'status': True,
                "msg":"data deleted successfully",
                "msg_code":200
            }
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {
                'status': 'user not found'
            }
            return Response(content, status=status.usernotfound)



class get_post_assignment_group(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Assignment_GroupSerializers

    def get_queryset(self):
        assignment_group = Assignment_Group.objects.all()
        return assignment_group

    # Get all group
    def get(self, request):
        #assignment_group = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        assignment_group = Assignment_Group.objects.all()
        serializer=Assignment_GroupSerializers(assignment_group,many=True)
        i=0
        for data in serializer.data:
            print(data['emp_email'])
        #     assigndata=Assignment_Group.objects.filter(id=data)
        #     serializer = Assignment_GroupSerializers(assigndata,many=True)
            emp_code=Employee.objects.filter(emp_code=data['emp_email']).values('email','emp_code','first_name','last_name')
            if emp_code[0]['email']:
                serializer.data[i]['emp_email']=emp_code[0]['email']
            else:
                serializer.data[i]['emp_email']=""
            if emp_code[0]['emp_code']:
                serializer.data[i]['emp_code']=emp_code[0]['emp_code']
            else:
                serializer.data[i]['emp_code']=""
            i=i+1
        dict = {'message': MSG_SUCESS, 'status_code':200,'status': 'True','data':serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new group
    def post(self, request):
        pprint.pprint(request.data)
        if isinstance(request.data['emp_email'], list):
            emp_emails = request.data.pop('emp_email')

        models = []
        for emp_email in emp_emails:
            # validate each model with one seat at a time
            request.data['emp_email'] = emp_email
            employee = Employee.objects.get(emp_code=emp_email)
            request.data['emp_name'] = employee.first_name
            serializer = Assignment_GroupSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            cursor = connection.cursor()
            sql="UPDATE employee_employee SET assignment_role='6' WHERE emp_code='"+request.data['emp_email']+"'"
            cursor=cursor.execute(sql)
            models.append(serializer)
        saved_models = [model.save() for model in models]
        result_serializer = Assignment_GroupSerializers(saved_models, many=True)
        dict = {'message': MSG_SUCESS, 'status_code':200,'status': 'True','data':result_serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        serializer = Assignment_GroupSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        dict = {'message': MSG_SUCESS, 'status_code':200,'status': 'True','data':serializer.data}
        return Response(dict, status=status.HTTP_200_OK)


class bulk_upload_assignment_group(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = Assignment_GroupSerializers

    # bulk upload api(import ROLE)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             group = Group.objects.filter(
    #                group_id=value['group_id']).first()
    #             value=value.to_dict()
    #             if (group):
    #                 continue
    #             else:
    #                 serializer = GroupSerializers(data=value)
    #             if serializer.is_valid():
    #                 serializer.save()
    #         return Response("File uploaded successfuly", status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        try:
            data = pd.read_excel(request.data.get("file"))
            sucessCount = 0
            failureCount = 0
            for i, value in data.iterrows():
                group = Assignment_Group.objects.filter(
                    group=value['id']).first()
                value = value.to_dict()
                if (group):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Assignment_GroupSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    group = Assignment_Group.objects.all()
                    serializer = Assignment_GroupSerializers(Group, many=True)
                    dict = {'message': MSG_EXCELSU, 'status_code':201,'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)


class get_post_assignment_employee(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Assignment_GroupSerializers

    def get_queryset(self):
        assignment_group = Assignment_Group.objects.all()
        return assignment_group

    # Get all group
    def get(self, request):
        assignment_group = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Assignment_GroupSerializers(assignment_group,many=True)
        dict = {'message': MSG_SUCESS, 'status_code':200,'status': 'False','data':serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

class get_post_assignment_status(ListCreateAPIView):
    def get(self, request):
    #import ipdb;ipdb.set_trace()
        employee = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Assignment_StatusSerializers(employee,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.data['request_status']=="visa":
            Visa_Request.objects.filter(visa_req_id=request.data['request']).update(visa_status=request.data['status_type'])
            requests=Assignment_Status.objects.filter(request=request.data.get('request')).first()
            if (requests):
                serializer = Assignment_StatusSerializers(requests,data=request.data)
            else:
                serializer = Assignment_StatusSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_200_OK)
        else:
            Travel_Request.objects.filter(travel_req_id=request.data['request']).update(travel_req_status=request.data['status_type'])
            requests=Assignment_Status.objects.filter(request=request.data.get('request')).first()
            if (requests):
                serializer = Assignment_StatusSerializers(requests,data=request.data)
            else:
                serializer = Assignment_StatusSerializers(data=request.data)
            if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_200_OK)
