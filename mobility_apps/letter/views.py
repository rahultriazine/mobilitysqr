from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mobility_apps.employee.models import Employee, Employee_Passport_Detail, Employee_Visa_Detail,Employee_Address,Employee_Emails,Employee_Phones,Employee_Nationalid,Employee_Emergency_Contact,Userinfo
from mobility_apps.employee.serializer import EmployeeSerializers,Employee_Passport_DetailSerializers, Employee_Visa_DetailSerializers,Employee_AddressSerializers,Employee_EmailsSerializers,Employee_PhonesSerializers,Employee_NationalidSerializers,Employee_Emergency_ContactSerializers,UserinfoSerializers
from mobility_apps.travel.models import Travel_Request ,Travel_Request_Details,Travel_Request_Dependent,Travel_Request_Draft ,Travel_Request_Details_Draft,Travel_Request_Dependent_Draft,Assignment_Travel_Tax_Grid
from mobility_apps.travel.serializers import Travel_RequestSerializers ,Travel_Request_DetailsSerializers,Travel_Request_DependentSerializers,Travel_Request_DraftSerializers ,Travel_Request_Details_DraftSerializers,Travel_Request_Dependent_DraftSerializers,Assignment_Travel_Tax_GridSerializers
from mobility_apps.employee.models import Employee, Employee_Passport_Detail, Employee_Visa_Detail,Employee_Address,Employee_Emails,Employee_Phones,Employee_Nationalid,Employee_Emergency_Contact,Userinfo
from mobility_apps.letter.models import Letters
from mobility_apps.letter.serializer import LettersSerializers
from mobility_apps.visa.models import Visa_Request , Visa_Request_Document,Visa_Request_Draft
from mobility_apps.visa.serializers import Visa_RequestSerializers,Visa_Request_DocumentSerializers,Visa_Request_DraftSerializers
from mobility_apps.master.models import Country,City,Per_Diem,Dial_Code,Country_Master,State_Master,Location_Master,Taxgrid_Master,Taxgrid_Country,Taxgrid,National_Id
from mobility_apps.master.models import Assignment_Type,Create_Assignment,Secondory_Assignment,Assignment_Extension
from mobility_apps.master.serializers.assinment_type import Assignment_TypeSerializers,Create_AssignmentSerializers,Secondory_AssignmentSerializers,Assignment_ExtensionSerializers

from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import  (AllowAny,IsAuthenticated)
from django.db.models.deletion import ProtectedError
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail.message import EmailMessage
from django.conf import settings
#import pandas as pd
import uuid
import datetime
from datetime import datetime,date,timezone
from mobility_apps.response_message import *
from collections import Counter
from django.db.models import Q
import os
import json
from zipfile import ZipFile
from django.utils.html import strip_tags
from dateutil import tz
class getassignmentletter(APIView):
    
   def get(self,request, *args, **kwargs):
      travel_status=Travel_Request.objects.filter(travel_req_id =request.GET['travel_req_id'],travel_req_status="3")
      print('#################')
      print(travel_status)
      letter=[]
      if travel_status.exists(): 
         id=request.GET['travel_req_id']
         travel_statuss=Travel_Request_Details.objects.filter(travel_req_id =request.GET['travel_req_id']).values("travel_req_id","travel_purpose")
         
         i=0
         for travel_statu in travel_statuss:
            #print(travel_statu['travel_purpose'])
            if travel_statu['travel_purpose']=="Work":
                  id=travel_statu['travel_req_id']
                  travel_request= Create_Assignment.objects.filter(Ticket_ID=id)
                  #print(travel_request)
                  
                  if travel_request.exists():
                     travel_request_serializer = Create_AssignmentSerializers(travel_request,many=True)
                  else:
                     travel_request= Secondory_Assignment.objects.filter(Ticket_ID=id)
                     #print(travel_request)
                     travel_request_serializer = Secondory_AssignmentSerializers(travel_request,many=True)
                  

                  emp_code=travel_request_serializer.data[0]['Employee_ID']
                  #print(travel_request_serializer.data[0]['Employee_ID'])
                  emp = Employee.objects.filter(emp_code=emp_code)
                  
                  emp_serializer = EmployeeSerializers(emp,many=True)
                  travel_request_serializer.data[0]['emp_info']=emp_serializer.data

                  empcode=emp_serializer.data[0]['emp_code']
                  empadd = Employee_Address.objects.filter(emp_code=empcode,address_type="host")
                  empadd_serializer = Employee_AddressSerializers(empadd,many=True)
                  travel_request_serializer.data[0]['emp_add']=empadd_serializer.data
                  #print(empadd_serializer.data)
                  #travel_request_serializer.data[0]['date']=datetime.now().date().strftime("%d-%b-%Y")
                  travel_requests=Travel_Request.objects.filter(travel_req_id =id)
                  travel_request_serializers= Travel_RequestSerializers(travel_requests,many=True)
                  travel_request_serializer.data[0]['travel']=travel_request_serializers.data

                  travel_requestes=Assignment_Travel_Tax_Grid.objects.filter(travel_req_id =id)
                  travel_request_serializeres= Assignment_Travel_Tax_GridSerializers(travel_requestes,many=True)
                  travel_request_serializer.data[0]['travel_combdata']=travel_request_serializeres.data

                  travel_requestss=Travel_Request_Details.objects.filter(travel_req_id =id)
                  travel_request_serializerss = Travel_Request_DetailsSerializers(travel_requestss,many=True)
                  travel_request_serializer.data[0]['details']=travel_request_serializerss.data
                  empadd = Employee_Passport_Detail.objects.filter(emp_code=emp_code)
                  emppassport_serializer = Employee_Passport_DetailSerializers(empadd,many=True)
                  travel_request_serializer.data[0]['emp_passport']=emppassport_serializer.data
                  datas={}

                  # print("###############emp_serializer.data")
                  # print(travel_request_serializer.data[0]['emp_info'])
                  # print("############### length travel_request_serializer.data #########")
                  # print(len(travel_request_serializer.data))
                  for data in travel_request_serializer.data:
                     print("############### length travel_request_serializer.data #########")
                     print(data)
                     if data['emp_info']:
                        if data['emp_info'][0]['first_name']:
                           first_name=data['emp_info'][0]['first_name']
                        else:
                           first_name=""
                        if data['emp_info'][0]['last_name']:
                           last_name=data['emp_info'][0]['last_name']
                        else:
                           last_name=""
                        if data['emp_info'][0]['nationality']:
                           datas['Citizenship']=data['emp_info'][0]['nationality']
                        else:
                           datas['Citizenship']=""
                        if data['emp_info'][0]['dob']:
                           datas['DateofBirth']=self.date_format(date=data['emp_info'][0]['dob'])
                        else:
                           datas['DateofBirth']=""
                     datas['AssigneeName']=first_name+' '+last_name
                     #print(datas['AssigneeName'])
                     datas['JobTitle']=""
                     datas['TodayDate']=datetime.now()
                     datas['AssignmentStartDate']=data['Actual_Start_Date']
                     datas['AssignmentEndDate']=data['Actual_End_Date']
                     datas['AssignmentType']=data['Assignment_Type']
                     datas['TravelID']=data['Ticket_ID']
                     datas['EmployeeID']=data['Employee_ID']
                     #print(data['details'])
                     if data['details']:
                        datas['travelling_country_to']=data['details'][i]['travelling_country_to']
                        datas['travelling_country']=data['details'][i]['travelling_country']
                        
                        #print(datas['travelling_country_to'])
                        if data['details'][i]['client_name']:
                           datas['ClientName']=data['details'][i]['client_name']
                        else:
                           datas['ClientName']=""
                        if data['details'][i]['host_attorney']:
                           datas['ProjectContact']=data['details'][i]['host_attorney']
                        else:
                           datas['ProjectContact']=""
                        if data['details'][i]['destination_city']:
                           datas['HostCity']=data['details'][i]['destination_city']
                        else:
                           datas['Host City']=""
                        if data['details'][i]['host_hr_name']:
                           datas['HostContactName']=data['details'][i]['host_hr_name']
                        else:
                           datas['HostContactName']=""

                        if data['details'][i]['host_country_head']:
                           datas['HostEntityName']=data['details'][i]['host_country_head']
                        else:
                           datas['HostEntityName']=""

                        if data['details'][i]['host_phone_no']:
                           phone=data['details'][i]['host_phone_no']
                        else:
                           phone=""
                        if data['details'][i]['host_phone_ext']:
                           ext=data['details'][i]['host_phone_ext']
                        else:
                           ext=""
                        datas['HostContactPhoneNumber']=ext+phone
                        if data['details'][i]['visa_number']:
                           datas['VisaNumber']=data['details'][i]['visa_number']
                        else:
                           datas['VisaNumber']=""
                        if data['details'][i]['visa_expiry_date']:
                           datas['VisaValidity']=self.date_format(date=data['details'][i]['visa_expiry_date'])
                        else:
                           datas['VisaValidity']=""
                        if data['details'][i]['applicable_visa']:
                           datas['VisaCategory']=data['details'][i]['applicable_visa']
                        else:
                           datas['VisaCategory']=""
                        if data['details'][i]['agenda']:
                           datas['DayWiseAgenda']=data['details'][i]['agenda']
                        else:
                           datas['DayWiseAgenda']=""
                        if data['details'][i]['applicable_visa']:
                           datas['VisaType']=data['details'][i]['applicable_visa']
                        else:
                           datas['VisaType']=""
                           
                        if data['details'][i]['host_hr_name']:
                           datas['HostEntityName']=data['details'][i]['host_hr_name']
                        else:
                           datas['HostEntityName']=""
                        i=i+1   
                     datas['VisaCountry']=datas['travelling_country_to'] 
                     datas['HostCountry']=datas['travelling_country_to'] 
                     datas['HomeCountry']=datas['travelling_country']
                     if data['emp_passport']:
                        print('#########################################################')
                        print(data['emp_passport'])
                        if data['emp_passport'][0]['passport_number']:
                           datas['PassportNo']=data['emp_passport'][0]['passport_number']
                        else:
                           datas['PassportNo']=""
                        if data['emp_passport'][0]['date_of_expiration']:
                           datas['PassportValidity']=self.date_format(date=data['emp_passport'][0]['date_of_expiration'])
                        else:
                           datas['PassportValidity']=""
                        if data['emp_passport'][0]['nationality']:
                           datas['Nationality']=data['emp_passport'][0]['nationality']
                        else:
                           datas['Nationality']=""
                        if data['emp_passport'][0]['country_of_issue']:
                           datas['CountryofIssue']=data['emp_passport'][0]['country_of_issue']
                        else:
                           datas['CountryofIssue']=""
                        
                        if data['emp_passport'][0]['place_of_issue']:
                           datas['PlaceofIssue']=data['emp_passport'][0]['place_of_issue']
                        else:
                           datas['PlaceofIssue']=""

                        if data['emp_passport'][0]['date_of_issue']:
                           datas['DateofIssue']=self.date_format(date=data['emp_passport'][0]['date_of_issue'])
                        else:
                           datas['DateofIssue']=""

                        if data['emp_passport'][0]['date_of_expiration']:
                           datas['DateofExpiration']=self.date_format(date=data['emp_passport'][0]['date_of_expiration'])
                        else:
                           datas['DateofExpiration']=""
                     if data['travel']:
                        if data['travel'][0]['project_name']:
                           datas['ProjectName']=data['travel'][0]['project_name']
                        else:
                           datas['ProjectName']=""   
                        if data['travel'][0]['project']:
                           datas['ProjectIDWBSECode']=data['travel'][0]['project']
                        else:
                           datas['ProjectIDWBSECode']=""
                        if data['travel'][0]['home_contact_name']:
                           datas['HomeEntityName']=data['travel'][0]['home_contact_name']
                        else:
                           datas['HomeEntityName']=""
                     
                     gross=Assignment_Travel_Tax_Grid.objects.filter(travel_req_id =id,tax_label='Gross Base Salary').values('annual_ammount')
                     
                     if gross:
                        datas['GrossBaseSalary']=gross[0]['annual_ammount']
                     else:
                        datas['GrossBaseSalary']=""
                     equity=Assignment_Travel_Tax_Grid.objects.filter(travel_req_id =id,tax_label='Equity Income').values('annual_ammount')
                     
                     if equity:
                        datas['EquityIncome']=equity[0]['annual_ammount']
                     else:
                        datas['EquityIncome']=""
                     
                     merit=Assignment_Travel_Tax_Grid.objects.filter(travel_req_id =id,tax_label='Merit Bonus').values('annual_ammount')
                     
                     if merit:
                        datas['MeritBonus']=merit[0]['annual_ammount']
                     else:
                        datas['MeritBonus']=""

                     pre=Assignment_Travel_Tax_Grid.objects.filter(travel_req_id =id,tax_label='Pre-Move Trip').values('annual_ammount')
                     
                     if pre:
                        datas['PreMoveTrip']=pre[0]['annual_ammount']
                     else:
                        datas['PreMoveTrip']=""

                     temporary=Assignment_Travel_Tax_Grid.objects.filter(travel_req_id =id,tax_label='Temporary Living in Host Country').values('annual_ammount')
                     
                     if temporary:
                        datas['TemporaryLivinginHostCountry']=temporary[0]['annual_ammount']
                     else:
                        datas['TemporaryLivinginHostCountry']=""
                     
                     relocation=Assignment_Travel_Tax_Grid.objects.filter(travel_req_id =id,tax_label='Relocation Allowance').values('annual_ammount')
                     
                     if relocation:
                        datas['RelocationAllowance']=relocation[0]['annual_ammount']
                     else:
                        datas['RelocationAllowance']=""

                     start=Assignment_Travel_Tax_Grid.objects.filter(travel_req_id =id,tax_label='Start Up Allowance').values('annual_ammount')
                     
                     if start:
                        datas['StartUpAllowance']=start[0]['annual_ammount']
                     else:
                        datas['StartUpAllowance']=""

                     cost=Assignment_Travel_Tax_Grid.objects.filter(travel_req_id =id,tax_label='Cost of Living Allowance').values('annual_ammount')
                     
                     if cost:
                        datas['CostofLivingAllowance']=cost[0]['annual_ammount']
                     else:
                        datas['CostofLivingAllowance']=""
                     
                     hardship=Assignment_Travel_Tax_Grid.objects.filter(travel_req_id =id,tax_label='Hardship Allowance').values('annual_ammount')
                     
                     if hardship:
                        datas['HardshipAllowance']=hardship[0]['annual_ammount']
                     else:
                        datas['HardshipAllowance']=""
                     
                     hosthousing=Assignment_Travel_Tax_Grid.objects.filter(travel_req_id =id,tax_label='Host Housing Allowance').values('annual_ammount')
                     
                     if hosthousing:
                        datas['HostHousingAllowance']=hosthousing[0]['annual_ammount']
                     else:
                        datas['HostHousingAllowance']=""
                     
                     school=Assignment_Travel_Tax_Grid.objects.filter(travel_req_id =id,tax_label='School Tuition - Self').values('annual_ammount')
                     
                     if school:
                        datas['SchoolTuitionSelf']=school[0]['annual_ammount']
                     else:
                        datas['SchoolTuitionSelf']=""


                     country=Country_Master.objects.filter(name=datas['travelling_country_to']).values("country_id")
                     print(country[0]['country_id'])
                     lettername=Letters.objects.filter(letter_type="Assignment Letter",country=country[0]['country_id'],letter_term=datas['AssignmentType']).values("letter_name")
                     print('############# leter name ##')
                     print(lettername)
                     print(datas['AssignmentType'])
                     if lettername:
                        lettername=lettername[0]['letter_name'].lstrip('templates/')
                        template = get_template(lettername)
                        filenames = lettername.rstrip('.html')
                        filename = filenames+'.pdf'
                        html = template.render(datas)
                        result = BytesIO()
                        file = open("uploadpdf/"+filename, "w+b")
                        print('############## file')
                        print(file)
                        #current_url = request.path_info
                        #print(current_url)
                        emp_codess="vikasy@triazinesoft.com"
                        pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
                        attachment = open('uploadpdf/'+filename, 'rb')
                     else:
                        filename=""
                        attachment=""
                     letternames=Letters.objects.filter(letter_type="Visa Letter",country=country[0]['country_id']).values("letter_name")
                     if letternames:
                        letternamess=letternames[0]['letter_name'].lstrip('templates/')

                        
                        templatess = get_template(letternamess)

                        filenamess = letternamess.rstrip('.html')
                        filenamess = filenamess+'.pdf'

                        html = templatess.render(datas)


                        result = BytesIO()

                        filess= open("uploadpdf/"+filenamess, "w+b")
                        pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=filess, encoding='utf-8')
                        attachments = open('uploadpdf/'+filenamess, 'rb')
                     else:
                        filenamess=""
                        attachments=""
                     inviteletternames=Letters.objects.filter(letter_type="Invite Letter",country=country[0]['country_id']).values("letter_name")
                     if inviteletternames:
                        inviteletternames=inviteletternames[0]['letter_name'].lstrip('templates/')
                        invitetemplates = get_template(inviteletternames)
                        invitefilenamess = inviteletternames.rstrip('.html')
                        invitefilenamess = invitefilenamess+'.pdf'

                        html = invitetemplates.render(datas)


                        result = BytesIO()

                        files= open("uploadpdf/"+invitefilenamess, "w+b")
                        #current_url = request.path_info
                        print(datas['travelling_country_to'])
                        emp_codess="vikasy@triazinesoft.com"
                        pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=files, encoding='utf-8')
                        inviteattachments = open('uploadpdf/'+invitefilenamess, 'rb')
                     else:
                        invitefilenamess=""
                        inviteattachments=""
                     email = EmailMessage(subject='Letters',
                                          body='Please Find the attachment Letters for travel id'+id+datas['travelling_country_to'],
                                          from_email='vikasy@triazinesoft.com',
                                          to=[emp_code,'vikasy@triazinesoft.com'],
                                          headers = {'Reply-To': 'vikasy@triazinesoft.com'})

                     # Open PDF file
                  
                     # Attach PDF file
                     
                     if filename:
                        email.attach(filename,attachment.read(),'application/pdf')
                        letter.append('uploadpdf/'+filename)
                        
                     if filenamess:
                        email.attach(filenamess,attachments.read(),'application/pdf')
                        letter.append('uploadpdf/'+filenamess)
                        
                     if invitefilenamess:
                        email.attach(invitefilenamess,inviteattachments.read(),'application/pdf')
                        letter.append('uploadpdf/'+invitefilenamess)
                        
                     
                     # Send message with built-in send() method
                     email.send()
                     
                     print(letter)
                     
                     # dict = {'massage': 'data found', 'status': True, 'datas': letter,'data': 'uploadpdf/'+filename,'visadata': 'uploadpdf/'+filenamess,'invitedata': 'uploadpdf/'+invitefilenamess,'datakeys':datas }
            else:
               id=travel_statu['travel_req_id']
               travel_request= Travel_Request.objects.filter(travel_req_id =id)
               if travel_request.exists():
                     travel_request_serializer = Travel_RequestSerializers(travel_request,many=True)
                     emp_code=travel_request_serializer.data[0]['emp_email']
                     print(emp_code)
                     emp = Employee.objects.filter(emp_code=emp_code)
                     emp_serializer = EmployeeSerializers(emp,many=True)
                     travel_request_serializer.data[0]['emp_info']=emp_serializer.data
                     empcode=emp_serializer.data[0]['emp_code']
                     empadd = Employee_Address.objects.filter(emp_code=empcode,address_type="host")
                     empadd_serializer = Employee_AddressSerializers(empadd,many=True)
                     travel_request_serializer.data[0]['emp_add']=empadd_serializer.data
                     #travel_request_serializer.data[0]['date']=datetime.now().date().strftime("%d-%b-%Y")
                     travel_requests=Travel_Request.objects.filter(travel_req_id =id)
                     travel_request_serializers= Travel_RequestSerializers(travel_requests,many=True)
                     travel_request_serializer.data[0]['travel']=travel_request_serializers.data
                     travel_requestss=Travel_Request_Details.objects.filter(travel_req_id =id)
                     travel_request_serializerss = Travel_Request_DetailsSerializers(travel_requestss,many=True)
                     travel_request_serializer.data[0]['details']=travel_request_serializerss.data
                     print(emp_code)
                     emppass = Employee_Passport_Detail.objects.filter(emp_code=emp_code)
                     emppassport_serializer = Employee_Passport_DetailSerializers(emppass,many=True)
                     travel_request_serializer.data[0]['emp_passport']=emppassport_serializer.data
                     datas={}
                     
                     for data in travel_request_serializer.data:
                        if data['emp_info']:
                           if data['emp_info'][0]['first_name']:
                              first_name=data['emp_info'][0]['first_name']
                           else:
                              first_name=""
                           if data['emp_info'][0]['last_name']:
                              last_name=data['emp_info'][0]['last_name']
                           else:
                              last_name=""
                           if data['emp_info'][0]['nationality']:
                              datas['Citizenship']=data['emp_info'][0]['nationality']
                           else:
                              datas['Citizenship']=""
                           if data['emp_info'][0]['dob']:
                              datas['DateofBirth']=self.date_format(date=data['emp_info'][0]['dob'])
                           else:
                              datas['DateofBirth']=""
                        datas['AssigneeName']=first_name+' '+last_name
                        datas['JobTitle']=""
                        datetoday=datetime.now()
                        print(datetoday)
                        datas['TodayDate']=datetime.now()
                        if data['details']:
                           datas['travelling_country_to']=data['details'][i]['travelling_country_to']
                           datas['travelling_country']=data['details'][i]['travelling_country']
                           print(datas['travelling_country_to'])
                           if data['details'][i]['client_name']:
                              datas['ClientName']=data['details'][i]['client_name']
                           else:
                              datas['ClientName']=""
                           if data['details'][i]['host_attorney']:
                              datas['ProjectContact']=data['details'][i]['host_attorney']
                           else:
                              datas['ProjectContact']=""
                           if data['details'][i]['destination_city']:
                              datas['HostCity']=data['details'][i]['destination_city']
                           else:
                              datas['Host City']=""
                           if data['details'][i]['host_hr_name']:
                              datas['HostContactName']=data['details'][i]['host_hr_name']
                           else:
                              datas['HostContactName']=""

                           if data['details'][i]['host_hr_name']:
                              datas['HostEntityName']=data['details'][i]['host_hr_name']
                           else:
                              datas['HostEntityName']=""

                           if data['details'][i]['host_phone_no']:
                              phone=data['details'][i]['host_phone_no']
                           else:
                              phone=""
                           if data['details'][i]['host_phone_ext']:
                              ext=data['details'][i]['host_phone_ext']
                           else:
                              ext=""
                           datas['HostContactPhoneNumber']=ext+phone
                           if data['details'][i]['visa_number']:
                              datas['VisaNumber']=data['details'][i]['visa_number']
                           else:
                              datas['VisaNumber']=""
                           if data['details'][i]['visa_expiry_date']:
                              datas['VisaValidity']=self.date_format(date=data['details'][i]['visa_expiry_date'])
                           else:
                              datas['VisaValidity']=""
                           if data['details'][i]['applicable_visa']:
                              datas['VisaCategory']=data['details'][i]['applicable_visa']
                           else:
                              datas['VisaCategory']=""
                           if data['details'][i]['agenda']:
                              datas['DayWiseAgenda']=data['details'][i]['agenda']
                           else:
                              datas['DayWiseAgenda']=""
                           if data['details'][i]['applicable_visa']:
                              datas['VisaType']=data['details'][i]['applicable_visa']
                           else:
                              datas['VisaType']=""
                              
                           if data['details'][i]['host_hr_name']:
                              datas['HostEntityName']=data['details'][i]['host_hr_name']
                           else:
                              datas['HostEntityName']=""
                           
                           i=i+1
                        datas['VisaCountry']=datas['travelling_country_to'] 
                        datas['HostCountry']=datas['travelling_country_to'] 
                        datas['HomeCountry']=datas['travelling_country']   
                        if data['emp_passport']:
                           #print(data['emp_passport'][0]['passort_number'])
                           if data['emp_passport'][0]['passport_number']:
                              datas['PassportNo']=data['emp_passport'][0]['passport_number']
                           else:
                              datas['PassportNo']=""
                           if data['emp_passport'][0]['date_of_expiration']:
                              datas['PassportValidity']=self.date_format(date=data['emp_passport'][0]['date_of_expiration'])
                           else:
                              datas['PassportValidity']=""
                           if data['emp_passport'][0]['nationality']:
                              datas['Nationality']=data['emp_passport'][0]['nationality']
                           else:
                              datas['Nationality']=""

                           if data['emp_passport'][0]['country_of_issue']:
                              datas['CountryofIssue']=data['emp_passport'][0]['country_of_issue']
                           else:
                              datas['CountryofIssue']=""
                           
                           if data['emp_passport'][0]['place_of_issue']:
                              datas['PlaceofIssue']=data['emp_passport'][0]['place_of_issue']
                           else:
                              datas['PlaceofIssue']=""

                           if data['emp_passport'][0]['date_of_issue']:
                              datas['DateofIssue']=self.date_format(date=data['emp_passport'][0]['date_of_issue'])
                           else:
                              datas['DateofIssue']=""

                           if data['emp_passport'][0]['date_of_expiration']:
                              datas['DateofExpiration']=self.date_format(date=data['emp_passport'][0]['date_of_expiration'])
                           else:
                              datas['DateofExpiration']=""
                        if data['travel']:
                           if data['travel'][0]['project_name']:
                              datas['ProjectName']=data['travel'][0]['project_name']
                           else:
                              datas['ProjectName']=""   
                           if data['travel'][0]['project']:
                              datas['ProjectIDWBSECode']=data['travel'][0]['project']
                           else:
                              datas['ProjectIDWBSECode']=""
                           if data['travel'][0]['home_contact_name']:
                              datas['HomeEntityName']=data['travel'][0]['home_contact_name']
                           else:
                              datas['HomeEntityName']=""
                     country=Country_Master.objects.filter(name=datas['travelling_country_to']).values("country_id")
                     letternames=Letters.objects.filter(letter_type="Visa Letter",country=country[0]['country_id']).values("letter_name")
                     if letternames:
                        letternamess=letternames[0]['letter_name'].lstrip('templates/')
                        templatess = get_template(letternamess)
                        filenamess = letternamess.rstrip('.html')
                        filenamess = filenamess+'.pdf'

                        html = templatess.render(datas)


                        result = BytesIO()

                        filess= open("uploadpdf/"+filenamess, "w+b")
                        pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=filess, encoding='utf-8')
                        attachments = open('uploadpdf/'+filenamess, 'rb')
                     else:
                        filenamess=""
                        attachments=""
                     inviteletternames=Letters.objects.filter(letter_type="Invite Letter",country=country[0]['country_id']).values("letter_name")
                     if inviteletternames:
                        inviteletternames=inviteletternames[0]['letter_name'].lstrip('templates/')
                        invitetemplates = get_template(inviteletternames)
                        invitefilenamess = inviteletternames.rstrip('.html')
                        invitefilenamess = invitefilenamess+'.pdf'

                        html = invitetemplates.render(datas)


                        result = BytesIO()

                        files= open("uploadpdf/"+invitefilenamess, "w+b")
                        #current_url = request.path_info
                        #print(current_url)
                        emp_codess="vikasy@triazinesoft.com"
                        pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=files, encoding='utf-8')
                        inviteattachments = open('uploadpdf/'+invitefilenamess, 'rb')
                     else:
                        invitefilenamess=""
                        inviteattachments=""
                     print(emp_code)
                     email = EmailMessage(subject='Letters',
                                       body='Please Find the attachment Letters for travel id'+id+datas['travelling_country_to'],
                                       from_email='vikasy@triazinesoft.com',
                                       to=[emp_code,'vikasy@triazinesoft.com'],
                                       headers = {'Reply-To': 'vikasy@triazinesoft.com'})

                     # Open PDF file
                  
                     # Attach PDF file
                     if filenamess:
                        email.attach(filenamess,attachments.read(),'application/pdf')
                        letter.append('uploadpdf/'+filenamess)
                     if invitefilenamess:
                        email.attach(invitefilenamess,inviteattachments.read(),'application/pdf')
                        letter.append('uploadpdf/'+invitefilenamess)
                     # Send message with built-in send() method
                     email.send()
            
            zipObj = ZipFile('uploadpdf/letters_'+id+'.zip', 'w')
            for letters in letter:
               print(letters)
               zipObj.write(letters)
            # close the Zip File
            zipObj.close()
            
            #http://52.165.220.40/mobilitysqrapi/uploadpdf/sample1.zip
            # email = EmailMessage(subject='Letters',
            #                            body='Please Find the attachment Letters for travel id'+id+datas['travelling_country_to'],
            #                            from_email='vikasy@triazinesoft.com',
            #                            to=['vikasy@triazinesoft.com','vikasy@triazinesoft.com'],
            #                            headers = {'Reply-To': 'vikasy@triazinesoft.com'}) 
            # email.attach('http://52.165.220.40/mobilitysqrapi/uploadpdf/sample1.zip','application/rar')
            
            # email.send()               
            dict = {'massage': 'data found', 'status': True, 'data': 'http://api.mobilitysqr.net/mobilitysqr_api/mobilitysqr_staging_virtualenv/mobilitysqr_staging/uploadpdf/letters_'+id+'.zip' }
      else:
         dict = {'massage': 'Assignment Not Generated', 'status': False}
      return Response(dict, status=status.HTTP_200_OK)

   def date_format(self,date):
        
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        
        date=date[0:10]
        # utc = datetime.utcnow()
        utc = datetime.strptime(date, '%Y-%m-%d')
        # Tell the datetime object that it's in UTC time zone since 
        # datetime objects are 'naive' by default
        utc = utc.replace(tzinfo=from_zone)
        # Convert time zone
        central = utc.astimezone(to_zone)
        string=str(central)
        demo= string[0:10].split("-")
        new_case_date = demo[2]+"/"+demo[1]+"/"+demo[0]
        return new_case_date

       
class getinviteletter(APIView):
    def get(self,request, *args, **kwargs):
        id=request.GET['travel_req_id']
        travel_request= Create_Assignment.objects.filter(Ticket_ID =request.GET['travel_req_id'])
        print(travel_request)
        if travel_request.exists():
            travel_request_serializer = Create_AssignmentSerializers(travel_request,many=True)
            emp_code=travel_request_serializer.data[0]['Employee_ID']
            emp = Employee.objects.filter(email=emp_code)
            emp_serializer = EmployeeSerializers(emp,many=True)
            travel_request_serializer.data[0]['emp_info']=emp_serializer.data
            empcode=emp_serializer.data[0]['emp_code']
            empadd = Employee_Address.objects.filter(emp_code=empcode,address_type="host")
            empadd_serializer = Employee_AddressSerializers(empadd,many=True)
            travel_request_serializer.data[0]['emp_add']=empadd_serializer.data
            print(empadd_serializer.data)
            #travel_request_serializer.data[0]['date']=datetime.now().date().strftime("%d-%b-%Y")
            travel_requests=Travel_Request.objects.filter(travel_req_id =id)
            travel_request_serializers= Travel_RequestSerializers(travel_requests,many=True)
            travel_request_serializer.data[0]['travel']=travel_request_serializers.data
            travel_requestss=Travel_Request_Details.objects.filter(travel_req_id =id)
            travel_request_serializerss = Travel_Request_DetailsSerializers(travel_requestss,many=True)
            travel_request_serializer.data[0]['details']=travel_request_serializerss.data
            empadd = Employee_Passport_Detail.objects.filter(emp_code=emp_code)
            emppassport_serializer = Employee_Passport_DetailSerializers(empadd,many=True)
            travel_request_serializer.data[0]['emp_passport']=emppassport_serializer.data
            '''empadd = Employee_Emails.objects.filter(emp_code=emp_code)
            empemails_serializer = Employee_EmailsSerializers(empadd,many=True)
            emp_serializer.data[0]['emp_emails']=empemails_serializer.data
            empadd = Employee_Emergency_Contact.objects.filter(emp_code=emp_code)
            empemergency_serializer = Employee_Emergency_ContactSerializers(empadd,many=True)
            emp_serializer.data[0]['emp_emergency']=empemergency_serializer.data
            empadd = Employee_Phones.objects.filter(emp_code=emp_code)
            empphones_serializer = Employee_PhonesSerializers(empadd,many=True)
            emp_serializer.data[0]['emp_phones']=empphones_serializer.data
            empadd = Employee_Nationalid.objects.filter(emp_code=emp_code)
            empnational_serializer = Employee_NationalidSerializers(empadd,many=True)
            emp_serializer.data[0]['emp_national']=empnational_serializer.data
            empadd = Employee_Passport_Detail.objects.filter(emp_code=emp_code)
            emppassport_serializer = Employee_Passport_DetailSerializers(empadd,many=True)
            emp_serializer.data[0]['emp_passport']=emppassport_serializer.data
            empadd = Employee_Visa_Detail.objects.filter(emp_code=emp_code)
            empvisa_serializer = Employee_Visa_DetailSerializers(empadd,many=True)
            emp_serializer.data[0]['emp_visa']=empvisa_serializer.data'''

            #data= travel_request_serializer.data
            #print(data)

            datas={}
            for data in travel_request_serializer.data:
               if data['emp_info']:
                  if data['emp_info'][0]['first_name']:
                     first_name=data['emp_info'][0]['first_name']
                  else:
                     first_name=""
                  if data['emp_info'][0]['last_name']:
                     last_name=data['emp_info'][0]['last_name']
                  else:
                     last_name=""
                  if data['emp_info'][0]['nationality']:
                     datas['Citizenship']=data['emp_info'][0]['nationality']
                  else:
                     datas['Citizenship']=""
                  
               datas['AssigneeName']=first_name+' '+last_name
               print(datas['AssigneeName'])
               datas['JobTitle']=""
               datas['TodayDate']=date.today()
               datas['AssignmentStartDate']=data['Actual_Start_Date']
               datas['AssignmentEndDate']=data['Actual_End_Date']
               datas['AssignmentType']=data['Assignment_Type']
               datas['TravelID']=data['Ticket_ID']
               datas['EmployeeID']=data['Employee_ID']
               print(data['details'])
               if data['details']:
                  if data['details'][0]['client_name']:
                     datas['ClientName']=data['details'][0]['client_name']
                  else:
                     datas['ClientName']=""
                  if data['details'][0]['host_attorney']:
                     datas['ProjectContact']=data['details'][0]['host_attorney']
                  else:
                     datas['ProjectContact']=""
                  if data['details'][0]['destination_city']:
                     datas['HostCity']=data['details'][0]['destination_city']
                  else:
                     datas['Host City']=""
                  if data['details'][0]['host_hr_name']:
                     datas['HostContactName']=data['details'][0]['host_hr_name']
                  else:
                     datas['HostContactName']=""

                  if data['details'][0]['host_country_head']:
                     datas['HostEntityName']=data['details'][0]['host_country_head']
                  else:
                     datas['HostEntityName']=""

                  if data['details'][0]['host_phone_no']:
                     phone=data['details'][0]['host_phone_no']
                  else:
                     phone=""
                  if data['details'][0]['host_phone_ext']:
                     ext=data['details'][0]['host_phone_ext']
                  else:
                     ext=""
                  datas['HostContactPhoneNumber']=ext+phone
                  if data['details'][0]['visa_number']:
                     datas['VisaNumber']=data['details'][0]['visa_number']
                  else:
                     datas['VisaNumber']=""
                  if data['details'][0]['visa_expiry_date']:
                     datas['VisaValidity']=data['details'][0]['visa_expiry_date']
                  else:
                     datas['VisaValidity']=""
                  if data['details'][0]['applicable_visa']:
                     datas['VisaCategory']=data['details'][0]['applicable_visa']
                  else:
                     datas['VisaCategory']=""
                  if data['details'][0]['agenda']:
                     datas['DayWiseAgenda']=data['details'][0]['agenda']
                  else:
                     datas['DayWiseAgenda']=""
                  if data['details'][0]['applicable_visa']:
                     datas['VisaType']=data['details'][0]['applicable_visa']
                  else:
                     datas['VisaType']=""
               datas['VisaCountry']=data['Host_Country']
               datas['HostCountry']=data['Host_Country'] 
               datas['HomeCountry']= data['Home_Country']
               if data['emp_passport']:
                  if data['emp_passport'][0]['passort_number']:
                     datas['PassportNo']=data['emp_passport'][0]['passort_number']
                  else:
                     datas['PassportNo']=""
                  if data['emp_passport'][0]['date_of_expiration']:
                     datas['PassportValidity']=data['emp_passport'][0]['date_of_expiration']
                  else:
                     datas['PassportValidity']=""
               if data['travel']:
                  if data['travel'][0]['project_name']:
                     datas['ProjectName']=data['travel'][0]['project_name']
                  else:
                     datas['ProjectName']=""   
                  if data['travel'][0]['project']:
                     datas['ProjectIDWBSECode']=data['travel'][0]['project']
                  else:
                     datas['ProjectIDWBSECode']=""
                  if data['travel'][0]['home_contact_name']:
                     datas['HomeEntityName']=data['travel'][0]['home_contact_name']
                  else:
                     datas['HomeEntityName']=""
            country=Country_Master.objects.filter(Q(name__icontains=request.GET['country']))
            lettername=Letters.objects.filter(letter_type="Invite Letter").values("letter_name")
            lettername=lettername[0]['letter_name'].lstrip('templates/')
            #print(lettername)
            template = get_template(lettername)
            filenames = lettername.rstrip('.html')
            filename = filenames+'.pdf'
            #print(template)
            html = template.render(datas)
            result = BytesIO()
            file = open("uploadpdf/"+filename, "w+b")
            #current_url = request.path_info
            #print(current_url)
            emp_codess="vikasy@triazinesoft.com"
            pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
            email = EmailMessage(subject='Invite Letter',
                                 body='Please Find the attachment report Below',
                                 from_email='vikasy@triazinesoft.com',
                                 to=[emp_code,'vikasy@triazinesoft.com'],
                                 headers = {'Reply-To': 'vikasy@triazinesoft.com'})

            # Open PDF file
            attachment = open('uploadpdf/'+filename, 'rb')

            # Attach PDF file
            email.attach(filename,attachment.read(),'application/pdf')

            # Send message with built-in send() method
            email.send()
            dict = {'massage': 'data found', 'status': True, 'data': 'uploadpdf/'+filename }
        else:
            dict = {'massage': 'data not found', 'status': False}
        #dict = {'massage': 'data found', 'status': True, 'data': travel_request_serializer.data[0] }
        return Response(dict, status=status.HTTP_200_OK)

class getvisaletter(APIView):
    def get(self,request, *args, **kwargs):
        id=request.GET['travel_req_id']
        travel_request= Create_Assignment.objects.filter(Ticket_ID =request.GET['travel_req_id'])
        print(travel_request)
        if travel_request.exists():
            travel_request_serializer = Create_AssignmentSerializers(travel_request,many=True)
            emp_code=travel_request_serializer.data[0]['Employee_ID']
            emp = Employee.objects.filter(email=emp_code)
            emp_serializer = EmployeeSerializers(emp,many=True)
            travel_request_serializer.data[0]['emp_info']=emp_serializer.data
            empcode=emp_serializer.data[0]['emp_code']
            empadd = Employee_Address.objects.filter(emp_code=empcode,address_type="host")
            empadd_serializer = Employee_AddressSerializers(empadd,many=True)
            travel_request_serializer.data[0]['emp_add']=empadd_serializer.data
            print(empadd_serializer.data)
            #travel_request_serializer.data[0]['date']=datetime.now().date().strftime("%d-%b-%Y")
            travel_requests=Travel_Request.objects.filter(travel_req_id =id)
            travel_request_serializers= Travel_RequestSerializers(travel_requests,many=True)
            travel_request_serializer.data[0]['travel']=travel_request_serializers.data
            travel_requestss=Travel_Request_Details.objects.filter(travel_req_id =id)
            travel_request_serializerss = Travel_Request_DetailsSerializers(travel_requestss,many=True)
            travel_request_serializer.data[0]['details']=travel_request_serializerss.data
            empadd = Employee_Passport_Detail.objects.filter(emp_code=emp_code)
            emppassport_serializer = Employee_Passport_DetailSerializers(empadd,many=True)
            travel_request_serializer.data[0]['emp_passport']=emppassport_serializer.data
            '''empadd = Employee_Emails.objects.filter(emp_code=emp_code)
            empemails_serializer = Employee_EmailsSerializers(empadd,many=True)
            emp_serializer.data[0]['emp_emails']=empemails_serializer.data
            empadd = Employee_Emergency_Contact.objects.filter(emp_code=emp_code)
            empemergency_serializer = Employee_Emergency_ContactSerializers(empadd,many=True)
            emp_serializer.data[0]['emp_emergency']=empemergency_serializer.data
            empadd = Employee_Phones.objects.filter(emp_code=emp_code)
            empphones_serializer = Employee_PhonesSerializers(empadd,many=True)
            emp_serializer.data[0]['emp_phones']=empphones_serializer.data
            empadd = Employee_Nationalid.objects.filter(emp_code=emp_code)
            empnational_serializer = Employee_NationalidSerializers(empadd,many=True)
            emp_serializer.data[0]['emp_national']=empnational_serializer.data
            empadd = Employee_Passport_Detail.objects.filter(emp_code=emp_code)
            emppassport_serializer = Employee_Passport_DetailSerializers(empadd,many=True)
            emp_serializer.data[0]['emp_passport']=emppassport_serializer.data
            empadd = Employee_Visa_Detail.objects.filter(emp_code=emp_code)
            empvisa_serializer = Employee_Visa_DetailSerializers(empadd,many=True)
            emp_serializer.data[0]['emp_visa']=empvisa_serializer.data'''

            #data= travel_request_serializer.data
            #print(data)

            datas={}
            for data in travel_request_serializer.data:
               if data['emp_info']:
                  if data['emp_info'][0]['first_name']:
                     first_name=data['emp_info'][0]['first_name']
                  else:
                     first_name=""
                  if data['emp_info'][0]['last_name']:
                     last_name=data['emp_info'][0]['last_name']
                  else:
                     last_name=""
                  if data['emp_info'][0]['nationality']:
                     datas['Citizenship']=data['emp_info'][0]['nationality']
                  else:
                     datas['Citizenship']=""
                  
               datas['AssigneeName']=first_name+' '+last_name
               print(datas['AssigneeName'])
               datas['JobTitle']=""
               datas['TodayDate']=date.today()
               datas['AssignmentStartDate']=data['Actual_Start_Date']
               datas['AssignmentEndDate']=data['Actual_End_Date']
               datas['AssignmentType']=data['Assignment_Type']
               datas['TravelID']=data['Ticket_ID']
               datas['EmployeeID']=data['Employee_ID']
               print(data['details'])
               if data['details']:
                  if data['details'][0]['client_name']:
                     datas['ClientName']=data['details'][0]['client_name']
                  else:
                     datas['ClientName']=""
                  if data['details'][0]['host_attorney']:
                     datas['ProjectContact']=data['details'][0]['host_attorney']
                  else:
                     datas['ProjectContact']=""
                  if data['details'][0]['destination_city']:
                     datas['HostCity']=data['details'][0]['destination_city']
                  else:
                     datas['Host City']=""
                  if data['details'][0]['host_hr_name']:
                     datas['HostContactName']=data['details'][0]['host_hr_name']
                  else:
                     datas['HostContactName']=""

                  if data['details'][0]['host_country_head']:
                     datas['HostEntityName']=data['details'][0]['host_country_head']
                  else:
                     datas['HostEntityName']=""

                  if data['details'][0]['host_phone_no']:
                     phone=data['details'][0]['host_phone_no']
                  else:
                     phone=""
                  if data['details'][0]['host_phone_ext']:
                     ext=data['details'][0]['host_phone_ext']
                  else:
                     ext=""
                  datas['HostContactPhoneNumber']=ext+phone
                  if data['details'][0]['visa_number']:
                     datas['VisaNumber']=data['details'][0]['visa_number']
                  else:
                     datas['VisaNumber']=""
                  if data['details'][0]['visa_expiry_date']:
                     datas['VisaValidity']=data['details'][0]['visa_expiry_date']
                  else:
                     datas['VisaValidity']=""
                  if data['details'][0]['visa_expiry_date']:
                     datas['VisaCategory']=data['details'][0]['visa_expiry_date']
                  else:
                     datas['VisaCategory']=""
                  if data['details'][0]['agenda']:
                     datas['DayWiseAgenda']=data['details'][0]['agenda']
                  else:
                     datas['DayWiseAgenda']=""
                  if data['details'][0]['applicable_visa']:
                     datas['VisaType']=data['details'][0]['applicable_visa']
                  else:
                     datas['VisaType']=""
               datas['VisaCountry']=data['Host_Country']
               datas['HostCountry']=data['Host_Country'] 
               datas['HomeCountry']= data['Home_Country']
               if data['emp_passport']:
                  if data['emp_passport'][0]['passort_number']:
                     datas['PassportNo']=data['emp_passport'][0]['passort_number']
                  else:
                     datas['PassportNo']=""
                  if data['emp_passport'][0]['date_of_expiration']:
                     datas['PassportValidity']=data['emp_passport'][0]['date_of_expiration']
                  else:
                     datas['PassportValidity']=""
               if data['travel']:
                  if data['travel'][0]['project_name']:
                     datas['ProjectName']=data['travel'][0]['project_name']
                  else:
                     datas['ProjectName']=""   
                  if data['travel'][0]['project']:
                     datas['ProjectIDWBSECode']=data['travel'][0]['project']
                  else:
                     datas['ProjectIDWBSECode']=""
                  if data['travel'][0]['home_contact_name']:
                     datas['HomeEntityName']=data['travel'][0]['home_contact_name']
                  else:
                     datas['HomeEntityName']=""
            lettername=Letters.objects.filter(letter_type="Visa Letter").values("letter_name")
            lettername=lettername[0]['letter_name'].lstrip('templates/')
            template = get_template(lettername)
            filenames = lettername.rstrip('.html')
            filename = filenames+'.pdf'
            #print(template)
            html = template.render(datas)
            result = BytesIO()
            file = open("uploadpdf/"+filename, "w+b")
            #current_url = request.path_info
            #print(current_url)
            emp_codess="vikasy@triazinesoft.com"
            pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
            email = EmailMessage(subject='Visa Letter',
                                 body='Please Find the attachment report Below',
                                 from_email='vikasy@triazinesoft.com',
                                 to=[emp_code,'vikasy@triazinesoft.com'],
                                 headers = {'Reply-To': 'vikasy@triazinesoft.com'})

            # Open PDF file
            attachment = open('uploadpdf/'+filename, 'rb')

            # Attach PDF file
            email.attach(filename,attachment.read(),'application/pdf')

            # Send message with built-in send() method
            email.send()
            dict = {'massage': 'data found', 'status': True, 'data': 'uploadpdf/'+filename }
        else:
            dict = {'massage': 'data not found', 'status': False}
        #dict = {'massage': 'data found', 'status': True, 'data': travel_request_serializer.data[0] }
        return Response(dict, status=status.HTTP_200_OK)




class assignmentletterkeys(APIView):

    def get(self,request, *args, **kwargs):
        
        datas=['AssigneeName',
                'JobTitle',
                'TodayDate',
                'AssignmentStartDate'	,
                'AssignmentEndDate',	
                'AssignmentType',
                'TravelID',
                'EmployeeID',
                'ClientName',
                'ProjectName',
                'ProjectIDWBSECode',
                'ProjectContact',
                'HostCountry',	
                'HostCity',
                'HostEntityName',
                'HostContactName',
                'HostContactPhoneNumber',
                'HomeCountry',
                'HomeEntityName',	
                'PassportValidity',
                'Citizenship',
                'VisaCategory',
                'VisaNumber',
                'VisaCountry',	
                'VisaValidity',
                'DayWiseAgenda',
                'PassportNo',
                'Nationality',
                'DateofBirth',
                'DateofIssue',
                'DateofExpiration',
                'PlaceofIssue',
                'GrossBaseSalary',
                'EquityIncome',
                'MeritBonus',
                'PreMoveTrip',
                'TemporaryLivinginHostCountry',
                'RelocationAllowance',
                'StartUpAllowance',
                'CostofLivingAllowance',
                'HardshipAllowance',
                'HostHousingAllowance',
                'SchoolTuitionSelf',]
        datass=['Long Term Assignment','Medium Term Assignment','Short Term Assignment','Permanent Transfer','Invite','Visa','Business Travel']
        dict = {'massage': 'data found', 'status': True,'Data':datas,'DataType':datass}
        return Response(dict, status=status.HTTP_200_OK)



class uploadletters(APIView):

    def get(self,request, *args, **kwargs):
        lettername=Letters.objects.all()
        serilaizer=LettersSerializers(lettername,many=True)
        dict = {'massage': 'data found', 'status': True,'Data':serilaizer.data}
        return Response(dict, status=status.HTTP_200_OK)
    def post(self,request, *args, **kwargs):
        lettername=Letters.objects.filter(letter_type=request.data['letter_type'],letter_term=request.data['letter_term'],country=request.data['country'],organization=request.data['organization']).first()
        if lettername:
            lettername.delete()
            serilaizer=LettersSerializers(lettername,data=request.data)
            if serilaizer.is_valid():
                serilaizer.save()
                dict = {'massage': 'data found', 'status': True,'Data':serilaizer.data}
            else:
                dict = {'massage': 'data found', 'status': True,'Data':serilaizer.errors}
        else:
            serilaizer=LettersSerializers(data=request.data)
            if serilaizer.is_valid():
                serilaizer.save()
                dict = {'massage': 'data found', 'status': True,'Data':serilaizer.data}
            else:
                dict = {'massage': 'data found', 'status': True,'Data':serilaizer.errors}
        #dict = {'massage': 'data found', 'status': True, 'data': travel_request_serializer.data[0] }
        return Response(dict, status=status.HTTP_200_OK)

class getSavedTemplate(APIView):
    def get(self,request, *args, **kwargs):
        lettername=Letters.objects.filter(letter_type=request.GET['letter_type'],letter_term=request.GET['letter_term'],country=request.GET['country'],organization=request.GET['organization'])
        serilaizer=LettersSerializers(lettername,many=True)
        dict = {'massage': 'data found', 'status': True,'Data':serilaizer.data}
        return Response(dict, status=status.HTTP_200_OK)