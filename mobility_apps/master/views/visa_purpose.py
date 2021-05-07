from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.master.models import Visa_Purpose
from mobility_apps.master.serializers.visa_purpose import Visa_PurposeSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
import pandas as pd
from mobility_apps.response_message import *

class get_delete_update_visa_purpose(RetrieveDestroyAPIView):
    http_method_names = ['get', 'put', 'delete', 'head', 'options', 'trace']
    permission_classes = (IsAuthenticated,)
    serializer_class = Visa_PurposeSerializers

    def get_queryset(self, pk):
        try:
            visa_purpose = Visa_Purpose.objects.get(pk=self.kwargs['pk'])
        except Visa_Purpose.DoesNotExist:
            content = {
                'status': MSG_NF
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return visa_purpose

    # Get a visa_purpose
    def get(self, request, pk):
        visa_purpose = self.get_queryset(pk)
        serializer = Visa_PurposeSerializers(visa_purpose)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Delete a visa_purpose
    def delete(self, request, pk):
        visa_purpose = self.get_queryset(pk)

        if (True):  # If creator is who makes request
            try:
                visa_purpose.delete()
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



class get_post_visa_purpose(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Visa_PurposeSerializers

    def get_queryset(self):
        visa_purpose = Visa_Purpose.objects.all()
        return visa_purpose

    # Get all visa_purpose
    def get(self, request):
        visa_purpose = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Visa_PurposeSerializers(visa_purpose,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new visa_purpose
    def post(self, request):
        visa_purposevpid = Visa_Purpose.objects.filter(
           VPID=request.data.get('VPID')).first()
        if (visa_purposevpid):
            serializer = Visa_PurposeSerializers(
                visa_purposevpid, data=request.data)
        else:
            serializer = Visa_PurposeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
            return Response(dict, status=status.HTTP_201_CREATED)
        dict={"status":False,'status_code':400,"message":MSG_FAILED,"data":serializer.errors}
        return Response(dict, status=status.HTTP_400_BAD_REQUEST)


class bulk_upload_visa_purpose(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Visa_PurposeSerializers

    # bulk upload api(import VISAPURPOSE)
    def post(self, request):
        try:
            data=pd.read_excel(request.data.get("file"))
            sucessCount = 0
            failureCount = 0
            for i, value in data.iterrows():
                visa_purpose = Visa_Purpose.objects.filter(
                    visa_id=value['VPID']).first()
                value = value.to_dict()
                if (visa_purpose):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Visa_PurposeSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    visa = Visa_Purpose.objects.all()
                    serializer =Visa_PurposeSerializers(visa, many=True)
                    dict = {'message': MSG_EXCELSU, 'status_code':201,'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)

class get_post_visa_purpose_list(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Visa_PurposeSerializers

    # Get all visa_purpose
    def get(self, request):
        org_id = request.GET.get('organization', None)
        country_id = request.GET.get('country_id', None)
        if org_id is not None and country_id is not None:
               visa_purpose = Visa_Purpose.objects.filter(organization=org_id, country_id=country_id)
               serializer = Visa_PurposeSerializers(visa_purpose,many=True)
               if serializer.data:
                  dict = {"status": True, "Message":MSG_SUCESS, "data": serializer.data}
               else:
                   dict = {"status": True, "Message":MSG_SUCESS, "data": serializer.data}
        elif country_id is None and org_id is not None:
            visa_purpose = Visa_Purpose.objects.filter(organization=org_id)
            serializer = Visa_PurposeSerializers(visa_purpose, many=True)
            if serializer.data:
                dict = {"status": True, "Message": MSG_SUCESS, "data": serializer.data}
            else:
                dict = {"status": True, "Message": MSG_SUCESS, "data": serializer.data}
        elif country_id is not None and org_id is None:
            visa_purpose = Visa_Purpose.objects.filter(country_id=country_id)
            serializer = Visa_PurposeSerializers(visa_purpose, many=True)
            if serializer.data:
                dict = {"status": True, "Message": MSG_SUCESS, "data": serializer.data}
            else:
                dict = {"status": True, "Message": MSG_SUCESS, "data": serializer.data}
        else:
            visa_purpose = Visa_Purpose.objects.all()
            serializer = Visa_PurposeSerializers(visa_purpose, many=True)
            if serializer.data:
                dict = {"status": True, "Message": MSG_SUCESS, "data": serializer.data}
            else:
                dict = {"status": True, "Message": MSG_SUCESS, "data": serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = Visa_PurposeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict = {'message': 'Successful', 'status': True, 'data': serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)



##############################################
# update purpose of travel
##############################################

class update_purpose_of_travel(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Visa_PurposeSerializers

    def get_object(self, pk):
        return Visa_Purpose.objects.get(pk=pk)

    def patch(self, request, pk):
        instance = self.get_object(pk)
        serializer = Visa_PurposeSerializers(instance,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            dict = {'message': 'Successful', 'status': True, 'data': serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)