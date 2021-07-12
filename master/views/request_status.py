from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.master.models import Request_Status
from mobility_apps.master.serializers.request_status import Request_StatusSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
import pandas as pd
from mobility_apps.response_message import *

class get_delete_update_reuest_status(RetrieveDestroyAPIView):
    http_method_names = ['get', 'put', 'delete', 'head', 'options', 'trace']
    permission_classes = (IsAuthenticated,)
    serializer_class = Request_StatusSerializers

    def get_queryset(self, pk):
        try:
            request_status = Request_Status.objects.get(pk=self.kwargs['pk'])
        except Request_Status.DoesNotExist:
            content = {
                'status': MSG_NF
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return request_status

    # Get a rewuest_status
    def get(self, request, pk):
        request_status = self.get_queryset(pk)
        serializer = Request_StatusSerializers(request_status)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Delete a coutry
    def delete(self, request, pk):
        request_status = self.get_queryset(pk)

        if (True):  # If creator is who makes request
            try:
                request_status.delete()
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



class get_post_reuest_status(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Request_StatusSerializers

    def get_queryset(self):
        request_status = Request_Status.objects.all()
        return request_status

    # Get all requeststatus
    def get(self, request):
        request_status = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Request_StatusSerializers(request_status,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new requeststatus
    def post(self, request):
        statusid = Request_Status.objects.filter(
           status_id=request.data.get('status_id')).first()
        if (statusid):
            serializer = Request_StatusSerializers(
                statusid, data=request.data)
        else:
            serializer = Request_StatusSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
            return Response(data, status=status.HTTP_201_CREATED)
        dict={"status":False,'status_code':400,"message":MSG_SUCESS,"data":serializer.errors}
        return Response(dict, status=status.HTTP_400_BAD_REQUEST)


class bulk_upload_request_status(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Request_StatusSerializers

    # bulk upload api(import request status)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             request_status = Request_Status.objects.filter(
    #                status_id=value['status_id']).first()
    #             value=value.to_dict()
    #             if (request_status):
    #                 continue
    #             else:
    #                 serializer = Request_StatusSerializers(data=value)
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
                request_status = Request_Status.objects.filter(
                    status_id=value['status_id']).first()
                value = value.to_dict()
                if (request_status):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Request_StatusSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    request_status = Request_Status.objects.all()
                    serializer = Request_StatusSerializers(request_status, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code':201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':400, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)



