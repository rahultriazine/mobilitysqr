from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.master.models import Visa,Visa_Master,Visa_Master_Applicable
from mobility_apps.master.serializers.visa import VisaSerializers,Visa_MasterSerializers,Visa_Master_ApplicableSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
import pandas as pd
from mobility_apps.response_message import *

class get_delete_update_visa(RetrieveDestroyAPIView):
    http_method_names = ['get', 'put', 'delete', 'head', 'options', 'trace']
    #permission_classes = (IsAuthenticated,)
    serializer_class = VisaSerializers

    def get_queryset(self, pk):
        try:
            visa = Visa.objects.get(pk=self.kwargs['pk'])
        except Visa.DoesNotExist:
            content = {
                'status': MSG_NF
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return visa

    # Get a visa
    def get(self, request, pk):
        visa = self.get_queryset(pk)
        serializer = VisaSerializers(visa)
        dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    # Delete a visa
    def delete(self, request, pk):
        visa = self.get_queryset(pk)

        if (True):  # If creator is who makes request
            try:
                visa.delete()
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



class get_post_visa(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = VisaSerializers

    def get_queryset(self):
        visa = Visa.objects.all()
        return visa

    # Get all visa
    def get(self, request):
        visa = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = VisaSerializers(visa,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new visa
    def post(self, request):
        visaid = Visa.objects.filter(
            visa_id=request.data.get('visa_id')).first()
        if (visaid):
            serializer = VisaSerializers(
                visaid, data=request.data)
        else:
            serializer = VisaSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
            return Response(dict, status=status.HTTP_201_CREATED)
        dict={"status":False,'status_code':200,"message":MSG_FAILED,"data":serializer.errors}
        return Response(dict, status=status.HTTP_200_OK)


class bulk_upload_visa(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = VisaSerializers


    # bulk upload api(import VISA)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             visa = Visa.objects.filter(
    #                visa_id=value['visa_id']).first()
    #             value=value.to_dict()
    #             if (visa):
    #                 continue
    #             else:
    #                 serializer = VisaSerializers(data=value)
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
                visa = Visa.objects.filter(
                    visa_id=value['visa_id']).first()
                value = value.to_dict()
                if (visa):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = VisaSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    visa = Visa.objects.all()
                    serializer = VisaSerializers(visa, many=True)
                    dict = {'message': MSG_EXCELSU, 'status_code':201,'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)

class get_visa_country(RetrieveDestroyAPIView):
    #permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    serializer_class = VisaSerializers

    def get_queryset(self, country,visa_type):
        try:
            visa = Visa.objects.filter(country=country,visa_type=visa_type)
        # print(visa)
        except Visa.DoesNotExist:

            return []
        return visa

    # Get a vendor
    def get(self, request):
        # import ipdb;ipdb.set_trace()
        visa = self.get_queryset(request.GET["country"],request.GET["visa_type"])
        print(visa)
        if visa:
            serializer = VisaSerializers(visa,many=True)
            dict = {"status": True, "message":MSG_SUCESS, "data": serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'status': False,"status_code":'200', 'message':MSG_NF}
            return Response(dict, status=status.HTTP_200_OK)

    # Delete a vendor
class get_post_visa_master(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VisaSerializers

    def get_queryset(self):
        visa = Visa_Master.objects.all()
        return visa

    # Get all visa
    def get(self, request):
        # visa = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        org_id = self.request.GET.get('org_id',None)
        visa = Visa_Master.objects.filter(organization=org_id)

        serializer = Visa_MasterSerializers(visa,many=True)
        if serializer:
           dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        else:
           dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.errors}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    def post(self, request):
        #visa = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Visa_MasterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        else:
            dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.errors}
        return Response(dict, status=status.HTTP_200_OK)

class get_post_visa_master_applicable(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Visa_Master_ApplicableSerializers

    def get(self, request):
        visa=Visa_Master_Applicable.objects.filter(applicable_country=request.GET["applicable_country"],visa_type=request.GET["visa_type"],organization=request.GET["org_id"])
        print(visa)
        visas=Visa_Master_ApplicableSerializers(visa,many=True)

        if visas:
            x=0
            for visass in visas.data:
                print(visass['document_id'])
                visad=Visa_Master.objects.filter(id=visass['document_id'])
                visadd = Visa_MasterSerializers(visad,many=True)
                print(visadd.data[0]['document_name'])
                visas.data[x]['document_name']=visadd.data[0]['document_name']
                visas.data[x]['document_type']=visadd.data[0]['document_type']
                x=int(x)+1
            dict = {'massage': 'data found', 'status': True, 'data': visas.data}
        else:
            dict = {'massage': 'data not found', 'status': True, 'data': []}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)
        # Create a new employee
    def post(self, request):
        # import ipdb;ipdb.set_trace()

        try:
            ditsct=[]
            for data in request.data:
                if data['update_id']:
                    for document in data['update_id']:
                        data['update_id']=document
                        print(data['update_id'])
                        ditsct.append(data['update_id'])

                        assignments=Visa_Master_Applicable.objects.filter(id=data['update_id']).first()
                        assignments.delete()
                        dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data':ditsct}
                if data['document_id']:
                    for document in data['document_id']:
                        data['document_id']=document
                        assignment=Visa_Master.objects.filter(id=document).values("host_type")
                        if assignment:
                            data['host_type']=assignment[0]['host_type']
                        else:
                            data['host_type']=""
                        assignment_travel=Visa_Master_ApplicableSerializers(data=data)
                        if assignment_travel.is_valid():
                            id=assignment_travel.save().id
                            ditsct.append(id)
                            dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data':ditsct}
                        else:
                            dict = {'massage code': '200', 'massage': 'successful', 'status': True, 'data':assignment_travel.errors}
            return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            dict = {'massage code': 'already exists', 'massage': 'unsuccessful', 'status': 'False','data':str(e)}
            return Response(dict, status=status.HTTP_200_OK)