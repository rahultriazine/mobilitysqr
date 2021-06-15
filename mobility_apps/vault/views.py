from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import FileSystemStorage
from mobility_apps.vault.models import Vault_type,Vault_type_info, Compliance, Employee_compliance
from mobility_apps.vault.serializer import Vault_type_infoSerializers,Vault_typeSerializers,ComplianceSerializers,Employee_complianceSerializers
from rest_framework.permissions import (AllowAny,IsAuthenticated)
from django.conf import settings
import os
import datetime




##########################################
#  get post vault type data
##########################################

class getPostVaultType(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Vault_typeSerializers

    def post(self,request):
        vault_id = request.data.get('vault_id', None)
        vault_type = request.data.get('vault_type', None)

        if (vault_id is None) or (vault_type is None):
            dict ={'message':'Please enter Vault id and vault type','status':False}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            serializer = Vault_typeSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                dict = {'message':'Successful','status':True,'data': serializer.data}
                return Response(dict, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self,request):
        vaultserilizer = Vault_type.objects.all()
        serializer = Vault_typeSerializers(vaultserilizer,many=True)
        dict = {'message':'Successful','status':True,'data': serializer.data}
        return Response(dict, status=status.HTTP_200_OK)




#####################################################
# vault document upload
#####################################################

class getPostVaultDocument(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Vault_type_infoSerializers


    def post(self, request,format=None  ):
        emp_code = request.data.get('emp_code', None)
        vault_type = request.data.get('vault_type', None)
        doc_name = request.data.get('doc_name', None)
        file = request.FILES
        if file:
            file = request.FILES['document_url']
        else:
            file = None
        # doc_description = request.data.get('doc_description', None)
        # document_url = request.data.get('document_url', None)
        if (emp_code is None) or (vault_type is None) or (doc_name is None) or (file is None):
            dict = {'message': 'Please enter employee code, vault type, document name and select file', 'status': False}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            file_name = str(file)
            file_type = file_name.lower()
            file_exte = file_type.endswith(('.png', '.jpg', '.jpeg', '.pdf', '.doc', '.docx'))
            if file_exte:
                fil_size = file_size(request)
                if fil_size:
                    file_url = vaultUpoadDoc(request,'/vaultDocument/')
                    request.data['document_url'] = file_url
                    # print(request.data)
                    serializer = Vault_type_infoSerializers(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        dict = {'message': 'Successful', 'status': True, 'data': serializer.data}
                        return Response(dict, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    dict = {'message': 'Exceeds the maximum file size 10MB', 'status': False}
                    return Response(dict, status=status.HTTP_200_OK)
            else:
                dict = {'message': 'Only file type (png, jpg, jpeg, pdf, doc, docx) allow', 'status': False}
                return Response(dict, status=status.HTTP_200_OK)


    " get all vault document by emp_id and type"
    def get(self, request):
        emp_code = request.GET.get('emp_code', '')
        vault_type = request.GET.get('vault_type', '')

        if (emp_code is None) or (emp_code == '') or (vault_type is None) or (vault_type == ''):
            dict = {'massage': 'Required employee code and vault type', 'status': False, 'data': []}
        else:
            vault_data = Vault_type_info.objects.filter(emp_code_id=emp_code,vault_type=vault_type)
            serializer = Vault_type_infoSerializers(vault_data, many=True)
            dict = {'massage': 'data found', 'status': True, 'data': serializer.data}

        return Response(dict, status=status.HTTP_200_OK)





#######################################
#  update and delete vault document
#######################################

class updateDeleteVaultDocument(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Vault_type_infoSerializers

    def get_object(self, pk):
        return Vault_type_info.objects.get(pk=pk)

    def patch(self, request, pk):

        file = request.FILES
        if file:
            file = request.FILES['document_url']
        else:
            file = None
        # doc_description = request.data.get('doc_description', None)
        # document_url = request.data.get('document_url', None)

        if file:
            file_name = str(file)
            file_type = file_name.lower()
            file_exte = file_type.endswith(('.png', '.jpg', '.jpeg', '.pdf', '.doc', '.docx'))
            if file_exte:
                fil_size = file_size(request)
                if fil_size:
                    file_url = vaultUpoadDoc(request,'/vaultDocument/')
                    request.data['document_url'] = file_url
                else:
                    dict = {'message': 'Exceeds the maximum file size 10MB', 'status': False}
                    return Response(dict, status=status.HTTP_200_OK)
            else:
                dict = {'message': 'Only file type (png, jpg, jpeg, pdf, doc, docx) allow', 'status': False}
                return Response(dict, status=status.HTTP_200_OK)
        instance = self.get_object(pk)
        serializer = Vault_type_infoSerializers(instance,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            dict = {'message': 'Successful', 'status': True, 'data': serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        transformer = self.get_object(pk)
        transformer.delete()
        dict = {'message': 'Deleted', 'status': True}
        return Response(dict, status=status.HTTP_200_OK)




def file_size(request):
    if request.FILES['document_url'].size <= 10000000:
        result = True
    else:
        result = False
    return result


def vaultUpoadDoc(request, foldername):
    if not os.path.exists(settings.MEDIA_ROOT + foldername):
        os.makedirs(settings.MEDIA_ROOT + foldername)
    root_location = settings.MEDIA_ROOT + foldername
    file = request.FILES['document_url']
    fs = FileSystemStorage(root_location)
    filename = fs.save(file.name, file)
    uploaded_file_url = fs.url(foldername+filename)
    return uploaded_file_url


##########################################
#  get post Compliance
##########################################

class getPostCompliance(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ComplianceSerializers

    def post(self,request):
        try:
            compl_ques = request.data.get('compl_ques', None)
            if compl_ques is None:
                dict = {'message':'Please enter compliance question','status':False}
                return Response(dict, status=status.HTTP_200_OK)
            else:
                serializer = ComplianceSerializers(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    dict = {'message': 'Successful', 'status': True, 'data': serializer.data}
                    return Response(dict, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            dict = {'status': False, 'error': str(e)}
            return Response(dict, status=status.HTTP_200_OK)

    def get(self,request):
        compserilizer = Compliance.objects.all()
        serializer = ComplianceSerializers(compserilizer, many=True)
        dict = {'message': 'Successful', 'status': True, 'data': serializer.data}
        return Response(dict, status=status.HTTP_200_OK)




##########################################
#  get post Compliance by employee
##########################################

class getPostComplianceAnswer(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Employee_complianceSerializers

    def post(self,request):
        try:
            emp_code = request.data[0]['emp_code']
            check = self.permission_check(emp_code)
            if check is False:
                dict = {'status': False, 'message': 'Already answered, you are eligible to answer in next month.'}
                return Response(dict, status=status.HTTP_200_OK)
            alldata = []
            for data in request.data:
                serializer = Employee_complianceSerializers(data=data)
                if serializer.is_valid():
                    serializer.save()
                    alldata.append(serializer.data)
                else:
                    alldata.append(serializer.errors)
                dict = {'message': 'successfully registered your response.', 'status': True, 'data': alldata}
            return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            dict = {'status': False, 'error': str(e)}
            return Response(dict, status=status.HTTP_200_OK)


    def get(self,request):
        try:
            emp_code = request.GET.get('emp_code', None)
            if emp_code is None:
                dict = {'message': 'Please enter employee code ', 'status': False}
                return Response(dict, status=status.HTTP_200_OK)
            else:
                compserilizer = Employee_compliance.objects.filter(emp_code=emp_code).order_by('date_created')[:5]
                serializer = Employee_complianceSerializers(compserilizer, many=True)
                if serializer.data:
                    dict = {'message': 'Successful', 'status': True, 'data': serializer.data}
                else:
                    compserilizer = Compliance.objects.all()
                    serializer = ComplianceSerializers(compserilizer, many=True)
                    dict = {'message': 'Successful', 'status': True, 'data': serializer.data}
                return Response(dict, status=status.HTTP_200_OK)

        except Exception as e:
            dict = {'status': False, 'error': str(e)}
            return Response(dict, status=status.HTTP_200_OK)


    def permission_check(self,emp_code):
        data = Employee_compliance.objects.filter(emp_code=emp_code).last()
        if data:
            date_time = str(data.date_created)
            date = date_time.split(' ')
            atee = datetime.datetime.strptime(date[0], "%Y-%m-%d")
            todays_date = datetime.date.today()
            if atee.month == todays_date.month:
                return False
            else:
                return True
        else:
            return True