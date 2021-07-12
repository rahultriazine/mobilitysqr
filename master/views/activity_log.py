from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.master.models import Activity_Log
from mobility_apps.master.serializers.activity_log import Activity_LogSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
import pandas as pd
from mobility_apps.response_message import *

class get_delete_update_activity_log(RetrieveDestroyAPIView):
    http_method_names = ['get', 'put', 'delete', 'head', 'options', 'trace']
    permission_classes = (IsAuthenticated,)
    serializer_class = Activity_LogSerializers

    def get_queryset(self, pk):
        try:
            activity_log = Activity_Log.objects.get(pk=self.kwargs['pk'])
        except Activity_Log.DoesNotExist:
            content = {
                'status': MSG_NF
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return activity_log

    # Get a activity_log
    def get(self, request, pk):
        activity_log = self.get_queryset(pk)
        serializer = Activity_LogSerializers(activity_log)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Delete a coutry
    def delete(self, request, pk):
        activity_log = self.get_queryset(pk)

        if (True):  # If creator is who makes request
            try:
                activity_log.delete()
            except ProtectedError:
                content = {
                    'status': MSG_RTOAR
                }
                return Response(content, status=status.HTTP_423_LOCKED)
            content = {
                'status': MSG_NOC
            }
            return Response(content, status=status.HTTP_204_NO_CONTENT)
        else:
            content = {
                'status': MSG_UN
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)



class get_post_activity_log(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Activity_LogSerializers

    def get_queryset(self):
        activity_log = Activity_Log.objects.all()
        return activity_log

    # Get all activity_log
    def get(self, request):
        activity_log = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Activity_LogSerializers(activity_log,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new activity_log
    def post(self, request):
        # actiontype = Activity_Log.objects.filter(
        #    action_type=request.data.get('action_type')).first()
        # activitylogid = Activity_Log.objects.filter(
        #     id=request.data.get('id')).first()
        if request.data:
        #     serializer = Activity_LogSerializers(data=request.data)
        #
        # if (activitylogid):
        #     serializer = Activity_LogSerializers(
        #         activitylogid, data=request.data)
        # else:
            serializer = Activity_LogSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
                return Response(dict, status=status.HTTP_201_CREATED)
            dict={"status":False,'status_code':400,"message":MSG_FAILED,"data":serializer.errors}
            return Response(dict, status=status.HTTP_400_BAD_REQUEST)
        else:
            msg={"status":False,"msg":"please add activity log"}
            return  Response(msg, status=status.HTTP_201_CREATED)


class bulk_upload_activity_type(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Activity_LogSerializers

    # bulk upload api(import ACTIVITYLOG)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             activity_log = Activity_Log.objects.filter(
    #                activity_type=value['activity_type']).first()
    #             value=value.to_dict()
    #             if (activity_log):
    #                 continue
    #             else:
    #                 serializer = Activity_LogSerializers(data=value)
    #             if serializer.is_valid():
    #                 serializer.save()
    #         return Response("File uploaded successfuly", status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    # bulk upload api(country import)
    def post(self, request):
        try:
            data = pd.read_excel(request.data.get("file"))
            sucessCount = 0
            failureCount = 0
            for i, value in data.iterrows():
                activity_log = Activity_Log.objects.filter(
                    activity_type=value['activity_type']).first()
                value = value.to_dict()
                if (activity_log):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Activity_LogSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    activity_log = Activity_Log.objects.all()
                    serializer = Activity_LogSerializers(activity_log, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code':201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)


