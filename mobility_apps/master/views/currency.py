from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.master.models import Currency ,Currency_Conversion,Currency_Conversion_History,Per_Diem
from mobility_apps.master.serializers.currency import CurrencySerializers ,Currency_ConversionSerializers,Currency_Conversion_HistorySerializers,Per_DiemSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
import pandas as pd
from mobility_apps.response_message import *
from django.db.models import Q
import datetime

from django.db.models import Max

class get_delete_update_currency(RetrieveDestroyAPIView):
    http_method_names = ['get', 'put', 'delete', 'head', 'options', 'trace']
    permission_classes = (IsAuthenticated,)
    serializer_class = CurrencySerializers

    def get_queryset(self, pk):
        try:
            currency = Currency.objects.get(pk=self.kwargs['pk'])
        except Currency.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return currency

    # Get a currency
    def get(self, request, pk):
        currency = self.get_queryset(pk)
        serializer = CurrencySerializers(currency)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Delete a coutry
    def delete(self, request, pk):
        currency = self.get_queryset(pk)

        if (True):  # If creator is who makes request
            try:
                currency.delete()
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



class get_post_currency(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CurrencySerializers

    def get_queryset(self):
        currency = Currency.objects.all().order_by('id')
        return currency

    # Get all currency
    # def get(self, request):
    #     currency = self.get_queryset()
    #     # paginate_queryset = self.paginate_queryset(employee)
    #     # serializer = self.serializer_class(paginate_queryset, many=True)''
    #     # org_id = self.request.GET.get('org_id',None)
    #     # currency = Currency.objects.filter(Q(organization=org_id) | Q(organization='null')).order_by('id')
    #     serializer = CurrencySerializers(currency,many=True)
    #     dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':serializer.data}
    #     return Response(dict, status=status.HTTP_200_OK)
    #     #return self.get_paginated_response(serializer.data)
    def get(self, request):
        org_id = self.request.GET.get('org_id',None)
        if org_id:
            currency = Currency.objects.filter(organization__isnull=True).order_by('id')
            serializer = CurrencySerializers(currency,many=True)
            currency_org = Currency.objects.filter(organization=org_id).order_by('id')
            serializer_org = CurrencySerializers(currency_org,many=True)
            null_org=serializer.data
            org_data = serializer_org.data
            for i in org_data:
                null_org.append(i)
            dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':null_org}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            currency = Currency.objects.filter(organization__isnull=True).order_by('id')
            serializer = CurrencySerializers(currency,many=True)
            dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':serializer.data}
            return Response(dict, status=status.HTTP_200_OK)


    # Create a new currency
    def post(self, request):
        currencyid = Currency.objects.filter(currency_code=request.data.get('currency_code')).first()
        if currencyid:
            data=request.data
            data.pop('organization')
            serializer = CurrencySerializers(currencyid, data=data)
        else:
            serializer = CurrencySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict={"status":True,'Status_code':201,"message":MSG_SUCESS,"data":serializer.data}
            return Response(dict, status=status.HTTP_201_CREATED)
        dict={"status":False,'Status_code':200,"message":MSG_SUCESS,"data":serializer.errors}
        return Response(dict, status=status.HTTP_200_OK)




class get_post_per_diem(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Per_DiemSerializers

    # Get all currency
    def get(self, request):
        band = request.GET.get('band', None)
        organization = request.GET.get('organization', None)
        home_country = request.GET.get('home_country', None)
        if organization is None:
            dict = {'message': "Organization id is required", 'status': False}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            if band is None and home_country is None:
                currency = Per_Diem.objects.filter(organization=organization).order_by('id')
                serializer = Per_DiemSerializers(currency, many=True)
                dict = {'message': MSG_SUCESS, 'status': True, 'data':serializer.data}
                return Response(dict, status=status.HTTP_200_OK)
            elif band is not None and home_country is None:
                currency = Per_Diem.objects.filter(organization=organization,band=band).order_by('id')
                serializer = Per_DiemSerializers(currency, many=True)
                dict = {'message': MSG_SUCESS, 'status': True, 'data': serializer.data}
                return Response(dict, status=status.HTTP_200_OK)
            elif band is None and home_country is not None:
                currency = Per_Diem.objects.filter(organization=organization,home_country=home_country).order_by('id')
                serializer = Per_DiemSerializers(currency, many=True)
                dict = {'message': MSG_SUCESS, 'status': True, 'data': serializer.data}
                return Response(dict, status=status.HTTP_200_OK)
            else:
                currency = Per_Diem.objects.filter(organization=organization, home_country=home_country,band=band).order_by('id')
                serializer = Per_DiemSerializers(currency, many=True)
                dict = {'message': MSG_SUCESS, 'status': True, 'data': serializer.data}
                return Response(dict, status=status.HTTP_200_OK)


    # Create a new currency
    def post(self, request):
        perdiem =Per_Diem.objects.filter(id=request.data['id']).first()
        if perdiem:
            serializer = Per_DiemSerializers(perdiem, data=request.data)
        else:
            serializer = Per_DiemSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            dict={"status":True,'Status_code':201,"message":MSG_SUCESS,"data":serializer.data}
            return Response(dict, status=status.HTTP_201_CREATED)
        dict={"status":False,'Status_code':200,"message":MSG_SUCESS,"data":serializer.errors}
        return Response(dict, status=status.HTTP_200_OK)




class bulk_upload_currency(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CurrencySerializers

    # bulk upload api(import Currency)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             currency = Currency.objects.filter(
    #                currency_id=value['currency_id']).first()
    #             value=value.to_dict()
    #             if (currency):
    #                 continue
    #             else:
    #                 serializer = CurrencySerializers(data=value)
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
            print(data)
            for i, value in data.iterrows():
                currency = Currency.objects.filter(
                    currency_code=value['currency_code']).first()
                value = value.to_dict()
                if (currency):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = CurrencySerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    currency = Currency.objects.all()
                    serializer = CurrencySerializers(currency, many=True)
                    dict = {'message': MSG_EXCELSU, 'status_code':201,'status': 'True', 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': 'False'}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)


class bulk_upload_currency_conversion(ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = Currency_ConversionSerializers

    # bulk upload api(import Currency)
    # def post(self, request):
    #     try:
    #         data=pd.read_excel(request.data.get("file"))
    #         for i, value in data.iterrows():
    #             currency = Currency.objects.filter(
    #                currency_id=value['currency_id']).first()
    #             value=value.to_dict()
    #             if (currency):
    #                 continue
    #             else:
    #                 serializer = CurrencySerializers(data=value)
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
                value = value.to_dict()
                if (failureCount):
                    failureCount += 1
                    continue
                else:
                    sucessCount += 1
                    serializer = Currency_ConversionSerializers(data=value)
                if serializer.is_valid():
                    serializer.save()
                    currency = Currency_Conversion.objects.all()
                    serializer = Currency_ConversionSerializers(currency, many=True)
                    dict = {'message': MSG_EXCELSU, 'status_code':201,'status': True, 'record pass': sucessCount,
                            'record fail': failureCount}
                    responseList = [dict]
            return Response(responseList, status=status.HTTP_201_CREATED)
        except Exception as e:
            dict = {'message': MSG_EXCELF,'status_code':406, 'status': False}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)
			
			
class get_active_currency(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CurrencySerializers

    def get_queryset(self,status_type):
        if status_type=="Active":
            currency = Currency.objects.filter(status_type=status_type)
            return currency
        else:
            currency = Currency.objects.all()
            return currency

    # Get all currency
    def get(self, request):
        # currency = self.get_queryset(request.GET['status_type'])
        # # paginate_queryset = self.paginate_queryset(employee)
        # # serializer = self.serializer_class(paginate_queryset, many=True)
        # serializer = CurrencySerializers(currency,many=True)
        # dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':serializer.data}
        # return Response(dict, status=status.HTTP_200_OK)
        # #return self.get_paginated_response(serializer.data)

        #============ajay code============
        status_type = request.GET.get('status_type', None)
        org_id = self.request.GET.get('org_id',None)
        filter_query = Q()
        if status_type is not None and status_type !='':
            filter_query.add(Q(status_type=status_type), Q.AND)
        if org_id:
            currency = Currency.objects.filter(organization__isnull=True).filter(filter_query)
            currency_org = Currency.objects.filter(organization=org_id).filter(filter_query)
            records = (currency | currency_org)
            serializer_org = CurrencySerializers(records,many=True)
            dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':serializer_org.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            currency = Currency.objects.all()
            serializer = CurrencySerializers(currency,many=True)
            dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':serializer.data}
            return Response(dict, status=status.HTTP_200_OK)

class get_currency_conversion(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = Currency_ConversionSerializers

    def get_queryset(self,from_currency,to_currency):
        currency = Currency_Conversion.objects.filter(from_currency=from_currency,to_currency=to_currency).order_by('-conversion_date')
        return currency

    # Get all currency
    # def get(self, request):
    #     currency = self.get_queryset(request.GET['from_currency'],request.GET['to_currency'])
    #     # paginate_queryset = self.paginate_queryset(employee)
    #     # serializer = self.serializer_class(paginate_queryset, many=True)
    #     serializer = Currency_ConversionSerializers(currency,many=True)
    #     dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':serializer.data}
    #     return Response(dict, status=status.HTTP_200_OK)
    #     #return self.get_paginated_response(serializer.data)

    def get(self, request):
        from_currency = request.GET.get('from_currency', None)
        to_currency = request.GET.get('to_currency', None)
        org_id = self.request.GET.get('org_id',None)
        filter_query = Q()
        if from_currency is not None and from_currency !='':
            filter_query.add(Q(from_currency=from_currency), Q.AND)
        if to_currency is not None and to_currency !='':
            filter_query.add(Q(to_currency__iexact=to_currency), Q.AND)
        if org_id:
            currency = Currency_Conversion.objects.filter(organization__isnull=True).filter(filter_query)
            # serializer = Currency_ConversionSerializers(currency,many=True)

            currency_org = Currency_Conversion.objects.filter(organization=org_id).filter(filter_query)
            # serializer_org = Currency_ConversionSerializers(currency_org,many=True)
            records = (currency | currency_org).order_by('-conversion_date')
            serializer_org = Currency_ConversionSerializers(records,many=True)
            # null_org=serializer.data
            # org_data = serializer_org.data
            # for i in org_data:
            #     null_org.append(i)
            dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':serializer_org.data}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            currency = Currency_Conversion.objects.filter(filter_query)
            serializer = Currency_ConversionSerializers(currency,many=True)
            dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':serializer.data}
            return Response(dict, status=status.HTTP_200_OK)


class post_currency_conversion(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Currency_ConversionSerializers
    # post all currency
    # def get(self, request):
    #     currency = Currency_Conversion.objects.all().order_by('id')
    #     # paginate_queryset = self.paginate_queryset(employee)
    #     # serializer = self.serializer_class(paginate_queryset, many=True)
    #     serializer = Currency_ConversionSerializers(currency,many=True)
    #     dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':serializer.data}
    #     return Response(dict, status=status.HTTP_200_OK)
    def get(self, request):
        org_id = self.request.GET.get('org_id',None)
        if org_id:
            currency = Currency_Conversion.objects.filter(organization__isnull=True).order_by('id')
            serializer = Currency_ConversionSerializers(currency,many=True)
            currency_org = Currency_Conversion.objects.filter(organization=org_id).order_by('id')
            serializer_org = Currency_ConversionSerializers(currency_org,many=True)
            null_org=serializer.data
            org_data = serializer_org.data
            for i in org_data:
                null_org.append(i)
            dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':null_org}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            currency = Currency_Conversion.objects.filter(organization__isnull=True).order_by('id')
            serializer = Currency_ConversionSerializers(currency,many=True)
            dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
    def post(self, request):
        editId  = request.data.get("id", 0)
        if editId:
           currency=Currency_Conversion.objects.filter(id=editId).first()
           serializer = Currency_ConversionSerializers(currency,data=request.data)
           if serializer.is_valid():
              id=serializer.save().id
              historyserializer = Currency_Conversion_HistorySerializers(data=request.data)
              if historyserializer.is_valid():
                 historyserializer.save()
              dict = {'message': MSG_UPDATE, 'status_code':200,'status': True,'data':id}  
           else:
              dict = {'message': MSG_FAILED, 'status_code':200,'status': True,'data':serializer.errors}
        else:
            currencyafirst=Currency_Conversion.objects.filter(from_currency=request.data['from_currency'],to_currency=request.data['to_currency']).first()
            if currencyafirst:
                currencyavail=Currency_Conversion.objects.filter(from_currency=request.data['from_currency'],to_currency=request.data['to_currency'],conversion_date__gte=request.data['conversion_date']).first()
                if currencyavail:
                    serializer = Currency_ConversionSerializers(currencyavail,data=request.data)
                    if serializer.is_valid():
                        id=serializer.save().id
                        historyserializer = Currency_Conversion_HistorySerializers(data=request.data)
                        if historyserializer.is_valid():
                            historyserializer.save()
                            dict = {'message': MSG_UPDATE, 'status_code':200,'status': True,'data':id}  
                    else:
                        dict = {'message':MSG_FAILED, 'status_code':200,'status': True,'data':serializer.errors}
                else:
                    serializer = Currency_ConversionSerializers(currencyavail,data=request.data)
                    if serializer.is_valid():
                        id=serializer.save().id
                        historyserializer = Currency_Conversion_HistorySerializers(data=request.data)
                        if historyserializer.is_valid():
                            historyserializer.save()
                            dict = {'message': MSG_UPDATE, 'status_code':200,'status': True,'data':id}  
                    else:
                        dict = {'message':MSG_FAILED, 'status_code':200,'status': True,'data':serializer.errors}   
            else:
                serializer = Currency_ConversionSerializers(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    historyserializer = Currency_Conversion_HistorySerializers(data=request.data)
                    if historyserializer.is_valid():
                        historyserializer.save()
                    dict = {'message': MSG_ADDED, 'status_code':200,'status': True,'data':serializer.data}  
                else:
                    dict = {'message':MSG_FAILED, 'status_code':200,'status': True,'data':serializer.errors}     
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)
    

class currency_conversion_history(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Currency_Conversion_HistorySerializers
    def get(self, request):
        from_currency = request.GET.get('from_currency', None)
        to_currency = request.GET.get('to_currency', None)
        from_date = request.GET.get('from_date', None)
        to_date = request.GET.get('to_date', None)
        org_id = self.request.GET.get('org_id',None)
        filter_query = Q()
        if from_currency is not None and from_currency !='':
            filter_query.add(Q(from_currency=from_currency), Q.AND)
        if to_currency is not None and to_currency !='':
            filter_query.add(Q(to_currency__iexact=to_currency), Q.AND)
        if from_date is not None and from_date !='':
            filter_query.add(Q(conversion_date__gte=from_date), Q.AND)
        if to_date is not None and to_date !='':
            to_date = to_date+" "+"23:59:00"
            filter_query.add(Q(conversion_date__lte=to_date), Q.AND)
        if org_id:
            currency = Currency_Conversion_History.objects.filter(organization__isnull=True).filter(filter_query)
            serializer = Currency_Conversion_HistorySerializers(currency,many=True)

            currency_org = Currency_Conversion_History.objects.filter(organization=org_id).filter(filter_query)
            serializer_org = Currency_Conversion_HistorySerializers(currency_org,many=True)
            null_org=serializer.data
            org_data = serializer_org.data
            for i in org_data:
                null_org.append(i)
            dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':null_org}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            currency = Currency_Conversion_History.objects.filter(filter_query)
            serializer = Currency_Conversion_HistorySerializers(currency,many=True)
            dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':serializer.data}
            return Response(dict, status=status.HTTP_200_OK)
class currency_conversion_history_new(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Currency_Conversion_HistorySerializers
    def get(self, request):
        from_currency = request.GET.get('from_currency', None)
        to_currency = request.GET.get('to_currency', None)
        from_date = request.GET.get('from_date', None)
        to_date = request.GET.get('to_date', None)
        org_id = self.request.GET.get('org_id',None)
        filter_query = Q()
        if from_currency is not None and from_currency !='':
            filter_query.add(Q(from_currency=from_currency), Q.AND)
        if to_currency is not None and to_currency !='':
            filter_query.add(Q(to_currency__iexact=to_currency), Q.AND)
        if from_date is not None and from_date !='':
            filter_query.add(Q(conversion_date__gte=from_date), Q.AND)
        if to_date is not None and to_date !='':
            to_date = to_date+" "+"23:59:00"
            filter_query.add(Q(conversion_date__lte=to_date), Q.AND)
        if org_id:
            currency = Currency_Conversion.objects.filter(organization__isnull=True).filter(filter_query)
            serializer = Currency_ConversionSerializers(currency,many=True)

            currency_org = Currency_Conversion.objects.filter(organization=org_id).filter(filter_query)
            serializer_org = Currency_ConversionSerializers(currency_org,many=True)
            null_org=serializer.data
            org_data = serializer_org.data
            for i in org_data:
                null_org.append(i)
            dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':null_org}
            return Response(dict, status=status.HTTP_200_OK)
        else:
            currency = Currency_Conversion.objects.filter(filter_query)
            serializer = Currency_ConversionSerializers(currency,many=True)
            dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':serializer.data}
            return Response(dict, status=status.HTTP_200_OK)



########################################################
" bulk json upload currency"
########################################################

class json_upload_currency(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CurrencySerializers

    def post(self, request, *args, **kwargs):
        try:
            serializer = CurrencySerializers(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            dict = {'message': e, 'status': False, 'status_code': 406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)


################################################################
" bulk upload json data for currency conversion"
################################################################

class json_upload_currency_conversion(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Currency_ConversionSerializers

    def post(self, request, *args, **kwargs):
        try:
            serializer = Currency_ConversionSerializers(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            dict = {'message': e, 'status': False, 'status_code': 406}
            return Response(dict, status=status.HTTP_406_NOT_ACCEPTABLE)