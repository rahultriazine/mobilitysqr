from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.master.models import Gender,Marital_Status,Salutation,Acedmic_Title,Name_Suffix,Email_Type,Phone_Type,Relation,Termination_Reasons,Address_Type,Language
from mobility_apps.master.serializers.dropdown import GenderSerializers,Marital_StatusSerializers,SalutationSerializers,Acedmic_TitleSerializers,Name_SuffixSerializers,Email_TypeSerializers,Phone_TypeSerializers,RelationSerializers,Termination_ReasonsSerializers,Address_TypeSerializers,LanguageSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
import pandas as pd
from mobility_apps.response_message import *

class get_post_gender(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = GenderSerializers

    def get_queryset(self):
        gender = Gender.objects.all()
        return gender

    # Get all department
    def get(self, request):
        gender = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = GenderSerializers(gender,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

class bulk_upload_Gender(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GenderSerializers

    # bulk upload api(import DEPARTMENT)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             department = Department.objects.filter(
    #                department_id=value['department_id']).first()
    #             value=value.to_dict()
    #             if (department):
    #                 continue
    #             else:
    #                 serializer = DepartmentSerializers(data=value)
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
                gender = Gender.objects.filter(
                    code=value['code']).first()
                value = value.to_dict()
                if (gender):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = GenderSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    gender = Gender.objects.all()
                    serializer = GenderSerializers(gender, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code':201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)



class get_post_marital_status(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Marital_StatusSerializers

    def get_queryset(self):
        marital_status = Marital_Status.objects.all()
        return marital_status

    # Get all department
    def get(self, request):
        marital_status = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Marital_StatusSerializers(marital_status,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

class bulk_upload_marital_status(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Marital_StatusSerializers

    # bulk upload api(import DEPARTMENT)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             department = Department.objects.filter(
    #                department_id=value['department_id']).first()
    #             value=value.to_dict()
    #             if (department):
    #                 continue
    #             else:
    #                 serializer = DepartmentSerializers(data=value)
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
                marital_status = Marital_Status.objects.filter(
                    code=value['code']).first()
                value = value.to_dict()
                if (marital_status):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Marital_StatusSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    marital_status = Marital_Status.objects.all()
                    serializer = Marital_StatusSerializers(marital_status, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code':201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)


class get_post_salutation(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = SalutationSerializers

    def get_queryset(self):
        salutation = Salutation.objects.all()
        return salutation

    # Get all department
    def get(self, request):
        salutation = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = SalutationSerializers(salutation,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

class bulk_upload_salutation(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SalutationSerializers

    # bulk upload api(import DEPARTMENT)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             department = Department.objects.filter(
    #                department_id=value['department_id']).first()
    #             value=value.to_dict()
    #             if (department):
    #                 continue
    #             else:
    #                 serializer = DepartmentSerializers(data=value)
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
                salutation = Salutation.objects.filter(
                    code=value['code']).first()
                value = value.to_dict()
                if (salutation):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = SalutationSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    salutation = Salutation.objects.all()
                    serializer = SalutationSerializers(salutation, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code':201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)



class get_post_acedmic(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Acedmic_TitleSerializers

    def get_queryset(self):
        acedmic = Acedmic_Title.objects.all()
        return acedmic

    # Get all department
    def get(self, request):
        acedmic = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Acedmic_TitleSerializers(acedmic,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

class bulk_upload_acedmic(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Acedmic_TitleSerializers

    # bulk upload api(import DEPARTMENT)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             department = Department.objects.filter(
    #                department_id=value['department_id']).first()
    #             value=value.to_dict()
    #             if (department):
    #                 continue
    #             else:
    #                 serializer = DepartmentSerializers(data=value)
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
                acedmic = Acedmic_Title.objects.filter(
                    code=value['code']).first()
                value = value.to_dict()
                if (acedmic):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Acedmic_TitleSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    acedmic = Acedmic_Title.objects.all()
                    serializer = Acedmic_TitleSerializers(acedmic, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code':201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)


class get_post_suffix(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Name_SuffixSerializers

    def get_queryset(self):
        suffix = Name_Suffix.objects.all()
        return suffix

    # Get all department
    def get(self, request):
        suffix = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Name_SuffixSerializers(suffix,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

class bulk_upload_suffix(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Name_SuffixSerializers

    # bulk upload api(import DEPARTMENT)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             department = Department.objects.filter(
    #                department_id=value['department_id']).first()
    #             value=value.to_dict()
    #             if (department):
    #                 continue
    #             else:
    #                 serializer = DepartmentSerializers(data=value)
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
                suffix = Name_Suffix.objects.filter(
                    code=value['code']).first()
                value = value.to_dict()
                if (suffix):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Name_SuffixSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    suffix = Name_Suffix.objects.all()
                    serializer = Name_SuffixSerializers(suffix, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code':201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)


class get_post_email(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Email_TypeSerializers

    def get_queryset(self):
        email = Email_Type.objects.all()
        return email

    # Get all department
    def get(self, request):
        email = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Email_TypeSerializers(email,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

class bulk_upload_email(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Email_TypeSerializers

    # bulk upload api(import DEPARTMENT)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             department = Department.objects.filter(
    #                department_id=value['department_id']).first()
    #             value=value.to_dict()
    #             if (department):
    #                 continue
    #             else:
    #                 serializer = DepartmentSerializers(data=value)
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
                email = Email_Type.objects.filter(
                    code=value['code']).first()
                value = value.to_dict()
                if (email):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Email_TypeSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    email = Email_Type.objects.all()
                    serializer = Email_TypeSerializers(email, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code':201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)


class get_post_phone(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Phone_TypeSerializers

    def get_queryset(self):
        phone = Phone_Type.objects.all()
        return phone

    # Get all department
    def get(self, request):
        phone = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Phone_TypeSerializers(phone,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

class bulk_upload_phone(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Phone_TypeSerializers

    # bulk upload api(import DEPARTMENT)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             department = Department.objects.filter(
    #                department_id=value['department_id']).first()
    #             value=value.to_dict()
    #             if (department):
    #                 continue
    #             else:
    #                 serializer = DepartmentSerializers(data=value)
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
                phone = Phone_Type.objects.filter(
                    code=value['code']).first()
                value = value.to_dict()
                if (phone):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Phone_TypeSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    phone = Phone_Type.objects.all()
                    serializer = Phone_TypeSerializers(phone, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code':201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)



class get_post_relation(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = RelationSerializers

    def get_queryset(self):
        relation = Relation.objects.all()
        return relation

    # Get all department
    def get(self, request):
        relation = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = RelationSerializers(relation,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

class bulk_upload_relation(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RelationSerializers

    # bulk upload api(import DEPARTMENT)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             department = Department.objects.filter(
    #                department_id=value['department_id']).first()
    #             value=value.to_dict()
    #             if (department):
    #                 continue
    #             else:
    #                 serializer = DepartmentSerializers(data=value)
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
                relation = Relation.objects.filter(
                    code=value['code']).first()
                value = value.to_dict()
                if (relation):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = RelationSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    relation = Relation.objects.all()
                    serializer = RelationSerializers(relation, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code':201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)



class get_post_termination(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Termination_ReasonsSerializers

    def get_queryset(self):
        termination = Termination_Reasons.objects.all()
        return termination

    # Get all department
    def get(self, request):
        termination = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Termination_ReasonsSerializers(termination,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

class bulk_upload_termination(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Termination_ReasonsSerializers

    # bulk upload api(import DEPARTMENT)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             department = Department.objects.filter(
    #                department_id=value['department_id']).first()
    #             value=value.to_dict()
    #             if (department):
    #                 continue
    #             else:
    #                 serializer = DepartmentSerializers(data=value)
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
                termination = Termination_Reasons.objects.filter(
                    code=value['code']).first()
                value = value.to_dict()
                if (termination):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Termination_ReasonsSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    termination = Termination_Reasons.objects.all()
                    serializer = Termination_ReasonsSerializers(termination, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code':201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)



class get_post_address(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Address_TypeSerializers

    def get_queryset(self):
        address = Address_Type.objects.all()
        return address

    # Get all department
    def get(self, request):
        address = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Address_TypeSerializers(address,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

class bulk_upload_address(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Address_TypeSerializers

    # bulk upload api(import DEPARTMENT)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             department = Department.objects.filter(
    #                department_id=value['department_id']).first()
    #             value=value.to_dict()
    #             if (department):
    #                 continue
    #             else:
    #                 serializer = DepartmentSerializers(data=value)
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
                address = Address_Type.objects.filter(
                    code=value['code']).first()
                value = value.to_dict()
                if (address):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Address_TypeSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    address = Address_Type.objects.all()
                    serializer = Address_TypeSerializers(address, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code':201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)



class get_post_language(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = LanguageSerializers

    def get_queryset(self):
        language = Language.objects.all()
        return language

    # Get all department
    def get(self, request):
        language = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = LanguageSerializers(language,many=True)
        dict={"status":True,'status_code':200,"message":MSG_SUCESS,"data":serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

class bulk_upload_language(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LanguageSerializers

    # bulk upload api(import DEPARTMENT)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             department = Department.objects.filter(
    #                department_id=value['department_id']).first()
    #             value=value.to_dict()
    #             if (department):
    #                 continue
    #             else:
    #                 serializer = DepartmentSerializers(data=value)
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
                language = Language.objects.filter(
                    code=value['code']).first()
                value = value.to_dict()
                if (language):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = LanguageSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    language = Language.objects.all()
                    serializer = LanguageSerializers(language, many=True)
                    dict = {'message': MSG_EXCELSU,'status_code':201, 'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)
