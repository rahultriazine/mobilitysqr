from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.master.models import Visa_Document_Checklist
from mobility_apps.master.serializers.visa_document_checklist import Visa_Document_ChecklistSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
import pandas as pd
from mobility_apps.response_message import *

class get_post_visa_document_checklist(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Visa_Document_ChecklistSerializers

    def get_queryset(self):
        visa_document_checklist = Visa_Document_Checklist.objects.all()
        return visa_document_checklist

    # Get all visa_document_checklist
    def get(self, request):
        visa_document_checklist = self.get_queryset()
        serializer = Visa_Document_ChecklistSerializers(visa_document_checklist,many=True)
        dict = {'massage code':'001', 'massage': 'data found', 'status': True, 'data': serializer.data}
        return Response(dict , status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new visa_document_checklist

    def post(self, request):

        visadocumentchecklist = Visa_Document_Checklist.objects.filter(visa_id__visa_id=request.data.get('visa_id')).first()
        if (visadocumentchecklist):
            serializer = Visa_Document_ChecklistSerializers(
                visadocumentchecklist, data=request.data)
        else:
            serializer = Visa_Document_ChecklistSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#
# class bulk_upload_visa_document_checklist(ListCreateAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = Visa_Document_ChecklistSerializers

# bulk upload api(import visadocumentchecklist)
# def post(self, request):
#     try:
#         data=pd.read_excel(request.data.get("file"))
#         for i, value in data.iterrows():
#             visa_document_checklist = Visa_Document_Checklist.objects.filter(
#                visa_id__visa_id=value['visa_id']).first()
#             value=value.to_dict()
#             if (visa_document_checklist):
#                 continue
#             else:
#                 serializer = Visa_Document_ChecklistSerializers(data=value)
#             if serializer.is_valid():
#                 serializer.save()
#         return Response("File uploaded successfuly", status=status.HTTP_201_CREATED)
#     except Exception as e:
#         return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
class bulk_upload_visa_document_checklist(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = Visa_Document_ChecklistSerializers


    def post(self, request):
        # import ipdb;ipdb.set_trace()
        try:
            data=pd.read_excel(request.data.get("file"))
            sucessCount = 0
            failureCount = 0
            for i, value in data.iterrows():
                visa_document_checklist = Visa_Document_Checklist.objects.filter(
                    visa_id__visa_id=value['visa_id']).first()
                value = value.to_dict()
                if (visa_document_checklist):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Visa_Document_ChecklistSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    visa_document_checklist = Visa_Document_Checklist.objects.all()
                    serializer = Visa_Document_ChecklistSerializers(visa_document_checklist, many=True)
                    dict = {'message':MSG_EXCELSU, 'status': 'True','status_code':201, 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message':MSG_EXCELF, 'status': 'False','status_code':406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)


class get_visa_country_checklist(RetrieveDestroyAPIView):
    #permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    serializer_class = Visa_Document_ChecklistSerializers

    #permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    #serializer_class = VisaSerializers

    def get_queryset(self, visa):
        try:
            visa_checklist = Visa_Document_Checklist.objects.filter(visa=visa)
        # print(visa)
        except visa_checklist.DoesNotExist:

            return []
        return visa_checklist

    # Get a visa country checklist
    def get(self, request):
        # import ipdb;ipdb.set_trace()
        visa_checklist = self.get_queryset(request.GET["visa"])
        # print(visa)
        if visa_checklist:
            serializer = Visa_Document_ChecklistSerializers(visa_checklist,many=True)
            dict = {"status": True,"status_code": 200, "Message":MSG_SUCESS, "data": serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'status': "False","status_code": 200, 'Message':MSG_FAILED}
            return Response(dict, status=status.HTTP_200_ok)

