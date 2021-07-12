from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.master.models import Role
from mobility_apps.master.serializers.role import RoleSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
import pandas as pd
from mobility_apps.response_message import *

class get_delete_update_role(RetrieveDestroyAPIView):
    http_method_names = ['get', 'put', 'delete', 'head', 'options', 'trace']
    permission_classes = (IsAuthenticated,)
    serializer_class = RoleSerializers

    def get_queryset(self, pk):
        try:
            role = Role.objects.get(pk=self.kwargs['pk'])
        except Role.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return role

    # Get a role
    def get(self, request, pk):
        role = self.get_queryset(pk)
        serializer = RoleSerializers(role)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Delete a coutry
    def delete(self, request, pk):
        role = self.get_queryset(pk)

        if (True):  # If creator is who makes request
            try:
                role.delete()
            except ProtectedError:
                content = {
                    'message': MSG_RTOAR,
                }
                return Response(content, status=status.HTTP_423_LOCKED)
            content = {
                'message': MSG_NOC,
            }
            return Response(content, status=status.HTTP_204_NO_CONTENT)
        else:
            content = {
                'message': MSG_UN

            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)



class get_post_role(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RoleSerializers

    def get_queryset(self):
        role = Role.objects.all()
        return role

    # Get all role
    def get(self, request):
        role = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = RoleSerializers(role,many=True)
        dict = {'message': MSG_SUCESS, 'status_code':200,'status': 'False','data':serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new role
    def post(self, request):
        roleid = Role.objects.filter(
           role_id=request.data.get('role_id')).first()
        if (roleid):
            serializer = RoleSerializers(
                roleid, data=request.data)
        else:
            serializer = RoleSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict={"status":True,'Status_code':201,"message":MSG_SUCESS,"data":serializer.data}
            return Response(dict, status=status.HTTP_201_CREATED)
        dict={"status":False,'Status_code':400,"message":MSG_SUCESS,"data":serializer.errors}
        return Response(dict, status=status.HTTP_400_BAD_REQUEST)


class bulk_upload_role(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RoleSerializers

    # bulk upload api(import ROLE)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             role = Role.objects.filter(
    #                role_id=value['role_id']).first()
    #             value=value.to_dict()
    #             if (role):
    #                 continue
    #             else:
    #                 serializer = RoleSerializers(data=value)
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
                role = Role.objects.filter(
                    role_id=value['role_id']).first()
                value = value.to_dict()
                if (role):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = RoleSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    role = Role.objects.all()
                    serializer = RoleSerializers(Role, many=True)
                    dict = {'message': MSG_EXCELSU, 'status_code':201,'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)


#####################################################################
"json bulk upload role"
#####################################################################

class json_upload_role(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RoleSerializers

    def post(self, request, *args, **kwargs):
        try:
            serializer = RoleSerializers(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            dict = {'message': e, 'status': False, 'status_code': 406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)




