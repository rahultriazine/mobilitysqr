from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.master.models import Vendor,Vendor_Category,Vendor_Master,Vendor_Income
# from mobility_apps.master.models import Vendor,Vendor_Category,Vendor_Master
from mobility_apps.master.serializers.vendor import VendorSerializers,Vendor_CategorySerializers,Vendor_MasterSerializers,Vendor_IncomeSerializers
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
from django.db import transaction,IntegrityError
from mobility_apps.master.serializers.vendor import *
from mobility_apps.master.models import *
from api.models import User

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


# class get_post_vendor(ListCreateAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = VendorSerializers

#     def get_queryset(self):
#         vendor = Vendor.objects.all()
#         return vendor

#     # Get all vendor
#     def get(self, request):
#         vendor = Vendor.objects.filter(vendor_type=request.GET['vendor_type'])
#         # paginate_queryset = self.paginate_queryset(employee)
#         # serializer = self.serializer_class(paginate_queryset, many=True)
#         serializer = VendorSerializers(vendor,many=True)
#         dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
#         return Response(dict, status=status.HTTP_200_OK)
#         #return self.get_paginated_response(serializer.data)

#     # Create a new vendor
#     def post(self, request):

#         vendorid = Vendor.objects.filter(vendor_id=request.data.get('vendor_id')).first()
#         if (vendorid):
#             # data = Vendor.object.get(~Q(vendor_id=request.data.get('vendor_id')),vendor_email__iexact=request.data['vendor_email'])
#             # if data is None:
#             #     dict = {"status": False, "message": 'This email id is already being used'}
#             #     return Response(dict, status=status.HTTP_201_CREATED)
#             # data1 = Employee.object.get(email__iexact=request.data['vendor_email'])
#             # if data1 is None:
#             #     dict = {"status": False, "message": 'This email id is already being used'}
#             #     return Response(dict, status=status.HTTP_201_CREATED)
#             serializer = VendorSerializers(vendorid, data=request.data)
#         else:
#             request.data['vendor_id']="VN"+str(uuid.uuid4().int)[:6]
#             serializer = VendorSerializers(data=request.data)
#             # data = Vendor.objects.get(vendor_email__iexact=request.data['vendor_email'])
#             # if data is None:
#             #     dict = {"status": False, "message": 'This email id is already being used'}
#             #     return Response(dict, status=status.HTTP_201_CREATED)
#             # data1 = Employee.objects.get(email__iexact=request.data['vendor_email'])
#             # if data1 is None:
#             #     dict = {"status": False, "message": 'This email id is already being used'}
#             #     return Response(dict, status=status.HTTP_201_CREATED)
#         if serializer.is_valid():
#             serializer.save()
#             request.data['user_name']=request.data['vendor_email']
#             request.data['email']=request.data['vendor_email']
#             request.data['person_id'] = "PER" + str(uuid.uuid4().int)[:6]
#             request.data['emp_code'] = "VEN" + str(uuid.uuid4().int)[:6]
#             request.data['first_name']=""
#             request.data['last_name']=""
#             request.data['role'] = "9"
#             res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
#             print(res)
#             request.data['password'] = make_password(str(res))
#             emailserializer=EmployeeSerializers(data=request.data)
#             if emailserializer.is_valid():
#                 emailserializer.save()
#                 #email= Employee.objects.filter(user_name=username).values("email")
#                 ctxt = {
#                     'user_name': request.data['user_name'],
#                     'password': request.data['password']
#                 }

#                 subject, from_email, to = 'Welcome to MobilitySQR - Vendor Registration Successful',"",request.data['user_name']
#                 html_content = render_to_string('email/vendor_registration.html', ctxt)
#                 # render with dynamic value
#                 text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
                
#                 # create the email, and attach the HTML version as well.
                
#                 msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#                 msg.attach_alternative(html_content, "text/html")
#                 msg.send()
#             else:
#                 print(emailserializer.errors)
#             dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
#             return Response(dict, status=status.HTTP_201_CREATED)
#         dict = {"status": False, "message": 'This email id is already being used in this organization'}
#         return Response(dict, status=status.HTTP_200_OK)

# class get_post_vendor(ListCreateAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = VendorSerializers

#     def get_queryset(self):
#         vendor = Vendor.objects.all()
#         return vendor

#     # Get all vendor
#     def get(self, request):
#         vendor = Vendor.objects.filter(vendor_type=request.GET['vendor_type'])
#         # paginate_queryset = self.paginate_queryset(employee)
#         # serializer = self.serializer_class(paginate_queryset, many=True)
#         serializer = VendorSerializers(vendor,many=True)
#         dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
#         return Response(dict, status=status.HTTP_200_OK)
#         #return self.get_paginated_response(serializer.data)

#     # Create a new vendor

#     def post(self, request):
#         if request.data['id']=='':
#             vendorid = Vendor.objects.filter(
#                vendor_id=request.data.get('vendor_id')).first()
#             if (vendorid):
#                 data = Vendor.objects.filter(vendor_email__iexact=request.data['vendor_email'],organization=request.data['organization'])
#                 if (data)>0:
#                     dict = {"status": False, "message": 'This email id is already being used in this organization'}
#                     return Response(dict, status=status.HTTP_200_OK)
#                 serializer = VendorSerializers(vendorid, data=request.data)
#             else:
#                 data = Vendor.objects.filter(vendor_email__iexact=request.data['vendor_email'],organization=request.data['organization'])
#                 if len(data)>0:
#                     dict = {"status": False, "message": 'This email id is already being used in this organization'}
#                     return Response(dict, status=status.HTTP_200_OK)
#                 request.data['vendor_id']="VN"+str(uuid.uuid4().int)[:6]
#                 serializer = VendorSerializers(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 request.data['user_name']=request.data['vendor_email']
#                 request.data['email']=request.data['vendor_email']
#                 request.data['person_id'] = "PER" + str(uuid.uuid4().int)[:6]
#                 request.data['emp_code'] = "VEN" + str(uuid.uuid4().int)[:6]
#                 request.data['first_name']=""
#                 request.data['last_name']=""
#                 request.data['role'] = "9"
#                 res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
#                 print(res)
#                 request.data['password'] = make_password(str(res))
#                 emailserializer=EmployeeSerializers(data=request.data)
#                 if emailserializer.is_valid():
#                     emailserializer.save()
#                     #email = Employee.objects.filter(user_name=username).values("email")
#                     ctxt = {
#                         'user_name': request.data['user_name'],
#                         'password': request.data['password']
#                     }

#                     subject, from_email, to = 'Welcome to MobilitySQR - Vendor Registration Successful',"",request.data['user_name']
#                     html_content = render_to_string('email/vendor_registration.html', ctxt)
#                     # render with dynamic value
#                     text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
                    
#                     # create the email, and attach the HTML version as well.
                    
#                     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#                     msg.attach_alternative(html_content, "text/html")
#                     msg.send()
#                 else:
#                     print(emailserializer.errors)
#                 dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
#                 return Response(dict, status=status.HTTP_201_CREATED)
#             dict={"status":False,'status_code':400,"message":MSG_FAILED,"data":serializer.errors}
#             return Response(dict, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             email=Vendor.objects.filter(vendor_email__iexact=request.data['vendor_email'],organization=request.data['organization']).last()
#             if email.id != request.data['id']:
#                 dict = {"status": False, "message": 'This email id is already being used in this organization'}
#                 return Response(dict, status=status.HTTP_200_OK)
#             else:
#                 vendorid = Vendor.objects.filter(
#                    vendor_id=request.data.get('vendor_id')).first()
#                 if (vendorid):
#                     serializer = VendorSerializers(vendorid, data=request.data)
#                 else:
#                     request.data['vendor_id']="VN"+str(uuid.uuid4().int)[:6]
#                     serializer = VendorSerializers(data=request.data)
#                 if serializer.is_valid():
#                     serializer.save()
#                     request.data['user_name']=request.data['vendor_email']
#                     request.data['email']=request.data['vendor_email']
#                     request.data['person_id'] = "PER" + str(uuid.uuid4().int)[:6]
#                     request.data['emp_code'] = "VEN" + str(uuid.uuid4().int)[:6]
#                     request.data['first_name']=""
#                     request.data['last_name']=""
#                     request.data['role'] = "9"
#                     res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
#                     print(res)
#                     request.data['password'] = make_password(str(res))
#                     emailserializer=EmployeeSerializers(data=request.data)
#                     if emailserializer.is_valid():
#                         emailserializer.save()
#                         #email = Employee.objects.filter(user_name=username).values("email")
#                         ctxt = {
#                             'user_name': request.data['user_name'],
#                             'password': request.data['password']
#                         }

#                         subject, from_email, to = 'Welcome to MobilitySQR - Vendor Registration Successful',"",request.data['user_name']
#                         html_content = render_to_string('email/vendor_registration.html', ctxt)
#                         # render with dynamic value
#                         text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
                        
#                         # create the email, and attach the HTML version as well.
                        
#                         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#                         msg.attach_alternative(html_content, "text/html")
#                         msg.send()
#                     else:
#                         print(emailserializer.errors)
#                     dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
#                     return Response(dict, status=status.HTTP_201_CREATED)
#                 dict={"status":False,'status_code':400,"message":MSG_FAILED,"data":serializer.errors}
#                 return Response(dict, status=status.HTTP_400_BAD_REQUEST)
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
        with transaction.atomic():
            vendorid = Vendor.objects.filter(vendor_id=request.data.get('vendor_id')).first()
            if (vendorid):
                serializer = VendorSerializers(vendorid, data=request.data)
            else:
                request.data['vendor_id']="VN"+str(uuid.uuid4().int)[:6]
                serializer = VendorSerializers(data=request.data)
            if serializer.is_valid():
                save_data=serializer.save()
                employee_obj = Employee.objects.filter(column1=request.data.get('vendor_id')).last()
                if employee_obj:
                    old_user_name = employee_obj.user_name
                    request.data['user_name']=request.data['vendor_email']
                    request.data['email']=request.data['vendor_email']
                    request.data['person_id'] = "PER" + str(uuid.uuid4().int)[:6]
                    request.data['emp_code'] = "VEN" + str(uuid.uuid4().int)[:6]
                    request.data['first_name']=""
                    request.data['last_name']=""
                    request.data['role'] = "9"
                    request.data['column1'] = save_data.vendor_id
                    # res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
                    # request.data['password'] = make_password(str(res))
                    emailserializer=EmployeeSerializers(employee_obj,data=request.data)
                    if emailserializer.is_valid():
                        emailserializer.save()
                        userdata = User.objects.get(username__iexact=old_user_name)
                        if userdata is not None:
                            userdata.username = request.data['vendor_email']
                            userdata.email = request.data['vendor_email']
                            userdata.save()
                        ctxt = {
                            'user_name': request.data['user_name'],
                            # 'password': request.data['password']
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
                        transaction.set_rollback(True)
                        dict = {"status": False, "message": 'Email already exist '}
                        return Response(dict, status=status.HTTP_200_OK)
                else:
                    request.data['user_name']=request.data['vendor_email']
                    request.data['email']=request.data['vendor_email']
                    request.data['person_id'] = "PER" + str(uuid.uuid4().int)[:6]
                    request.data['emp_code'] = "VEN" + str(uuid.uuid4().int)[:6]
                    request.data['first_name']=""
                    request.data['last_name']=""
                    request.data['role'] = "9"
                    request.data['column1'] = save_data.vendor_id
                    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
                    request.data['password'] = make_password(str(res))
                    emailserializer=EmployeeSerializers(data=request.data)
                    if emailserializer.is_valid():
                        emailserializer.save()
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
                        transaction.set_rollback(True)
                        dict = {"status": False, "message": 'Email already exist '}
                        return Response(dict, status=status.HTTP_200_OK)

                dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
                return Response(dict, status=status.HTTP_201_CREATED)
            else:
                transaction.set_rollback(True)
                dict = {"status": False, "message": 'Email already exist '}
                return Response(dict, status=status.HTTP_200_OK)


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
        org_id=self.request.GET.get('org_id',None)
        vendor = Vendor.objects.filter(organization=org_id).order_by('id')
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
        org_id=self.request.GET.get('org_id',None)
        vendor = Vendor_Master.objects.filter(status=True,organization=org_id).order_by('vendor_type')
        # paginate_queryset = self.paginate_queryset(employee)
        serializer = Vendor_MasterSerializers(vendor,many=True)
        dict={"status":True,'status_code':201,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)


##################################################
# post  master vendor type
##################################################

from django.db.models import Max
class get_post_master_vendors_type(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = Vendor_MasterSerializers

    def post(self,request):
        data=request.data
        a=Vendor_Master.objects.aggregate(Max('vendor_id'))
        if a['vendor_id__max']==None:
            data['vendor_id'] = 1
        else:
            data['vendor_id'] = int(a['vendor_id__max'])+1
        serializer = Vendor_MasterSerializers(data=data)
        if serializer.is_valid():
            savedata=serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)
        if savedata:
            for i in data['category_name']:
                b=Vendor_Category.objects.aggregate(Max('category_id'))
                if b['category_id__max']==None:
                    data['category_id'] = 1
                else:
                    data['category_id'] = int(b['category_id__max'])+1
                data['category_name']=i
                data['vendor_name']=data['vendor_type']
                vendor_category_serializers = Vendor_CategorySerializers(data=data)
                if vendor_category_serializers.is_valid():
                    vendor_category_serializers.save()

            dict = {'message': 'Successful', 'status': True, 'data': {"message":"success"}}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            return Response(vendor_category_serializers.errors, status=status.HTTP_200_OK)

    def get(self, request):
        org_id = request.GET.get('org_id', None)
        if org_id is None:
            data = Vendor_Master.objects.all().order_by('id')
            serializer = Vendor_MasterSerializers(data, many=True)
            dict = {"status": True, 'status_code': 200, "data": serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            data = Vendor_Master.objects.filter(organization=org_id).order_by('id')
            serializer = Vendor_MasterSerializers(data, many=True)
            dict = {"status": True, 'status_code': 200, "data": serializer.data}
            return Response(dict, status=status.HTTP_200_OK)


##################################################
# update master vendor type
##################################################

class update_master_vendors_type(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = Vendor_MasterSerializers

    def get_object(self, pk):
        return Vendor_Master.objects.get(pk=pk)

    def patch(self, request, pk):
        instance = self.get_object(pk)
        # serializer = Vendor_MasterSerializers(instance,data=request.data,partial=True)
        # if serializer.is_valid():
        #     serializer.save()
        #     dict = {'message': 'Successful', 'status': True, 'data': serializer.data}
        #     return Response(dict, status=status.HTTP_200_OK)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_200_OK)
        data=request.data
        serializer = Vendor_MasterSerializers(instance,data=data,partial=True)
        if serializer.is_valid():
            savedata=serializer.save()
        if savedata:
            abc=Vendor_Category.objects.filter(vendor_id=instance.vendor_id).delete()
            for i in data['category_name']:
                data['vendor_id'] = instance.vendor_id
                b=Vendor_Category.objects.aggregate(Max('category_id'))
                if b['category_id__max']==None:
                    data['category_id'] = 1
                else:
                    data['category_id'] = int(b['category_id__max'])+1
                data['category_name']=i
                data['vendor_name']=data['vendor_type']
                vendor_category_serializers = Vendor_CategorySerializers(data=data)
                if vendor_category_serializers.is_valid():
                    vendor_category_serializers.save()

            dict = {'message': 'Successful', 'status': True, 'data': {"message":"success"}}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)



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


class get_post_vendor_income(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Vendor_IncomeSerializers

    # Get all department
    def get(self, request):
        org_id = self.request.GET.get('org_id',None)
        vendor_income = Vendor_Income.objects.filter(organization=org_id).order_by('id')
        serializer = Vendor_IncomeSerializers(vendor_income,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = Vendor_IncomeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict = {"status": True,  "message": 'Successfully inserted', "data": serializer.data}
        else:
            dict = {"status": False, "message": 'Failed to insert data', "data": serializer.errors}
        return Response(dict, status=status.HTTP_200_OK)

class get_post_capital_gains_income(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Capital_Gains_IncomeSerializers

    # Get all department
    def get(self, request):
        org_id = self.request.GET.get('org_id',None)
        vendor_income = Capital_Gains_Income.objects.all().order_by('id')
        serializer = Capital_Gains_IncomeSerializers(vendor_income,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = Capital_Gains_IncomeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict = {"status": True,  "message": 'Successfully inserted', "data": serializer.data}
        else:
            dict = {"status": False, "message": 'Failed to insert data', "data": serializer.errors}
        return Response(dict, status=status.HTTP_200_OK)

class get_post_Vendor_Status_history(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Vendor_StatusSerializers

    # Get all department
    def get(self, request):
        org_id = self.request.GET.get('org_id',None)
        vendor_income = Vendor_Status.objects.all().order_by('id')
        serializer = Vendor_StatusSerializers(vendor_income,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = Vendor_StatusSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict = {"status": True,  "message": 'Successfully inserted', "data": serializer.data}
        else:
            dict = {"status": False, "message": 'Failed to insert data', "data": serializer.errors}
        return Response(dict, status=status.HTTP_200_OK)

class get_post_vendor_Service_List(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = vendor_Service_ListSerializers

    # Get all department
    def get(self, request):
        org_id = self.request.GET.get('org_id',None)
        vendor_income = vendor_Service_List.objects.all().order_by('id')
        serializer = vendor_Service_ListSerializers(vendor_income,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = vendor_Service_ListSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict = {"status": True,  "message": 'Successfully inserted', "data": serializer.data}
        else:
            dict = {"status": False, "message": 'Failed to insert data', "data": serializer.errors}
        return Response(dict, status=status.HTTP_200_OK)



class get_post_vendor_Service_List_status(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = vendor_Service_List_statusSerializers

    # Get all department
    def get(self, request):
        org_id = self.request.GET.get('org_id',None)
        vendor_income = vendor_Service_List_status.objects.all().order_by('id')
        serializer = vendor_Service_List_statusSerializers(vendor_income,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = vendor_Service_List_statusSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict = {"status": True,  "message": 'Successfully inserted', "data": serializer.data}
        else:
            dict = {"status": False, "message": 'Failed to insert data', "data": serializer.errors}
        return Response(dict, status=status.HTTP_200_OK)