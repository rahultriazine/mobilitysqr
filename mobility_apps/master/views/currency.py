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
        currency = Currency.objects.all()
        return currency

    # Get all currency
    def get(self, request):
        currency = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = CurrencySerializers(currency,many=True)
        dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

    # Create a new currency
    def post(self, request):
        currencyid = Currency.objects.filter(
            currency_code=request.data.get('currency_code')).first()
        if (currencyid):
            serializer = CurrencySerializers(
                currencyid, data=request.data)
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

    def get_queryset(self):
        currency = Per_Diem.objects.all()
        return currency

    # Get all currency
    def get(self, request):
        currency = self.get_queryset()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Per_DiemSerializers(currency,many=True)
        dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

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
        currency = self.get_queryset(request.GET['status_type'])
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = CurrencySerializers(currency,many=True)
        dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)

class get_currency_conversion(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Currency_ConversionSerializers

    def get_queryset(self,from_currency,to_currency):
        currency = Currency_Conversion.objects.filter(from_currency=from_currency,to_currency=to_currency)
        return currency

    # Get all currency
    def get(self, request):
        currency = self.get_queryset(request.GET['from_currency'],request.GET['to_currency'])
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Currency_ConversionSerializers(currency,many=True)
        dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':serializer.data}
        return Response(dict, status=status.HTTP_200_OK)
        #return self.get_paginated_response(serializer.data)


class post_currency_conversion(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Currency_ConversionSerializers
    # post all currency
    def get(self, request):
        currency = Currency_Conversion.objects.all()
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
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
    # post all currency
    def get(self, request):
        currency = Currency_Conversion_History.objects.filter(from_currency=request.GET['from_currency'],to_currency=request.GET['to_currency'],conversion_date__gte=request.GET['from_date'],conversion_date__lte=request.GET['to_date'])
        # paginate_queryset = self.paginate_queryset(employee)
        # serializer = self.serializer_class(paginate_queryset, many=True)
        serializer = Currency_Conversion_HistorySerializers(currency,many=True)
        print(serializer.data)
        dict = {'message': MSG_SUCESS, 'status_code':200,'status': True,'data':serializer.data}
        return Response(dict, status=status.HTTP_200_OK)