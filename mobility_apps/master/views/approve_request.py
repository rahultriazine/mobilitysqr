from django.shortcuts import render
#Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import settings
from mobility_apps.master.models import Approval_Hierarchy ,Request_Approvals,Status_Master
from mobility_apps.master.serializers.approve_request import Approve_RequestSerializers ,Request_ApprovalsSerializers,Status_MasterSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
import pandas as pd
import json
from mobility_apps.response_message import *

class get_post_approve_request(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Approve_RequestSerializers

    def get_queryset(self):
        employee = Approval_Hierarchy.objects.all()
        return employee

    # Get all employee_detail
    def get(self, request):
        employee = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Approve_RequestSerializers(employee,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new employee_detail
    def post(self, request):
        employedetail = Approval_Hierarchy.objects.filter(emp_code__id=request.data.get('id'), department__department_id=request.data.get("department_id")).first()
        if (employedetail):
            serializer = Approve_RequestSerializers(
                employedetail, data=request.data)
        else:
            serializer = Approve_RequestSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class get_post_approve_request(ListCreateAPIView):
    # Create a new employee_detail
    def post(self, request):
        serializer = Request_ApprovalsSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class get_action_status(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Status_MasterSerializers

    def get_queryset(self,module):
        employee = Status_Master.objects.filter(module__icontains=module).values("name","value","action")
        #print(employee)
        return employee

    # Get all employee_detail
    def get(self, request):
        employee = self.get_queryset(request.GET['module'])
        #print(employee)
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Status_MasterSerializers(employee,many=True)
        if request.GET['module']=="T":
           serializer.data[0]['module']="Travel"
        elif request.GET['module']=="V":
           serializer.data[0]['module']="Visa"
        elif request.GET['module']=="A":
           serializer.data[0]['module']="Assign"
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = Status_MasterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        