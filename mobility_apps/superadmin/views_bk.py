from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.superadmin.models import Organizations,Organization_branches,Organization_users
from mobility_apps.superadmin.serializers import UserinfoSerializers,OrganizationsSerializers,Organization_branchesSerializers,Organization_usersSerializers
from mobility_apps.employee.models import Userinfo
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
#import pandas as pd
import uuid
from datetime import datetime
from mobility_apps.response_message import *
from collections import Counter
from django.db.models import Q

class SaveOrganization(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrganizationsSerializers
    def post(self,request):
        try:
            editId  = request.GET.get("id", 0)
            msg =""
            if int(editId) > 0:
                sac = Organizations.objects.filter(id=editId).first()
                if sac ==None:
                    msg = "Organization Not Found"
                    dict = {'massage': msg, 'status': False, 'data':[]}
                    return Response(dict, status=status.HTTP_404_NOT_FOUND)
                org_serializer = OrganizationsSerializers(sac, data=request.data)
                msg ="Organization updated Successfully"
            else:
                request.data['org_id'] = "ORG" + str(uuid.uuid4().int)[:6]
                org_serializer = OrganizationsSerializers(data=request.data)
                msg = "Organization added Successfully"

            if org_serializer.is_valid():
                org_serializer.save()
                PKlastOrgId = org_serializer.data['id']
                #print(PKlastOrgId)
                #Branches = request.data['branches']
                #self.add_branches(Branches,PKlastOrgId)
                dict = {'massage': msg, 'status': True, 'data': org_serializer.data}
                return Response(dict, status=status.HTTP_201_CREATED)
            else:
                dict = {'massage': org_serializer.errors, 'status': False, 'data': []}
                return Response(dict, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            dict = {"success": False, "error":str(e)}
            return Response(dict)



    def get(self,request):
         try:
             id = request.GET.get("id", 0)
             if(int(id)>0):
                 orgdata = Organizations.objects.filter(id=id)
                 orgdata2 = Organizations.objects.filter(id=id).count()
             else:
                 orgdata = Organizations.objects.all().order_by('-id')
                 orgdata2 = Organizations.objects.count()


             #print(orgdata2)
             org_serializer = OrganizationsSerializers(orgdata,many=True)
             if orgdata2:
                 dict = {'massage': 'data found', 'status': True, 'data': org_serializer.data}
                 return Response(dict, status=status.HTTP_200_OK)
             else:
                 dict = {'massage': 'data not found', 'status': False,'data':[]}
                 return Response(dict, status=status.HTTP_404_NOT_FOUND)
         except Exception as e:
             dict = {"success": False, "error":str(e)}
             return Response(dict)



class Branch(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Organization_branchesSerializers
    def post(self,request):
        try:
            editId  = request.GET.get("branch_id", 0)
            msg =""
            if int(editId) > 0:
                sac = Organization_branches.objects.filter(id=editId).first()
                if sac ==None:
                    msg = "branch Not Found"
                    dict = {'massage': msg, 'status': False, 'data':[]}
                    return Response(dict, status=status.HTTP_404_NOT_FOUND)
                branch_serializer = Organization_branchesSerializers(sac, data=request.data)
                msg ="Branch updated Successfully"
            else:
                #request.data['status'] = 1
                branch_serializer = Organization_branchesSerializers(data=request.data)
                msg = "New Branch added Successfully"

            if branch_serializer.is_valid():
                branch_serializer.save()
                dict = {'massage': msg, 'status': True, 'data': branch_serializer.data}
                return Response(dict, status=status.HTTP_201_CREATED)
            else:
                dict = {'massage': branch_serializer.errors, 'status': False, 'data': []}
                return Response(dict, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            dict = {"success": False, "error":str(e)}
            return Response(dict)

    def get(self,request):
         try:
             org_id_id = request.GET.get("org_id", 0)
             branch_id = request.GET.get("branch_id", 0)
             #print(branch_id)
             if(int(branch_id)>0):
                 orgdata = Organization_branches.objects.filter(org_id_id=org_id_id).filter(id=branch_id)
                 orgdata2 = Organization_branches.objects.filter(org_id_id=org_id_id).filter(id=branch_id).count()
             else:
                 orgdata = Organization_branches.objects.filter(org_id_id=org_id_id).order_by('-id')
                 orgdata2 = Organization_branches.objects.filter(org_id_id=org_id_id).count()

             #print(orgdata2)
             org_serializer = Organization_branchesSerializers(orgdata,many=True)
             if orgdata2:
                 dict = {'massage': 'data found', 'status': True, 'data': org_serializer.data}
                 return Response(dict, status=status.HTTP_200_OK)
             else:
                 dict = {'massage': 'data not found', 'status': False,'data':[]}
                 return Response(dict, status=status.HTTP_404_NOT_FOUND)
         except Exception as e:
             dict = {"success": False, "error":str(e)}
             return Response(dict)


class get_org_count(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        orgdata2 = Organizations.objects.count()
        # org_serializer = OrganizationsSerializers(orgdata, many=True)
        dict = {'massage': 'data found', 'status': True, 'data': orgdata2}
        return Response(dict, status=status.HTTP_200_OK)




class OrgUsers(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserinfoSerializers
    def post(self,request):
        try:
            editId  = request.GET.get("user_id", 0)
            msg =""
            if int(editId) > 0:
                sac = Userinfo.objects.filter(id=editId).first()
                #print(sac.password)
                if sac ==None:
                    msg = "Not Found"
                    dict = {'massage': msg, 'status': False, 'data':[]}
                    return Response(dict, status=status.HTTP_404_NOT_FOUND)
                request.data['person_id'] = sac.person_id
                request.data['password'] = sac.password
                user_serializer = UserinfoSerializers(sac, data=request.data)
                #print(user_serializer)
                msg ="User updated Successfully"
            else:
                #request.data['status'] = 1
                request.data['role'] = 7
                request.data['person_id'] = "PER" + str(uuid.uuid4().int)[:6]
                request.data['password'] = str(uuid.uuid4().int)[:6]
                #print(request.data)
                user_serializer = UserinfoSerializers(data=request.data)
                msg = "New User added Successfully"
            if user_serializer.is_valid():
                user_serializer.save()
                if int(editId) == 0:
                    self.sendmails(msg,request.data['email'],request.data['password'])

                dict = {'massage': msg, 'status': True, 'data': user_serializer.data}
                return Response(dict, status=status.HTTP_201_CREATED)
            else:
                dict = {'massage': user_serializer.errors, 'status': False, 'data': []}
                return Response(dict, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            dict = {"success": False, "error":str(e)}
            return Response(dict)

    def sendmails(self,msg,email,password):
        username=email
        #"rahulr@triazinesoft.com"
        password = password
        #"123456"
        subject = 'New Admin user added'
        message = ''
        html_message = '<h3>New Admin user details below</h3>'
        html_message += '<p> User Name <b>: '+username+'</b> </p>'
        html_message += '<p>User Name : <b>' +password+ '</b> </p>'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email,]
        send_mail(subject, message, email_from, recipient_list, fail_silently=False, html_message=html_message)


    def get(self,request):
         try:
             user_id = request.GET.get("user_id", 0)
             #print(user_id)
             #orgdata = Userinfo.objects.filter(status=1).filter(id=user_id)
             if (int(user_id) > 0):
                 orgdata = Userinfo.objects.filter(id=user_id)
                 orgdata2 = Userinfo.objects.filter(id=user_id)
             else:
                 orgdata = Userinfo.objects.all().order_by('-id')
                 orgdata2 = Userinfo.objects.count()

             org_serializer = UserinfoSerializers(orgdata,many=True)
             if orgdata2:
                 dict = {'massage': 'data found', 'status': True, 'data': org_serializer.data}
                 return Response(dict, status=status.HTTP_200_OK)
             else:
                 dict = {'massage': 'data not found', 'status': False,'data':[]}
                 return Response(dict, status=status.HTTP_404_NOT_FOUND)


         except Exception as e:
             dict = {"success": False, "error":str(e)}
             return Response(dict)




