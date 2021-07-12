from rest_framework import status
from rest_framework import settings
from mobility_apps.master.models import Vendor
from mobility_apps.employee.models import Employee,Message_Chat
from django.core.mail import send_mail
from datetime import date
from datetime import datetime, timedelta
from rest_framework.response import Response
from django.conf import settings
from celery import shared_task


@shared_task
def send_mailChatEveryDay():
    today = date.today()
    yesterday = today - timedelta(days=1)
    print(yesterday)
    dicts = []
    tick_data = Message_Chat.objects.filter(created_date__startswith=today).values('ticket_id').distinct()
    if tick_data:
        for tic_data in tick_data:
            tic_id = tic_data['ticket_id']
            thred = Message_Chat.objects.filter(created_date__startswith=today, ticket_id=tic_id).values('thread',
                                                                                                         'sender_emp_code',
                                                                          'receiver_emp_code').distinct()
            for thr in thred:
                thr_id = thr['thread']
                sender_email = str(getEmailFrom_Emp(thr['sender_emp_code']))
                receiver_email = str(getEmailFrom_Emp(thr['receiver_emp_code']))
                message_query = Message_Chat.objects.filter(thread=thr_id, created_date__startswith=today).order_by(
                    'created_date')
                print(sender_email, thr['sender_emp_code'])
                print(receiver_email, thr['receiver_emp_code'])
                recipient_list = [sender_email, receiver_email]
                ticket = tic_id
                html_message = ''
                for chat_data in message_query:
                    html_message += '<p>' + str(chat_data.chat_message) + '</p>'
                    html_message += '<p>' + str(chat_data.created_date) + '</p>'
                    html_message += '<p>' + 'From: ' + sender_email + '</p>'
                    html_message += '<p>' + 'To: ' + receiver_email + '</p>'
                    html_message += '<p>---------------------------------</br></p>'
                result = chatMailSend(html_message, recipient_list, ticket)
                if result:
                    dict = {'massage': 'Send mail', 'status': True, 'data': sender_email + '/' + receiver_email}
                else:
                    dict = {'massage': 'send mail failed', 'status': False, 'data': sender_email + '/' + receiver_email}
                dicts.append(dict)
    return dicts



def getEmailFrom_Emp(emp_code):
    personid = Employee.objects.filter(emp_code=emp_code).values('email').first()
    if personid:
        return personid['email']
    else:
        vendor = Vendor.objects.filter(vendor_id=emp_code).values('vendor_email').first()
        return vendor['vendor_email']



def chatMailSend(html_message,recipient_list,ticket):
    subject = 'Chat message for Ticket' + ticket
    message = ''
    # html_message = '<h3>Your New Password:</h3>'
    # html_message += '<p> Username <b>: ' + usename_['user_name'] + '</b> </p>'
    # html_message += '<p>Temporary Password : <b>' + password + '</b> </p>'
    email_from = settings.EMAIL_HOST_USER
    # recipient_list = [request.data['email'], ]
    sentemail = send_mail(subject, message, email_from, recipient_list, fail_silently=False, html_message=html_message)
    if sentemail:
        return True
    else:
        return False