from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.employee.models import Employee, Employee_Passport_Detail, Employee_Visa_Detail,Employee_Address,Employee_Emails,Employee_Phones,Employee_Nationalid,Employee_Emergency_Contact,Userinfo
from mobility_apps.employee.serializer import EmployeeSerializers,Employee_Passport_DetailSerializers, Employee_Visa_DetailSerializers,Employee_AddressSerializers,Employee_EmailsSerializers,Employee_PhonesSerializers,Employee_NationalidSerializers,Employee_Emergency_ContactSerializers,UserinfoSerializers
from mobility_apps.travel.models import Travel_Request ,Travel_Request_Details,Travel_Request_Dependent,Travel_Request_Draft ,Travel_Request_Details_Draft,Travel_Request_Dependent_Draft,Assignment_Travel_Tax_Grid
from mobility_apps.travel.serializers import Travel_RequestSerializers ,Travel_Request_DetailsSerializers,Travel_Request_DependentSerializers,Travel_Request_DraftSerializers ,Travel_Request_Details_DraftSerializers,Travel_Request_Dependent_DraftSerializers,Assignment_Travel_Tax_GridSerializers
from mobility_apps.visa.models import Visa_Request

from mobility_apps.master.models import Country,City,Per_Diem,Dial_Code,Country_Master,State_Master,Location_Master,Taxgrid_Master,Taxgrid_Country,Taxgrid
from mobility_apps.master.serializers.country import CountrySerializers ,CitySerializers,Per_DiemSerializers,Dial_CodeSerializers,Country_MasterSerializers,State_MasterSerializers,Location_MasterSerializers,Taxgrid_MasterSerializers,Taxgrid_CountrySerializers,TaxgridSerializers
from mobility_apps.visa.serializers import Visa_RequestSerializers
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from mobility_apps.master.models import Country_Master
from mobility_apps.master.serializers.country import Country_MasterSerializers
from django.db.models.deletion import ProtectedError
from io import BytesIO
from django.template.loader import get_template
#from xhtml2pdf import pisa
from django.core.mail.message import EmailMessage
from django.conf import settings
#import pandas as pd
import uuid
import datetime
from datetime import datetime
from mobility_apps.response_message import *
from collections import Counter
from django.db.models import Q
from django.db import connection
from django.db.models import F
from django.db.models import Count
from collections import defaultdict
class visa_category_reports(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Travel_Request_DetailsSerializers
    # Get all visa_purpose
    def get(self, request):
        visa= Visa_Request.objects.all()
        #travels= Travel_Request.objects.filter(travel_req_status="2",current_ticket_owner="").count()

        try:
            if visa:
                #serializer =Travel_RequestSerializers(travels,many=True)
                serializer =Visa_RequestSerializers(visa,many=True)
               
                dict=[]
                for data in serializer.data:
                    dict.append(data['applied_visa'])
                total=sum(Counter(dict).values())
        
                my_dict = Counter(dict)
                visatype=Visa_Request.objects.values("id","visa_req_id","travel_req_id","req_id","emp_email","project_id","project_name","is_billable","is_dependent","vendor_fees","govt_fees","country","dependent_name","dependent_relation","from_city","to_city","organization","travel_start_date", "travel_end_date","visa_purpose","applied_visa","remark","request_notes","visa_status","visa_status_notes","current_ticket_owner","supervisor","expense_approver","project_manager","business_lead","client_executive_lead","approval_level")
                #print(visatype)
                datas=[]
                
                for visa in visatype:
                    data={}
                    data['Vsa Request ID']=visa['visa_req_id']
                    data['Travel Request ID']=visa['travel_req_id']
                    data['Employee Email']=visa['emp_email']
                    data['Project ID']=visa['project_id']
                    data['Project Name']=visa['project_name']
                    data['Is Billable']=visa['is_billable']
                    data['Is Dependent']=visa['is_dependent']
                    data['Vendor Fees']=visa['vendor_fees']
                    data['Govt Fees']=visa['govt_fees']
                    #data['Country']=visa['country']
                    data['Dependent Name']=visa['dependent_name']
                    data['Dependent Relation']=visa['dependent_relation']
                    data['From Country']=visa['from_city']
                    data['To Country']=visa['to_city']
                    data['Organization']=visa['organization']
                    data['Travel Start Date']=visa['travel_start_date']
                    data['Travel End Date']=visa['travel_end_date']
                    data['Visa Purpose']=visa['visa_purpose']
                    data['Applied Visa']=visa['applied_visa']
                    data['Remark']=visa['remark']
                    data['Request Notes']=visa['request_notes']
                    data['Visa Status']=visa['visa_status']
                    data['Visa Status Notes']=visa['visa_status_notes']
                    data['Current Ticket Owner']=visa['current_ticket_owner']
                    data['Supervisor']=visa['supervisor']
                    data['ExpenseApprover']=visa['expense_approver']
                    data['Project Manager']=visa['project_manager']
                    data['Business Lead']=visa['business_lead']
                    data['Client Executive Lead']=visa['client_executive_lead']
                    datas.append(data)
                dicts = {"status": True, "message":MSG_SUCESS, "data":my_dict,"details":datas}
                return Response(dicts, status=status.HTTP_200_OK)
            else:
                dict = {"status": "False","status_code":200, "message":MSG_FAILED}
                return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            dict = {'massage code': '200', 'massage': MSG_FAILED}
            return Response(dict, status=status.HTTP_200_OK)



class travel_country_reports(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Travel_Request_DetailsSerializers
    # Get all visa_purpose
    def get(self, request):
        travel= Travel_Request_Details.objects.all()
        #travels= Travel_Request.objects.filter(travel_req_status="2",current_ticket_owner="").count()

        try:
            if travel:
                #serializer =Travel_RequestSerializers(travels,many=True)
                serializer =Travel_Request_DetailsSerializers(travel,many=True)
                #print(serializer.data)
                dict=[]
                for data in serializer.data:
                    dict.append(data['travelling_country_to'])
                total=sum(Counter(dict).values())
                #print(dict.keys)
                my_dict = Counter(dict)
                traveltype=Travel_Request_Details.objects.all() 
                traveltypes=Travel_Request_DetailsSerializers(traveltype,many=True)
                #traveltype=Travel_Request.objects.values('travel_req_id','emp_email','project','project_name','is_billable','is_travel_multi_country','is_travel_multi_city','request_notes','remark','home_contact_name','home_phone_ext','home_phone_number','is_laptop_required','travel_req_status','travel_req_status_notes','current_ticket_owner','organization','supervisor','expense_approver','project_manager','business_lead','client_executive_lead','have_laptop')
                print(traveltypes.data)
                datas=[]
               
                for travel in traveltypes.data:
                    data={}
                    data['Travel Request ID']=travel['travel_req_id']
                    data['Travelling Country']=travel['travelling_country']
                    data['Travelling Country To']=travel['travelling_country_to']
                    data['Office Location']=travel['office_location']
                    data['Client Number Extension']=travel['client_number_ext']
                    data['Client Number']=travel['client_number']
                    data['Organization']=travel['organization']
                    data['Source City']=travel['source_city']
                    data['Destination City']=travel['destination_city']
                    data['Departure Date']=travel['departure_date']
                    data['Return Date']=travel['return_date']
                    data['Is Accmodation Required']=travel['is_accmodation_required']
                    data['Accmodation Start Date']=travel['accmodation_start_date']
                    data['Accmodation End Date']=travel['accmodation_end_date']
                    data['Travel Purpose']=travel['travel_purpose']
                    data['Assignment Date']=travel['assignment_type']
                    data['Applicable Visa']=travel['applicable_visa']
                    data['Visa Number']=travel['visa_number']
                    data['Visa Expiry Date']=travel['visa_expiry_date']
                    data['Host HR Name']=travel['host_hr_name']
                    data['Host Country Head']=travel['host_country_head']
                    data['Host Attorney']=travel['host_attorney']
                    data['Host Phone Extension']=travel['host_phone_ext']
                    data['Host Phone Nuber']=travel['host_phone_no']
                    data['Is Client Location']=travel['is_client_location']
                    data['Client Name']=travel['client_name']
                    data['Client Address']=travel['client_address']
                    data['Hotel Cost']=travel['hotel_cost']
                    data['Per Diem Cost']=travel['per_diem_cost']
                    data['Airfare Cost']=travel['airfare_cost']
                    data['transportation Cost']=travel['transportation_cost']
                    data['Total Cost']=travel['total_cost']
                    data['Currency']=travel['currency']
                    data['Reporting Currency']=travel['reporting_currency']
                    data['Travel Request Status']=travel['travel_request_status']
                    data['Travel Request Statuss Notes']=travel['travel_request_status_notes']
                    data['Is Dependent']=travel['is_dependent']
                    datas.append(data)
                print(datas)
                dicts = {"status": True, "message":MSG_SUCESS, "data":my_dict,"details":datas}
                return Response(dicts, status=status.HTTP_200_OK)
            else:
                dict = {"status": "False","status_code":200, "message":MSG_FAILED}
                return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            dict = {'massage code': '200', 'massage': MSG_FAILED, 'status': 'False'}
            return Response(dict, status=status.HTTP_200_OK)



class visa_country_reports(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class =Visa_RequestSerializers
    # Get all visa_purpose
    def get(self, request):
        travel= Visa_Request.objects.all()
        #travels= Travel_Request.objects.filter(travel_req_status="2",current_ticket_owner="").count()

        try:
            if travel:
                #serializer =Travel_RequestSerializers(travels,many=True)
                serializer =Visa_RequestSerializers(travel,many=True)
                #print(serializer.data)
                dict=[]
                for data in serializer.data:
                    #print(data['country'])
                    country=Country_Master.objects.filter(country_id=data['country']).values("name")
                    for country in country:
                    #country=Country_MasterSerializers()
                        dict.append(country['name'])
                total=sum(Counter(dict).values())
                my_dict = Counter(dict)
                visatype=Visa_Request.objects.values("id","visa_req_id","travel_req_id","req_id","emp_email","project_id","project_name","is_billable","is_dependent","vendor_fees","govt_fees","country","dependent_name","dependent_relation","from_city","to_city","organization","travel_start_date", "travel_end_date","visa_purpose","applied_visa","remark","request_notes","visa_status","visa_status_notes","current_ticket_owner","supervisor","expense_approver","project_manager","business_lead","client_executive_lead","approval_level")
                #print(visatype)
                datas=[]
                
                for visa in visatype:
                    data={}
                    data['Vsa Request ID']=visa['visa_req_id']
                    data['Travel Request ID']=visa['travel_req_id']
                    data['Employee Email']=visa['emp_email']
                    data['Project ID']=visa['project_id']
                    data['Project Name']=visa['project_name']
                    data['Is Billable']=visa['is_billable']
                    data['Is Dependent']=visa['is_dependent']
                    data['Vendor Fees']=visa['vendor_fees']
                    data['Govt Fees']=visa['govt_fees']
                    #data['Country']=visa['country']
                    data['Dependent Name']=visa['dependent_name']
                    data['Dependent Relation']=visa['dependent_relation']
                    data['From Country']=visa['from_city']
                    data['To Country']=visa['to_city']
                    data['Organization']=visa['organization']
                    data['Travel Start Date']=visa['travel_start_date']
                    data['Travel End Date']=visa['travel_end_date']
                    data['Visa Purpose']=visa['visa_purpose']
                    data['Applied Visa']=visa['applied_visa']
                    data['Remark']=visa['remark']
                    data['Request Notes']=visa['request_notes']
                    data['Visa Status']=visa['visa_status']
                    data['Visa Status Notes']=visa['visa_status_notes']
                    data['Current Ticket Owner']=visa['current_ticket_owner']
                    data['Supervisor']=visa['supervisor']
                    data['ExpenseApprover']=visa['expense_approver']
                    data['Project Manager']=visa['project_manager']
                    data['Business Lead']=visa['business_lead']
                    data['Client Executive Lead']=visa['client_executive_lead']
                    datas.append(data)
                dicts = {"status": True, "message":MSG_SUCESS, "data":my_dict,"details":datas}
                return Response(dicts, status=status.HTTP_200_OK)
            else:
                dict = {"status": "False","status_code":200, "message":MSG_FAILED}
                return Response(dict, status=status.HTTP_200_OK)
        except Exception as e:
            dict = {'massage code': '200', 'massage': MSG_FAILED, 'status': 'False'}
            return Response(dict, status=status.HTTP_200_OK)


class assignment_travel_tax_grid_reports(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = Assignment_Travel_Tax_GridSerializers
    def get(self, request):
        travel_requests=Assignment_Travel_Tax_Grid.objects.filter(travel_req_id=request.GET["travel_req_id"]).values('tax_label_id','annual_ammount','currency','report_currency','report_currency_ammount','frequency')
        datas=[]
        print(travel_requests)
        i=0
        for visa in travel_requests:
            data={}
            if Taxgrid.objects.filter(id=visa['tax_label_id']).exists():
                taxgrid=Taxgrid.objects.filter(id=visa['tax_label_id'])
                taxgrids=TaxgridSerializers(taxgrid,many=True)
                if taxgrids.data[0]['tax_label'] is None:
                    data['Tax Label']=""
                else:
                    data['Tax Label']=taxgrids.data[0]['tax_label']

            else:
                data['Tax Label']=""
            #data['Tax Label']=visa['tax_label_id']
            
            if visa['annual_ammount'] is None:
                data['Amount']=""
            else:
                data['Amount']=visa['annual_ammount']
            data['Currency']=visa['currency']
            data['Reporting Currency']=visa['report_currency']
            data['Reporting Currency Ammount']=visa['report_currency_ammount']
            data['Frequency']=visa['frequency']
            datas.append(data)
            i=i+1
        #travel_request_dependent=Assignment_Travel_Tax_GridSerializers(travel_requests,many=True)
        dict = {'massage': 'data found', 'status': True, 'data': datas}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)
    # Create a new employee

class all_assignment_travel_tax_grid_reports(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = Assignment_Travel_Tax_GridSerializers
    def get(self, request):
        travel_requests=Assignment_Travel_Tax_Grid.objects.values('travel_req_id').distinct()
        data=[]
        for tavelrequest in travel_requests:
            datas={}
            travels=tavelrequest['travel_req_id']
            datas[travels]={}
            travel_requests=Assignment_Travel_Tax_Grid.objects.filter(travel_req_id=tavelrequest['travel_req_id']).values('travel_req_id','tax_label_id','annual_ammount','currency','report_currency','report_currency_ammount','frequency')
            dsay=[]
            for travelsss in travel_requests:
               datats={}
               if Taxgrid.objects.filter(id=travelsss['tax_label_id']).exists():
                    taxgrid=Taxgrid.objects.filter(id=travelsss['tax_label_id'])
                    taxgrids=TaxgridSerializers(taxgrid,many=True)
                    if taxgrids.data[0]['tax_label'] is None:
                        datats[taxgrids.data[0]['tax_label']]=""
                    else:
                        datats[taxgrids.data[0]['tax_label']]=travelsss['annual_ammount']
               else:
                    datats['None']=""
               datats['currency']=travelsss['currency']
               datats['report_currency']=travelsss['report_currency']
               datats['report_currency_ammount']=travelsss['report_currency_ammount']
               datats['frequency']=travelsss['frequency']
               dsay.append(datats)
               datas[travels].update({"travel_data":dsay})
            #if travel_requests[0]['travel_req_id']
            #datas[travels].update({"annual_ammount":travel_requests[0]['annual_ammount']})
                
            data.append(datas)         
            # travel_requests=Assignment_Travel_Tax_Grid.objects.values('travel_req_id','tax_label_id','annual_ammount')
            #travel_requestss=Assignment_Travel_Tax_Grid.objects.values(Assignment_Travel_Tax_Grid.objects.values('travel_req_id','tax_label_id','amount').annotate(total=Count('travel_req_id'),))
            # print(travel_requests)
            # datas=[]
            # i=0
            # for visa in travel_requests:
                
            #     if Taxgrid_Master.objects.filter(id=visa['tax_label_id']).exists():
            #         taxgrid=Taxgrid_Master.objects.filter(id=visa['tax_label_id'])
            #         taxgrids=Taxgrid_MasterSerializers(taxgrid,many=True)
            #         if taxgrids.data[0]['tax_label'] is None:
            #             data['Tax Label']=""
            #         else:
            #             data['Tax Label']=taxgrids.data[0]['tax_label']

            #     else:
            #         data['Tax Label']=""
            #     data['Travel Request ID']=visa['travel_req_id']
            #     data['Amount']=visa['annual_ammount']
            #     # data['Currency']=visa['currency']
            #     # data['Report Currency']=visa['report_currency']
            #     # data['Frequency']=visa['frequency']
            #     datas.append(data)
        #travel_request_dependent=Assignment_Travel_Tax_GridSerializers(travel_requests,many=True)
        dict = {'massage': 'data found', 'status': True, 'data': data}
        # responseList = [dict]
        return Response(dict, status=status.HTTP_200_OK)
   
    # Create a new employee