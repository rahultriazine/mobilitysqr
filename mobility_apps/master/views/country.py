from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.superadmin.models import Organizations,Organization_branches,Organization_users
from mobility_apps.superadmin.serializers import UserinfoSerializers,OrganizationsSerializers,Organization_branchesSerializers,Organization_usersSerializers
from mobility_apps.master.models import Country,City,Per_Diem,Dial_Code,Country_Master,State_Master,Location_Master,Taxgrid_Master,Taxgrid_Country,Taxgrid,National_Id,Designation,Country_Policy
from mobility_apps.master.serializers.country import CountrySerializers ,CitySerializers,Per_DiemSerializers,Dial_CodeSerializers,Country_MasterSerializers,State_MasterSerializers,Location_MasterSerializers,Taxgrid_MasterSerializers,Taxgrid_CountrySerializers,TaxgridSerializers,National_IdSerializers,DesignationSerializers,Country_PolicySerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
from mobility_apps.response_message import *
from django.db import connection
from django.db.models import Q
# from rest_framework_bulk import (
#     BulkListSerializer,
#     BulkSerializerMixin,
#     ListBulkCreateUpdateDestroyAPIView,
# )
import math
from dateutil import tz
from datetime import datetime,date
class get_delete_update_country(RetrieveDestroyAPIView):
    http_method_names = ['get', 'put', 'delete', 'head', 'options', 'trace']
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    serializer_class = CountrySerializers

    def get_queryset(self, country_code):
        try:
            country = Country.objects.get(country_code=country_code)
        except Country.DoesNotExist:

            return []
        return country

    # Get a vendor
    def get(self, request):
        # import ipdb;ipdb.set_trace()
        country = self.get_queryset(request.GET["country_code"])
        if country:
            serializer = CountrySerializers(country)
            dict = {"status": True, "msg": "data found", "data": serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'status': False, 'msg': 'data Not Found'}
            return Response(dict, status=status.HTTP_404_NOT_FOUND)

    # Delete a vendor
    def delete(self, request):
        country = self.get_queryset(request.data["country_code"])
        if country:  # If creator is who makes request
            try:
                country.delete()
            except ProtectedError:
                content = {
                    'status': 'This resource is related to other active record.'
                }
                return Response(content, status=status.HTTP_423_LOCKED)
            content = {
                'status': True,
                "msg":"data deleted successfully"
            }
            return Response(content, status=status.HTTP_204_NO_CONTENT)
        else:
            content = {"status":False,
                       'msg': 'data not found'
                       }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)



class get_post_country(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = CountrySerializers

    def get_queryset(self):
        country = Country.objects.all()
        return country

    # Get all country:
    def get(self, request):
        country = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = CountrySerializers(country,many=True)
        dict = {'message':MSG_SUCESS,'status_code':200, 'status': True,'data': serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new country
    def post(self, request):
        country = Country.objects.filter(
           country_code=request.data.get('country_code')).first()
        if (country):
            serializer = CountrySerializers(
                country, data=request.data)
        else:
            serializer = CountrySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict = {'message':MSG_SUCESS,'status_code':201, 'status': True,'data': serializer.data}
            return Response(dict,serializer.data, status=status.HTTP_201_CREATED)
        dict = {'message':MSG_FAILED,'status_code':200, 'status': False,'data': serializer.errors}
        return Response(dict, status=status.HTTP_200_OK)


class bulk_upload_country(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CountrySerializers

    # bulk upload api(country import)
    def post(self, request):
        try:
            data=pd.read_excel(request.data.get("file"))
            sucessCount = 0
            failureCount = 0
            for i, value in data.iterrows():
                country = Country.objects.filter(
                   country_code=value['country_code']).first()
                value=value.to_dict()
                if (country):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = CountrySerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    country = Country.objects.all()
                    serializer = CountrySerializers(country, many=True)
                    dict = {'message':MSG_EXCELSU, 'status': True,'status_code':201, 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message':MSG_EXCELF, 'status': False,'status_code':406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)

class bulk_upload_country_master(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Country_MasterSerializers

    # bulk upload api(country import)
    def post(self, request):
        try:
            data=pd.read_excel(request.data.get("file"))
            sucessCount = 0
            failureCount = 0
            for i, value in data.iterrows():
                country = Country_Master.objects.filter(
                   country_id=value['country_id']).first()
                value=value.to_dict()
                if (country):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Country_MasterSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    country = Country_Master.objects.all()
                    serializer = Country_MasterSerializers(country, many=True)
                    dict = {'message':MSG_EXCELSU, 'status': True,'status_code':201, 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message':MSG_EXCELF, 'status': False,'status_code':406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)

class bulk_upload_city(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CitySerializers

    # bulk upload api(country import)
    def post(self, request):
        try:
            data=pd.read_excel(request.data.get("file"))
            sucessCount = 0
            failureCount = 0
            for i, value in data.iterrows():
                city = City.objects.filter(
                    airport_id=value['airport_id']).first()
                value=value.to_dict()
                if (city):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = CitySerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    city = City.objects.all()
                    serializer = CitySerializers(city, many=True)
                    dict = {'message':MSG_EXCELSU, 'status': True,'status_code':201, 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message':MSG_EXCELF, 'status': False,'status_code':406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)

class get_city(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CitySerializers

    def get_queryset(self,city):
        try:
            country = City.objects.filter(city__icontains=city)
            print(country)
        except Country.DoesNotExist:

            return []
        return country

    # Get all country:
    def get(self, request):
        # import ipdb;ipdb.set_trace()
        city = self.get_queryset(request.GET["city"])
        # print(visa)
        if city:
            serializer = CitySerializers(city,many=True)
            for data in serializer.data:
             country_code=data['country']
             country_code=str(country_code).split('.')[0]
             print(country_code)
             country = Country.objects.filter(country_code=country_code)
             if country:
                country=CountrySerializers(country,many=True)
                data['country_name']=country.data[0]['country_name']
             else:
                data['country_name']=""
            dict = {"status": True, "Message":MSG_SUCESS, "data": serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'status': "False", 'Message':MSG_FAILED}
            return Response(dict, status=status.HTTP_200_OK)


class get_country(ListCreateAPIView):
    serializer_class = CountrySerializers

    def get_queryset(self, country_name):
        try:
            country = Country.objects.filter(country_name__icontains=country_name)
        # print(visa)
        except Country.DoesNotExist:

            return []
        return country

    # Get all country:
    def get(self, request):
        # import ipdb;ipdb.set_trace()
        country = self.get_queryset(request.GET["country_name"])
        # print(visa)
        if country:
            serializer = CountrySerializers(country,many=True)
            country=serializer.data[0]['country_code']

            dict = {"status": True, "Message":MSG_SUCESS, "data": serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'status': False, 'Message':MSG_FAILED}
            return Response(dict, status=status.HTTP_200_OK)


class bulk_upload_perdiem(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Per_DiemSerializers

    # bulk upload api(country import)
    def post(self, request):
        try:
            data=pd.read_excel(request.data.get("file"))
            sucessCount = 0
            failureCount = 0
            for i, value in data.iterrows():
                per_diem = Per_Diem.objects.filter(
                    country=value['country']).first()
                value=value.to_dict()
                if (per_diem):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Per_DiemSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    per_diem = Per_Diem.objects.all()
                    serializer = Per_DiemSerializers(per_diem, many=True)
                    dict = {'message':MSG_EXCELSU, 'status': True,'status_code':201, 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message':MSG_EXCELF, 'status': False,'status_code':406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)

class get_perdiem(ListCreateAPIView):
    serializer_class = Per_DiemSerializers

    def get_queryset(self,country,home_country,organization):
        try:
            per_diem = Per_Diem.objects.filter(country__icontains=country,home_country__icontains=home_country,organization=organization).order_by('effective_date').last()
        # print(visa)
        except Per_Diem.DoesNotExist:

            return []
        return per_diem

    # Get all country:
    def get(self, request):

        per_diem= self.get_queryset(request.GET['country'],request.GET['home_country'],request.GET['organization'])
        # print(visa)
        if per_diem:
            serializer = Per_DiemSerializers(per_diem)
            dict = {"status": True, "Message":MSG_SUCESS, "data": serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'status': False, 'Message':MSG_FAILED}
            return Response(dict, status=status.HTTP_200_OK)
			
class dial_code(ListCreateAPIView):
    serializer_class = Dial_CodeSerializers
    def post(self, request):
        # import ipdb;ipdb.set_trace()
        for data in request.data:
            serializer = Dial_CodeSerializers(data=data)
            if serializer.is_valid():
                serializer.save()
                dict = {"status": True, "Message":MSG_SUCESS, "data": serializer.data}
            else:
                dict = {'status': False, 'Message':MSG_FAILED}
        return Response(dict, status=status.HTTP_200_OK)


class get_dial_code(ListCreateAPIView):
    serializer_class = Dial_CodeSerializers
    def get(self, request):
        # import ipdb;ipdb.set_trace()
        print(request.GET['dial_code'])
        dial=Dial_Code.objects.filter(Q(name__icontains=request.GET['dial_code'])|Q(code__icontains=request.GET['dial_code'])).order_by('name')
        serializer = Dial_CodeSerializers(dial,many=True)
        if serializer.data:
            dict = {"status": True, "Message":MSG_SUCESS, "data": serializer.data}
        else:
            dict = {'status': False, 'Message':MSG_FAILED}
        return Response(dict, status=status.HTTP_200_OK)
		
class get_country_master(ListCreateAPIView):
    serializer_class = Country_MasterSerializers
    def get(self, request):
        # import ipdb;ipdb.set_trace()
        print(request.GET['country'])
        dial=Country_Master.objects.filter(Q(name__icontains=request.GET['country']))
        serializer = Country_MasterSerializers(dial,many=True)
        if serializer.data:
            dict = {"status": True, "Message":MSG_SUCESS, "data": serializer.data}
        else:
            dict = {'status': False, 'Message':MSG_FAILED}
        return Response(dict, status=status.HTTP_200_OK)

    def post(self, request):
        # import ipdb;ipdb.set_trace()
        for data in request.data:
            serializer = Country_MasterSerializers(data=data)
            if serializer.is_valid():
                serializer.save()
                dict = {"status": True, "Message":MSG_SUCESS, "data": serializer.data}
            else:
                dict = {'status': False, 'Message':MSG_FAILED}
        return Response(dict, status=status.HTTP_200_OK)

class get_state_master(ListCreateAPIView):
    serializer_class = State_MasterSerializers
    def get(self, request):
        # import ipdb;ipdb.set_trace()
        print(request.GET['country_id'])
        dial=State_Master.objects.filter(Q(country_id=request.GET['country_id']))
        serializer = State_MasterSerializers(dial,many=True)
        if serializer.data:
            dict = {"status": True, "Message":MSG_SUCESS, "data": serializer.data}
        else:
            dict = {'status': False, 'Message':MSG_FAILED}
        return Response(dict, status=status.HTTP_200_OK)

    def post(self, request):
        # import ipdb;ipdb.set_trace()
        for data in request.data:
            serializer = State_MasterSerializers(data=data)
            if serializer.is_valid():
                serializer.save()
                dict = {"status": True, "Message":MSG_SUCESS, "data": serializer.data}
            else:
                dict = {'status': "False", 'Message':MSG_FAILED}
        return Response(dict, status=status.HTTP_200_OK)


class bulk_upload_location(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Location_MasterSerializers

    # bulk upload api(country import)
    def post(self, request):
        try:
            data=pd.read_excel(request.data.get("file"))
            sucessCount = 0
            failureCount = 0
            for i, value in data.iterrows():
                city = Location_Master.objects.filter(
                    location_code=value['location_code']).first()
                value=value.to_dict()
                if (city):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Location_MasterSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    city = Location_Master.objects.all()
                    serializer = Location_MasterSerializers(city, many=True)
                    dict = {'message':MSG_EXCELSU, 'status': True,'status_code':201, 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message':MSG_EXCELF, 'status': False,'status_code':406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)
			
			
class bulk_upload_taxgrid(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Taxgrid_CountrySerializers

    # bulk upload api(country import)
    def post(self, request):
        try:
            data=pd.read_excel(request.data.get("file"))
            print(data)
            sucessCount = 0
            failureCount = 0
            for i, value in data.iterrows():
                per_diem = Taxgrid_Country.objects.filter(
                    tax_label=value['tax_label']).first()
                value=value.to_dict()
                if (per_diem):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Taxgrid_CountrySerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    per_diem = Taxgrid_Country.objects.all()
                    serializer = Taxgrid_CountrySerializers(per_diem, many=True)
                    dict = {'message':MSG_EXCELSU, 'status': 'True','status_code':201, 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
                else:
                    print(serializer.errors)
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message':MSG_EXCELF, 'status': 'False','status_code':406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)



class get_post_location(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Location_MasterSerializers

    def post(self, request):
        serializers_data = Location_MasterSerializers(data=request.data)
        if serializers_data.is_valid():
           serializers_data.save()
           dict = {'message': MSG_SUCESS, 'status_code': 200, 'status': True, 'data': serializers_data.data}
           return Response(dict, status=status.HTTP_200_OK)
        else:
           dict = {'message': MSG_FAILED, 'status_code': 400, 'status': False, 'data': serializers_data.errors}
           return Response(dict, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        country = Location_Master.objects.filter(country=request.GET['country']).order_by('location_name')
        serializer = Location_MasterSerializers(country,many=True)
        dict = {'message':MSG_SUCESS,'status_code':200, 'status': True,'data': serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

##############################################
# update purpose of travel
##############################################

class update_master_location(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Location_MasterSerializers

    def get_object(self, pk):
        return Location_Master.objects.get(pk=pk)

    def patch(self, request, pk):
        instance = self.get_object(pk)
        serializer = Location_MasterSerializers(instance,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            dict = {'message': 'Successful', 'status': True, 'data': serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)



class get_taxgridcountry(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Location_MasterSerializers

    def get_queryset(self):
        country = Taxgrid_Country.objects.all()
        return country

    # Get all country:
    def get(self, request):
        country = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Taxgrid_CountrySerializers(country,many=True)
        dict = {'message':MSG_SUCESS,'status_code':200, 'status': True,'data': serializer.data}
        return Response(dict, status=status.HTTP_200_OK)


class get_taxgridmaster(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Taxgrid_MasterSerializers

    def get_queryset(self):
        country = Taxgrid_Master.objects.all()
        return country

    # Get all country:
    def get(self, request):
        taxgrid = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Taxgrid_MasterSerializers(taxgrid,many=True)
        dict = {'message':MSG_SUCESS,'status_code':200, 'status': True,'data': serializer.data}
        return Response(dict, status=status.HTTP_200_OK)


class add_taxgrid(ListCreateAPIView):
    serializer_class = TaxgridSerializers
    def get_queryset(self):
        taxgrid = Taxgrid.objects.all()
        return taxgrid

# Get all country:
    def get(self, request):
        taxgrid = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = TaxgridSerializers(taxgrid,many=True)
        dict = {'message':MSG_SUCESS,'status_code':200, 'status': True,'data': serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
    def post(self, request):
        # import ipdb;ipdb.set_trace()
        alldata=[]
        for data in request.data:

            taxgrid=Taxgrid.objects.filter(tax_label=data['tax_label'],organization=data['organization']).first()
            print(taxgrid)
            if taxgrid:
                print(data)
                serializer = TaxgridSerializers(taxgrid,data=data)
                if serializer.is_valid():
                    serializer.save()
                    print(serializer.data)
                    alldata.append(serializer.data)
                    dict = {"status": True, "Message":MSG_SUCESS, "data": alldata}
                else:
                    dict = {'status': "False", 'Message':MSG_FAILED,"data":serializer.errors}
            else:
                serializer = TaxgridSerializers(data=data)
                if serializer.is_valid():
                    serializer.save()
                    alldata.append(serializer.data)
                    dict = {"status": True, "Message":MSG_SUCESS, "data": alldata}
                else:
                    dict = {'status': "False", 'Message':MSG_FAILED}
        return Response(dict, status=status.HTTP_200_OK)


class bulk_upload_national_id(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class =National_IdSerializers

    # bulk upload api(country import)
    def post(self, request):
        try:
            data=pd.read_excel(request.data.get("file"))
            sucessCount = 0
            failureCount = 0
            for i, value in data.iterrows():
                per_diem = National_Id.objects.filter(
                    country=value['country']).first()
                value=value.to_dict()
                if (per_diem):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = National_IdSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    per_diem = National_Id.objects.all()
                    serializer = National_IdSerializers(per_diem, many=True)
                    dict = {'message':MSG_EXCELSU, 'status': 'True','status_code':201, 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message':MSG_EXCELF, 'status': 'False','status_code':406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)

class get_national_id(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Taxgrid_MasterSerializers

    def get_queryset(self,country):
        country = National_Id.objects.filter(country=country)
        return country

    # Get all country:
    def get(self, request):
        taxgrid = self.get_queryset(request.GET['country'])
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = National_IdSerializers(taxgrid,many=True)
        if serializer:
           dict = {'message':MSG_SUCESS,'status_code':200, 'status': True,'data': serializer.data}
        else:
           dict = {'message':MSG_SUCESS,'status_code':200, 'status': True,'data': []}
        return Response(dict, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = National_IdSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict = {"status": True, "message": 'Successfully inserted', "data": serializer.data}
        else:
            dict = {"status": False, "message": 'Failed to insert data', "data": serializer.errors}
        return Response(dict, status=status.HTTP_200_OK)


##############################################
# update master National id
##############################################

class update_master_national_id(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = National_IdSerializers

    def get_object(self, pk):
        return National_Id.objects.get(pk=pk)

    def patch(self, request, pk):
        instance = self.get_object(pk)
        serializer = National_IdSerializers(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            dict = {'message': 'Successful', 'status': True, 'data': serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)




class tax_grid_country_update(ListCreateAPIView):
    def post(self, request):
        #taxgrid = self.get_queryset(request.GET['country'])
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        cursor = connection.cursor()
        # class CursorByName():
        #     def __init__(self, cursor):
        #         self._cursor = cursor

        #     def __iter__(self):
        #         return self

        #     def __next__(self):
        #         row = self._cursor.__next__()
        #         return { description[0]: row[col] for col, description in enumerate(self._cursor.description) }
                
        #sql ="UPDATE master_location_master SET group='null' WHERE group='nan'"
        #sql ="SELECT  * FROM master_country_policy WHERE country_code='AE'"
        sql ="DELETE FROM master_vendor_category"
        cursor.execute(sql)
        # datas=[]
        # for data in CursorByName(cursor):
        #     datas.append(data)
        # from_zone = tz.tzutc()
        # to_zone = tz.tzlocal()
        # date=str('2020-11-10 18:30:00+00:00')[:-3]
        # # utc = datetime.utcnow()
        # utc = datetime.strptime(date, '%Y-%m-%d %H:%M:%S+%f')

        # # Tell the datetime object that it's in UTC time zone since 
        # # datetime objects are 'naive' by default
        # utc = utc.replace(tzinfo=from_zone)

        # # Convert time zone
        # central = utc.astimezone(to_zone)
        # print(central)
        dict = {'message':'datas','status_code':200, 'status': True}
    
        return Response(dict, status=status.HTTP_200_OK)



class get_all_location(ListCreateAPIView):
    
    def get(self, request):
        country = Location_Master.objects.filter(Q(location_name__icontains=request.GET['name'])|Q(city__icontains=request.GET['name']))
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Location_MasterSerializers(country,many=True)
        dict = {'message':MSG_SUCESS,'status_code':200, 'status': True,'data': serializer.data}
        return Response(dict, status=status.HTTP_200_OK)


class get_designation(ListCreateAPIView):
    
    def get(self, request):
        country = Designation.objects.filter(name__icontains=request.GET['name'])
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = DesignationSerializers(country,many=True)
        dict = {'message':MSG_SUCESS,'status_code':200, 'status': True,'data': serializer.data}
        return Response(dict, status=status.HTTP_200_OK)



class bulk_upload_designation(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class =DesignationSerializers

    # bulk upload api(country import)
    def post(self, request):
        try:
            data=pd.read_excel(request.data.get("file"))
            sucessCount = 0
            failureCount = 0
            for i, value in data.iterrows():
                per_diem = Designation.objects.filter(
                    name=value['name']).first()
                value=value.to_dict()
                if (per_diem):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = DesignationSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    per_diem = Designation.objects.all()
                    serializer = DesignationSerializers(per_diem, many=True)
                    dict = {'message':MSG_EXCELSU, 'status': 'True','status_code':201, 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message':MSG_EXCELF, 'status': 'False','status_code':406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)

class active_taxgrid(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaxgridSerializers
# Get all country:
    def get(self, request):
        try:
            taxgrid = Taxgrid.objects.filter(organization=request.GET['org'],status=True)
            # paginate_queryset = self.paginate_queryset(employee)
            # serializer = self.serializer_class(paginate_queryset, many=True)
            serializer = TaxgridSerializers(taxgrid,many=True)
            dict = {'message':MSG_SUCESS,'status_code':200, 'status': True,'data': serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            dict = {'message':MSG_FAILED, 'status': 'False','status_code':406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)


class add_taxgrid_label(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaxgridSerializers
    # Add new taxgid label:
    def post(self, request):
        try:
            taxgrid = Taxgrid.objects.filter(tax_label=request.data['tax_label']).first()
            # paginate_queryset = self.paginate_queryset(employee)
            # serializer = self.serializer_class(paginate_queryset, many=True)
            if taxgrid:
                serializer = TaxgridSerializers(taxgrid,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'message':MSG_UPDATE,'status_code':200, 'status': True,'data': serializer.data}
                else:
                    dict = {'message':MSG_UPDATE,'status_code':200, 'status': True,'data': serializer.errors}
            else:
                serializer = TaxgridSerializers(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'message':MSG_ADDED,'status_code':200, 'status': True,'data': serializer.data}
                else:
                    dict = {'message':MSG_UPDATE,'status_code':200, 'status': True,'data': serializer.errors}
            return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            dict = {'message':MSG_FAILED, 'status': 'False','status_code':406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)



class bulk_upload_designation(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class =DesignationSerializers

    # bulk upload api(country import)
    def post(self, request):
        try:
            data=pd.read_excel(request.data.get("file"))
            sucessCount = 0
            failureCount = 0
            for i, value in data.iterrows():
                per_diem = Designation.objects.filter(
                    name=value['name']).first()
                value=value.to_dict()
                if (per_diem):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = DesignationSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    per_diem = Designation.objects.all()
                    serializer = DesignationSerializers(per_diem, many=True)
                    dict = {'message':MSG_EXCELSU, 'status': 'True','status_code':201, 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message':MSG_EXCELF, 'status': 'False','status_code':406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)


class bulk_upload_country_policy(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class =Country_PolicySerializers

    # bulk upload api(country import)
    def post(self, request):
        try:
            data=pd.read_excel(request.data.get("file"))
            sucessCount = 0
            failureCount = 0
            for i, value in data.iterrows():
                per_diem = Country_Policy.objects.filter(
                    country_id=value['country_id']).first()
                value=value.to_dict()
                if (per_diem):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Country_PolicySerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    per_diem = Country_Policy.objects.all()
                    serializer = Country_PolicySerializers(per_diem, many=True)
                    dict = {'message':MSG_EXCELSU, 'status': 'True','status_code':201, 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message':MSG_EXCELF, 'status': 'False','status_code':406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)

class get_post_country_policy(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Country_PolicySerializers
    
    # Get all country:
    def get(self, request):
        days=int(request.GET['days'])
        criterion1 = Q(country_name=request.GET['country_code'])
        country = Country_Policy.objects.filter(criterion1).values('bv_threshold')
        print(country[0]['bv_threshold'])
        if int(country[0]['bv_threshold'])<days:
           dict = {'message':MSG_SUCESS,'status_code':200, 'status': True,'policy_violations': 'Yes'}
        else:
           dict = {'message':MSG_SUCESS,'status_code':200, 'status': True,'policy_violations': 'No'}
        return Response(dict, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            taxgrid = Country_Policy.objects.filter(id=request.data['id']).first()
            # paginate_queryset = self.paginate_queryset(employee)
            # serializer = self.serializer_class(paginate_queryset, many=True)
            if taxgrid:
                serializer = Country_PolicySerializers(taxgrid,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'message':MSG_UPDATE,'status_code':200, 'status': True,'data': serializer.data}
                else:
                    dict = {'message':MSG_UPDATE,'status_code':200, 'status': True,'data': serializer.errors}
            else:
                serializer = Country_PolicySerializers(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'message':MSG_ADDED,'status_code':200, 'status': True,'data': serializer.data}
                else:
                    dict = {'message':MSG_UPDATE,'status_code':200, 'status': True,'data': serializer.errors}
            return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            dict = {'message':MSG_FAILED, 'status': 'False','status_code':406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)





class post_country_policy(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Country_PolicySerializers
    
    # Get all country:
    def get(self, request):
        organization_id = request.GET.get('organization_id', None)
        home_country = request.GET.get('home_country', None)
        if organization_id is None:
            dict = {'message': "Organization id is required", 'status': False}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            if home_country is None:
                country = Country_Policy.objects.filter(organization_id=organization_id).order_by('id')
                serializer = Country_PolicySerializers(country,many=True)
                dict = {'message':MSG_SUCESS,'status': True, 'data': serializer.data}
                return Response(dict, status=status.HTTP_200_OK)
            else:
                country = Country_Policy.objects.filter(organization_id=organization_id,home_country=home_country).order_by('id')
                serializer = Country_PolicySerializers(country, many=True)
                dict = {'message': MSG_SUCESS, 'status': True, 'data': serializer.data}
                return Response(dict, status=status.HTTP_200_OK)


    def post(self, request):
        try:
            taxgrid = Country_Policy.objects.filter(id=request.data['id']).first()
            # paginate_queryset = self.paginate_queryset(employee)
            # serializer = self.serializer_class(paginate_queryset, many=True)
            if taxgrid:
                serializer = Country_PolicySerializers(taxgrid,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'message':MSG_UPDATE,'status_code':200, 'status': True,'data': serializer.data}
                else:
                    dict = {'message':MSG_UPDATE,'status_code':200, 'status': True,'data': serializer.errors}
            else:
                serializer = Country_PolicySerializers(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'message':MSG_ADDED,'status_code':200, 'status': True,'data': serializer.data}
                else:
                    dict = {'message':MSG_UPDATE,'status_code':200, 'status': True,'data': serializer.errors}
            return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            dict = {'message':MSG_FAILED, 'status': 'False','status_code':406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)



###########################################################
" bulk Upload country json"
###########################################################

class json_upload_country(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CountrySerializers

    def post(self, request, *args, **kwargs):
        try:
            serializer = CountrySerializers(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            dict = {'message':e, 'status': False,'status_code':406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)


##########################################################
" json upload city"
##########################################################

class json_upload_city(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CitySerializers
    def post(self, request, *args, **kwargs):
        try:
            serializer = CitySerializers(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            dict = {'message':e, 'status': False,'status_code':406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)
