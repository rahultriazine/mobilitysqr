from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.master.models import Department
from mobility_apps.master.serializers.department import DepartmentSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
import pandas as pd
from mobility_apps.response_message import *

class get_delete_update_department(RetrieveDestroyAPIView):
    http_method_names = ['get', 'put', 'delete', 'head', 'options', 'trace']
    permission_classes = (IsAuthenticated,)
    serializer_class = DepartmentSerializers

    def get_queryset(self, pk):
        try:
            department = Department.objects.get(pk=self.kwargs['pk'])
        except Department.DoesNotExist:
            content = {
                'status': MSG_NF
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return department

    # Get a department
    def get(self, request, pk):
        department = self.get_queryset(pk)
        serializer = DepartmentSerializers(department)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Delete a coutry
    def delete(self, request, pk):
        department = self.get_queryset(pk)

        if (True):  # If creator is who makes request
            try:
                department.delete()
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



class get_post_department(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = DepartmentSerializers

    def get_queryset(self):
        department = Department.objects.all()
        return department

    # Get all department
    def get(self, request):
        department = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = DepartmentSerializers(department,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new department
    def post(self, request):
        departmentid = Department.objects.filter(
           department_id=request.data.get('department_id')).first()
        if (departmentid):
            serializer = DepartmentSerializers(
                departmentid, data=request.data)
        else:
            serializer = DepartmentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
            return Response(dict, status=status.HTTP_201_CREATED)
        dict={"status":False,'status_code':400,"message":MSG_FAILED,"data":serializer.errors}
        return Response(dict, status=status.HTTP_400_BAD_REQUEST)


class bulk_upload_department(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DepartmentSerializers

    # bulk upload api(import DEPARTMENT)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             department = Department.objects.filter(
    #                department_id=value['department_id']).first()
    #             value=value.to_dict()
    #             if (department):
    #                 continue
    #             else:
    #                 serializer = DepartmentSerializers(data=value)
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
                department = Department.objects.filter(
                    department_id=value['department_id']).first()
                value = value.to_dict()
                if (department):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = DepartmentSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    department = Department.objects.all()
                    serializer = DepartmentSerializers(department, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code':201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)


###########################################################
" json upload department"
###########################################################

class json_upload_department(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DepartmentSerializers

    def post(self, request, *args, **kwargs):
        try:
            serializer = DepartmentSerializers(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            dict = {'message': e, 'status': False, 'status_code': 406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)

