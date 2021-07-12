from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.master.models import Assignment_Type,Create_Assignment,Secondory_Assignment,Assignment_Extension
from mobility_apps.master.serializers.assinment_type import Assignment_TypeSerializers,Create_AssignmentSerializers,Secondory_AssignmentSerializers,Assignment_ExtensionSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
import pandas as pd
import uuid
from mobility_apps.response_message import *
from django.db.models import Q, Count

class get_delete_update_assignment_type(RetrieveDestroyAPIView):
    http_method_names = ['get', 'put', 'delete', 'head', 'options', 'trace']
   # permission_classes = (IsAuthenticated,)
    serializer_class = Assignment_TypeSerializers

    def get_queryset(self, pk):
        try:
            assignment_type = Assignment_Type.objects.get(pk=self.kwargs['pk'])
        except Assignment_Type.DoesNotExist:
            content = {
                'status': MSG_NF
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return assignment_type

    # Get a assignment_type
    def get(self, request, pk):
        assignment_type = self.get_queryset(pk)
        serializer = Assignment_TypeSerializers(assignment_type)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Delete a coutry
    def delete(self, request, pk):
        assignment_type = self.get_queryset(pk)

        if (True):  # If creator is who makes request
            try:
                assignment_type.delete()
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



class get_post_assignment_type(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Assignment_TypeSerializers

    def get_queryset(self):
        assignment_type = Assignment_Type.objects.all()
        return assignment_type

    # Get all assignment_type
    def get(self, request):
        assignment_type = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Assignment_TypeSerializers(assignment_type,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new assignment
    def post(self, request):
        assignment_typeid = Assignment_Type.objects.filter(
           assignment_type_id=request.data.get('assignment_type_id')).first()
        if (assignment_typeid):
            serializer = Assignment_TypeSerializers(
                assignment_typeid, data=request.data)
        else:
            serializer = Assignment_TypeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
            return Response(dict, status=status.HTTP_201_CREATED)
        dict={"status":False,'status_code':400,"message":MSG_FAILED,"data":serializer.errors}
        return Response(dict, status=status.HTTP_400_BAD_REQUEST)


class bulk_upload_assignment_type(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Assignment_TypeSerializers

    # bulk upload api(import ASSIOGNMENT)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             assignment_type = Assignment_Type.objects.filter(
    #                assignment_type_id=value['assignment_type_id']).first()
    #             value=value.to_dict()
    #             if (assignment_type):
    #                 continue
    #             else:
    #                 serializer = Assignment_TypeSerializers(data=value)
    #             if serializer.is_valid():
    #                 serializer.save()
    #         return Response("File uploaded successfuly", status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    # bulk upload api(assignment import)
    def post(self, request):
        try:
            data = pd.read_excel(request.data.get("file"))
            sucessCount = 0
            failureCount = 0
            for i, value in data.iterrows():
                assignment_type = Assignment_Type.objects.filter(
                    assignment_type_id=value['assignment_type_id']).first()
                value = value.to_dict()
                if (assignment_type):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Assignment_TypeSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    assignment_type = Assignment_Type.objects.all()
                    serializer = Assignment_TypeSerializers(assignment_type, many=True)
                    dict = {'message':MSG_EXCELSU,'status_code':201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)



class get_create_assignment(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Create_AssignmentSerializers

    def get(self, request):
        if request.GET['home']:
            assignment_type=Create_Assignment.objects.exclude(Host_Country=request.GET['home']).filter(Q(Tentative_Assignment_Start_Date__lte=request.GET['Start_date']),Q(Tentative_Assignment_End_Date__gte=request.GET['End_date']),Employee_ID=request.GET['emp_code'])
        else:
           assignment_type=Create_Assignment.objects.filter(Ticket_ID=request.GET['Ticket_ID'],organization=request.GET['org_id'])
        serializers = Create_AssignmentSerializers(assignment_type,many=True)
        i=0
        for data in serializers.data:
            assignment_type_id=Secondory_Assignment.objects.filter(Assignment_ID=data['Assignment_ID'])
            assignment_type_serializer=Secondory_AssignmentSerializers(assignment_type_id,many=True)
            if assignment_type_serializer:
               serializers.data[i]['Secondary']=assignment_type_serializer.data
            else:
                serializers.data[i]['Secondary']=[]
            assignment_ext=Assignment_Extension.objects.filter(Assignment_ID=data['Assignment_ID'])
            assignment_ext_serializer=Assignment_ExtensionSerializers(assignment_ext,many=True)
            if assignment_type_serializer:
                serializers.data[i]['Extension']=assignment_ext_serializer.data
            else:
                serializers.data[i]['Extension']=[]
            i=i+1
        dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializers.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new assignment
    def post(self, request):
            if(request.data['Entity_Type']=='Primary'):
                assignment_typeid = Create_Assignment.objects.filter(Assignment_ID=request.data.get('Assignment_ID')).first()
                if (assignment_typeid):
                    serializer = Create_AssignmentSerializers(assignment_typeid, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
                    else:
                        dict={"status":True,'status_code':201,"message":MSG_FAILED,"data":serializer.errors}

                ####Assignment Update####
                else:
                    request.data['Assignment_ID']="ASSIGN"+str(uuid.uuid4().int)[:6]
                    serializer = Create_AssignmentSerializers(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
                    else:
                        dict={"status":True,'status_code':201,"message":MSG_FAILED,"data":serializer.errors}
                    ####Assignment Insert####
            elif(request.data['Entity_Type']=='Secondary'):
                Secondory_Assignment_ID = Secondory_Assignment.objects.filter(Secondory_Assignment_ID=request.data.get('Secondory_Assignment_ID')).first()
                if (Secondory_Assignment_ID):
                    serializer = Secondory_AssignmentSerializers(Secondory_Assignment_ID, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
                    else:
                        dict={"status":True,'status_code':201,"message":MSG_FAILED,"data":serializer.errors}
                else:
                    request.data['Secondory_Assignment_ID']="SECONASSIGN"+str(uuid.uuid4().int)[:6]
                    serializers = Secondory_AssignmentSerializers(data=request.data)
                    if serializers.is_valid():
                        serializers.save()
                        dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializers.data}
                    else:
                        dict={"status":True,'status_code':201,"message":MSG_FAILED,"data":serializers.errors}
            elif(request.data['Entity_Type']=='Extension'):
                Extension_Assignment_ID = Assignment_Extension.objects.filter(Extension_Assignment_ID=request.data.get('Extension_Assignment_ID')).first()
                if (Extension_Assignment_ID):
                    serializer = Assignment_ExtensionSerializers(Extension_Assignment_ID, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
                    else:
                        dict={"status":True,'status_code':201,"message":MSG_FAILED,"data":serializer.errors}
                else:
                    request.data['Extension_Assignment_ID']="EXSTNASSIGN"+str(uuid.uuid4().int)[:6]
                    serializers = Assignment_ExtensionSerializers(data=request.data)
                    if serializers.is_valid():
                        serializers.save()
                        dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializers.data}
                    else:
                        dict={"status":True,'status_code':201,"message":MSG_FAILED,"data":serializers.errors}
            return Response(dict, status=status.HTTP_201_CREATED)

class get_assignments(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Create_AssignmentSerializers

    def get(self, request):
        assignment_type=Create_Assignment.objects.filter(Employee_ID=request.GET['emp_code'])
        serializers = Create_AssignmentSerializers(assignment_type,many=True)
        i=0
        for data in serializers.data:
            assignment_type_id=Secondory_Assignment.objects.filter(Assignment_ID=data['Assignment_ID'])
            assignment_type_serializer=Secondory_AssignmentSerializers(assignment_type_id,many=True)
            if assignment_type_serializer:
                serializers.data[i]['Secondary']=assignment_type_serializer.data
            else:
                serializers.data[i]['Secondary']=[]
            assignment_ext=Assignment_Extension.objects.filter(Assignment_ID=data['Assignment_ID'])
            assignment_ext_serializer=Assignment_ExtensionSerializers(assignment_ext,many=True)
            if assignment_type_serializer:
                serializers.data[i]['Extension']=assignment_ext_serializer.data
            else:
                serializers.data[i]['Extension']=[]
            i=i+1
        dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializers.data}
        return Response(dict, status=status.HTTP_200_OK)

