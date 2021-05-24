from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.master.models import Project
from mobility_apps.master.serializers.project import ProjectSerializers
from mobility_apps.employee.models import Employee
from mobility_apps.employee.serializer import EmployeeSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
import pandas as pd
from mobility_apps.response_message import *
from datetime import date
import json
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pagination import CustomPagination
class get_delete_update_project(RetrieveDestroyAPIView):
    http_method_names = ['get', 'put', 'delete', 'head', 'options', 'trace']
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializers

    def get_queryset(self, pk):
        try:
            project = Project.objects.get(pk=self.kwargs['pk'])
        except Project.DoesNotExist:
            content = {
                'status': MSG_NF
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return project

    # Get a project
    def get(self, request, pk):
        project = self.get_queryset(pk)
        serializer = ProjectSerializers(Project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Delete a PROJECT
    def delete(self, request, pk):
        project = self.get_queryset(pk)

        if (True):  # If creator is who makes request
            try:
                project.delete()
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



class get_post_project(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializers

    def get_queryset(self):
        project = Project.objects.all()
        return project

    # Get all project
    def get(self, request):
        project = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = ProjectSerializers(project,many=True)
        dict={"status":True,'status_code':200,"message":"New project added Successfully","data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new project
    def post(self, request):
        projectpid = Project.objects.filter(
           pid=request.data.get('pid')).first()
        if projectpid:
           dict={"status":True,'status_code':201,"message":"Project ID is already exists"}
            #serializer = ProjectSerializers(
             #   projectpid, data=request.data)
        else:
            serializer = ProjectSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
            else:
                dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.errors}
        return Response(dict, status=status.HTTP_201_CREATED)


class get_update_project(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializers
    # Create a new project
    def post(self, request):
        projectpid = Project.objects.filter(id=request.data['uid']).first()
        print(projectpid)
        if projectpid:
            serializer = ProjectSerializers(projectpid, data=request.data)
            if serializer.is_valid():
                serializer.save()
                dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
            else:
                dict={"status":False, 'status_code':201,"message":MSG_FAILED,"data":serializer.errors}
        else:
            dict={"status":False,'status_code':201,"message":MSG_FAILED,"data":"Project ID is not in database"}
        return Response(dict, status=status.HTTP_200_OK)



class bulk_upload_project(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializers

    # bulk upload api(import PROJECT)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             project = Project.objects.filter(
    #                pid=value['pid']).first()
    #             value=value.to_dict()
    #             if (project):
    #                 continue
    #             else:
    #                 serializer = ProjectSerializers(data=value)
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
                project = Project.objects.filter(
                    pid=value['pid']).first()
                value = value.to_dict()
                #print(value)
                if (project):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = ProjectSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    project = Project.objects.all()
                    serializer = ProjectSerializers(project, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code':201,'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
                else:
                    print(serializer.errors)
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)

class get_project_list(ListCreateAPIView):
    serializer_class = ProjectSerializers
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        # import ipdb;ipdb.set_trace()
        t = date.today()
        print(t)
        pid = request.GET["pid"]
        pids=request.GET["limit"]
        org_id=request.GET["org_id"]
        project = Project.objects.filter(Q(pid__icontains=pid)|Q(project_name__icontains=pid),End_Date__gte=t,organization_id=org_id,)[:15] 
        #project = Project.objects.raw("select top 15 * from master_project where pid LIKE '%"+str(pid)+"%' or project_name LIKE '%"+str(pid)+"%' AND organization_id ='"+org_id+"'")

        serializer = ProjectSerializers(project,many=True)
        dicts=[]
        for projects in serializer.data:
            pid=projects['pid']
            projects=Project.objects.filter(pid=pid)
            serializers = ProjectSerializers(projects,many=True)
            dicts.append(serializers.data[0])
        if dicts:
           dict = {"status": True, "message":MSG_SUCESS, "data": dicts}
           return Response(dict, status=status.HTTP_200_OK)
        else:
           dict = {"status": True, "message":MSG_SUCESS, "data": dicts}
           return Response(dict, status=status.HTTP_200_OK)


class get_project_list_user(ListCreateAPIView):
    serializer_class = ProjectSerializers

    def get_queryset(self, request):
        print(request)
        try:
            project =  Project.objects.filter(Q(business_lead=request) | Q(client_executive_lead=request)|Q(expense_approver=request)|Q(project_manager=request))
        # print(visa)
        except Project.DoesNotExist:

            return []
        return project
    # Get all country:
    def get(self, request):
        project = self.get_queryset(request.GET['role'])
        if project:
            serializer = ProjectSerializers(project,many=True)
            dict = {"status": True, "Message":MSG_SUCESS, "data": serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'status': "False", 'Message':MSG_FAILED}
            return Response(dict, status=status.HTTP_200_OK)



class get_projects(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializers
    
    pagination_class = CustomPagination
    def get(self, request):
        if request.GET['search']:
           queryset = Project.objects.filter(Q(pid__icontains=request.GET['search'])|Q(project_name__icontains=request.GET['search']),organization=request.GET['org'])
           #print(queryset)
        else:
           queryset = Project.objects.filter(organization=request.GET['org']) 
        if queryset:
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                i=0
                for data in serializer.data:
                    serializer.data[i]['client_executive_name']=self.employee_name(emp_code=data['client_executive_lead'])
                    serializer.data[i]['business_lead_name'] = self.employee_name(emp_code=data['business_lead'])
                    serializer.data[i]['expense_approver_name'] = self.employee_name(emp_code=data['expense_approver'])
                    serializer.data[i]['project_manager_name'] = self.employee_name(emp_code=data['project_manager'])
                    i=i+1
                result = self.get_paginated_response(serializer.data)
                data = result.data # pagination data
            else:
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data
            payload = {
                'return_code': '0000',
                'return_message': 'Success',
                'data': data
            }
            dict = {"status": True, "Message":MSG_SUCESS, "data":data}
        
        else:
            dict = {'status': "False", 'Message':MSG_FAILED}
        return Response(dict, status=status.HTTP_200_OK)
    def employee_name(self,emp_code):
        if emp_code:
            emp_code=Employee.objects.filter(emp_code=emp_code).values('emp_code','preferred_first_name','first_name','last_name')
            if emp_code[0]['first_name']:
                first_name=emp_code[0]['first_name']
            else:
                first_name=''

            if emp_code[0]['last_name']:
                last_name=emp_code[0]['last_name']
            else:
                last_name=""
            name=first_name+" "+last_name
            return name

##################################################
" bulk upload json project"
##################################################

class json_upload_project(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializers

    def post(self, request, *args, **kwargs):
        try:
            serializer = ProjectSerializers(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            dict = {'message': e, 'status': False, 'status_code': 406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)

