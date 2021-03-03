from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.master.models import Organization_Location
from mobility_apps.master.serializers.organization_location import Organization_LocationSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
import pandas as pd
from mobility_apps.response_message import *

class get_delete_update_organization_location(RetrieveDestroyAPIView):
    http_method_names = ['get', 'put', 'delete', 'head', 'options', 'trace']
    permission_classes = (IsAuthenticated,)
    serializer_class = Organization_LocationSerializers

    def get_queryset(self, pk):
        try:
            organization_location = Organization_Location.objects.get(pk=self.kwargs['pk'])
        except Organization_Location.DoesNotExist:
            content = {
                'status': MSG_NF
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return organization_location

    # Get a organizatioin_location
    def get(self, request, pk):
        organization_location = self.get_queryset(pk)
        serializer = Organization_LocationSerializers(Organization_Location)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Delete a coutry
    def delete(self, request, pk):
        organization = self.get_queryset(pk)

        if (True):  # If creator is who makes request
            try:
                organization.delete()
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



class get_post_organization_location(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Organization_LocationSerializers

    def get_queryset(self):
        organization_location = Organization_Location.objects.all()
        return organization_location

    # Get all organization
    def get(self, request):
        organization_location = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Organization_LocationSerializers(organization_location,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict ,status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new organization
    def post(self, request):
        locationid= Organization_Location.objects.filter(
           location_id=request.data.get('location_id')).first()
        if (locationid):
            serializer = Organization_LocationSerializers(
                locationid, data=request.data)
        else:
            serializer = Organization_LocationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
            return Response(dict, status=status.HTTP_201_CREATED)
        dict={"status":True,'status_code':400,"message":MSG_FAILED,"data":serializer.errors}
        return Response(dict, status=status.HTTP_400_BAD_REQUEST)


class bulk_upload_organization_location(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Organization_LocationSerializers

    # bulk upload api(import ORGANIZATION LOCATION)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             organization_location = Organization_Location.objects.filter(
    #                location_id=value['location_id']).first()
    #             value=value.to_dict()
    #             if (organization_location):
    #                 continue
    #             else:
    #                 serializer = Organization_LocationSerializers(data=value)
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
                organization_location = Organization_Location.objects.filter(
                    location_id=value['location_id']).first()
                value = value.to_dict()
                if (organization_location):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Organization_LocationSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    organization_location = Organization_Location.objects.all()
                    serializer = Organization_LocationSerializers(organization_location, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code':201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF, 'status_code':406,'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)




