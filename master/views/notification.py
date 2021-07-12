from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.master.models import Notification
from mobility_apps.master.serializers.notification import NotificationSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
import pandas as pd
from mobility_apps.response_message import *

class get_post_notification(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializers

    def get_queryset(self,email,org_id):
        notification = Notification.objects.filter(Action_taken_by=email,organization_id=org_id).order_by('-id')
        return notification

    # Get all visa_purpose
    def get(self, request):
        notification = self.get_queryset(request.GET["email"],request.GET["org_id"])
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = NotificationSerializers(notification,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new visa_purpose
    def post(self, request):

        if request.data["id"] !="":
           notification=Notification.objects.filter(Action_taken_by=request.data["email"],id=request.data["id"]).values("id")
        else:
           notification=Notification.objects.filter(Action_taken_by=request.data["email"]).values("id")
        #print(notification)
        for data in notification:
            #print(data['id'])
            notification = Notification.objects.filter(id=data['id']).delete()
            dict={"status":True,'status_code':201,"message":MSG_SUCESS}
        return Response(dict, status=status.HTTP_201_CREATED)
        dict={"status":False,'status_code':400,"message":MSG_FAILED}
        return Response(dict, status=status.HTTP_400_BAD_REQUEST)