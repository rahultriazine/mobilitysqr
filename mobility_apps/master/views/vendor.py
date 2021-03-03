from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.master.models import Vendor,Vendor_Category,Vendor_Master
from mobility_apps.master.serializers.vendor import VendorSerializers,Vendor_CategorySerializers,Vendor_MasterSerializers
from mobility_apps.employee.models import Employee
from mobility_apps.employee.serializer import EmployeeSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
import pandas as pd
import string
import random
import urllib
from contextlib import closing
from django.core.mail import EmailMultiAlternatives
#from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.hashers import make_password ,check_password
from mobility_apps.response_message import *
import uuid

class get_delete_update_vendor(RetrieveDestroyAPIView):
    http_method_names = ['get', 'put', 'delete', 'head', 'options', 'trace']
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    serializer_class = VendorSerializers

    def get_queryset(self, id):
        try:
            vendor = Vendor.objects.get(id=id)
        except Vendor.DoesNotExist:

            return []
        return vendor

    # Get a vendor
    def get(self, request):
        # import ipdb;ipdb.set_trace()
        vendor = self.get_queryset(request.GET["id"])
        if vendor:
            serializer = VendorSerializers(vendor)
            dict = {"status": True, "msg": "data found", "data": serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            dict = {'status': "False", 'msg': 'data Not Found'}
            return Response(dict, status=status.HTTP_404_NOT_FOUND)

    # Delete a vendor
    def delete(self, request):
        vendor = self.get_queryset(request.data["id"])
        if vendor:  # If creator is who makes request
            try:
                vendor.delete()
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


class get_post_vendor(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VendorSerializers

    def get_queryset(self):
        vendor = Vendor.objects.all()
        return vendor

    # Get all vendor
    def get(self, request):
        vendor = Vendor.objects.filter(vendor_type=request.GET['vendor_type'])
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = VendorSerializers(vendor,many=True)
        dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new vendor
    def post(self, request):
        vendorid = Vendor.objects.filter(
           vendor_id=request.data.get('vendor_id')).first()
        if (vendorid):
            serializer = VendorSerializers(
                vendorid, data=request.data)
        else:
            request.data['vendor_id']="VN"+str(uuid.uuid4().int)[:6]
            serializer = VendorSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            request.data['user_name']=request.data['vendor_email']
            request.data['email']=request.data['vendor_email']
            request.data['person_id'] = "PER" + str(uuid.uuid4().int)[:6]
            request.data['emp_code'] = "VEN" + str(uuid.uuid4().int)[:6]
            request.data['first_name']=""
            request.data['last_name']=""
            request.data['role'] = "9"
            res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
            print(res)
            request.data['password'] = make_password(str(res))
            emailserializer=EmployeeSerializers(data=request.data)
            if emailserializer.is_valid():
                emailserializer.save()
                #email = Employee.objects.filter(user_name=username).values("email")
                ctxt = {
                    'user_name': request.data['user_name'],
                    'password': request.data['password']
                }

                subject, from_email, to = 'Welcome to MobilitySQR - Vendor Registration Successful',"",request.data['user_name']
                html_content = render_to_string('email/vendor_registration.html', ctxt)
                # render with dynamic value
                text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
                
                # create the email, and attach the HTML version as well.
                
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            else:
                print(emailserializer.errors)
            dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
            return Response(dict, status=status.HTTP_201_CREATED)
        dict={"status":False,'status_code':400,"message":MSG_FAILED,"data":serializer.errors}
        return Response(dict, status=status.HTTP_400_BAD_REQUEST)


class bulk_upload_Vendor(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VendorSerializers

    # bulk upload api(import VENDOR)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             vendor = Vendor.objects.filter(
    #                vendor_id=value['vendor_id']).first()
    #             value=value.to_dict()
    #             if (vendor):
    #                 continue
    #             else:
    #                 serializer = VendorSerializers(data=value)
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
                vendor = Vendor.objects.filter(
                    vendor_id=value['vendor_id']).first()
                value = value.to_dict()
                if (vendor):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = VendorSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    vendor = Vendor.objects.all()
                    serializer = VendorSerializers(vendor, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code': 201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code': 406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)


class get_vendors(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VendorSerializers

    def get_queryset(self):
        vendor = Vendor.objects.all()
        return vendor

    # Get all vendor
    def get(self, request):
        vendor = Vendor.objects.all()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = VendorSerializers(vendor,many=True)
        dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)
		
		
class get_vendors_type(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Vendor_MasterSerializers
    def get(self, request):
        vendor = Vendor_Master.objects.all()
        # paginate_queryset = self.paginate_queryset(employee)
        serializer = Vendor_MasterSerializers(vendor,many=True)
        dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)






class bulk_upload_vendor_category(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Vendor_CategorySerializers

    # bulk upload api(import VENDOR)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             vendor = Vendor.objects.filter(
    #                vendor_id=value['vendor_id']).first()
    #             value=value.to_dict()
    #             if (vendor):
    #                 continue
    #             else:
    #                 serializer = VendorSerializers(data=value)
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
                vendor = Vendor_Category.objects.filter(
                    category_id=value['category_id']).first()
                value = value.to_dict()
                if (vendor):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Vendor_CategorySerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    vendor = Vendor.objects.all()
                    serializer = Vendor_CategorySerializers(vendor, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code': 201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code': 406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)


class bulk_upload_vendor_master(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Vendor_MasterSerializers

    # bulk upload api(import VENDOR)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             vendor = Vendor.objects.filter(
    #                vendor_id=value['vendor_id']).first()
    #             value=value.to_dict()
    #             if (vendor):
    #                 continue
    #             else:
    #                 serializer = VendorSerializers(data=value)
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
                vendor = Vendor_Master.objects.filter(
                    vendor_type=value['vendor_type']).first()
                value = value.to_dict()
                if (vendor):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Vendor_MasterSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    vendor = Vendor_Master.objects.all()
                    serializer = Vendor_MasterSerializers(vendor, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code': 201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code': 406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)



class get_vendors_category(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VendorSerializers

    def get_queryset(self):
        vendor = Vendor_Category.objects.all()
        return vendor

    # Get all vendor
    def post(self, request):
        #vendor = Vendor_Category.objects.filter(vendor_id=)
        vendor = Vendor_Category.objects.filter(vendor_id=request.data['vendor'])
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Vendor_CategorySerializers(vendor,many=True)
        dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)