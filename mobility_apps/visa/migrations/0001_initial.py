# Generated by Django 2.1 on 2021-06-09 14:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0001_initial'),
        ('superadmin', '0001_initial'),
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visa_Request',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default='system', max_length=100, null=True)),
                ('modified_by', models.CharField(default='system', max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('visa_req_id', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('travel_req_id', models.CharField(blank=True, max_length=100, null=True)),
                ('req_id', models.CharField(blank=True, max_length=100, null=True)),
                ('project_name', models.CharField(blank=True, max_length=200, null=True)),
                ('is_billable', models.BooleanField(blank=True, default=False)),
                ('is_dependent', models.BooleanField(blank=True, default=False)),
                ('vendor_fees', models.IntegerField(blank=True, null=True)),
                ('govt_fees', models.IntegerField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('dependent_name', models.CharField(blank=True, max_length=100, null=True)),
                ('dependent_relation', models.CharField(blank=True, max_length=100, null=True)),
                ('from_city', models.CharField(blank=True, max_length=100, null=True)),
                ('to_city', models.CharField(blank=True, max_length=100, null=True)),
                ('travel_start_date', models.DateTimeField(blank=True, null=True)),
                ('travel_end_date', models.DateTimeField(blank=True, null=True)),
                ('visa_purpose', models.CharField(blank=True, max_length=100, null=True)),
                ('applied_visa', models.CharField(blank=True, max_length=20, null=True)),
                ('remark', models.CharField(blank=True, max_length=200, null=True)),
                ('request_notes', models.CharField(blank=True, max_length=200, null=True)),
                ('visa_status', models.CharField(blank=True, max_length=50, null=True)),
                ('visa_status_notes', models.CharField(blank=True, max_length=200, null=True)),
                ('current_ticket_owner', models.CharField(blank=True, max_length=100, null=True)),
                ('supervisor', models.CharField(blank=True, max_length=100, null=True)),
                ('expense_approver', models.CharField(blank=True, max_length=100, null=True)),
                ('project_manager', models.CharField(blank=True, max_length=100, null=True)),
                ('business_lead', models.CharField(blank=True, max_length=100, null=True)),
                ('client_executive_lead', models.CharField(blank=True, max_length=100, null=True)),
                ('approval_level', models.CharField(blank=True, max_length=100, null=True)),
                ('column1', models.CharField(blank=True, max_length=100, null=True)),
                ('column2', models.CharField(blank=True, max_length=100, null=True)),
                ('column3', models.CharField(blank=True, max_length=100, null=True)),
                ('column4', models.CharField(blank=True, max_length=100, null=True)),
                ('column5', models.CharField(blank=True, max_length=100, null=True)),
                ('column6', models.CharField(blank=True, max_length=100, null=True)),
                ('column7', models.CharField(blank=True, max_length=100, null=True)),
                ('column8', models.CharField(blank=True, max_length=100, null=True)),
                ('column9', models.CharField(blank=True, max_length=100, null=True)),
                ('column10', models.CharField(blank=True, max_length=100, null=True)),
                ('column11', models.CharField(blank=True, max_length=100, null=True)),
                ('column12', models.CharField(blank=True, max_length=100, null=True)),
                ('emp_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', to_field='emp_code')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='superadmin.Organizations', to_field='org_id')),
                ('project_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='master.Project', to_field='pid')),
            ],
            options={
                'verbose_name': 'Visa Request',
                'verbose_name_plural': 'Visa Request',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Visa_Request_Document',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default='system', max_length=100, null=True)),
                ('modified_by', models.CharField(default='system', max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('req_id', models.CharField(blank=True, max_length=100, null=True)),
                ('uploaded_document_name', models.FileField(max_length=255, null=True, upload_to='visaimage/')),
                ('document_name', models.CharField(blank=True, max_length=100, null=True)),
                ('document_type', models.CharField(blank=True, max_length=100, null=True)),
                ('host_type', models.CharField(blank=True, max_length=100, null=True)),
                ('request_note', models.CharField(blank=True, max_length=100, null=True)),
                ('remark', models.CharField(blank=True, max_length=10, null=True)),
                ('request_status', models.CharField(blank=True, max_length=10, null=True)),
                ('visa_main_id', models.CharField(blank=True, max_length=100, null=True)),
                ('column1', models.CharField(blank=True, max_length=100, null=True)),
                ('column2', models.CharField(blank=True, max_length=100, null=True)),
                ('column3', models.CharField(blank=True, max_length=100, null=True)),
                ('column4', models.CharField(blank=True, max_length=100, null=True)),
                ('column5', models.CharField(blank=True, max_length=100, null=True)),
                ('column6', models.CharField(blank=True, max_length=100, null=True)),
                ('column7', models.CharField(blank=True, max_length=100, null=True)),
                ('column8', models.CharField(blank=True, max_length=100, null=True)),
                ('column9', models.CharField(blank=True, max_length=100, null=True)),
                ('column10', models.CharField(blank=True, max_length=100, null=True)),
                ('column11', models.CharField(blank=True, max_length=100, null=True)),
                ('column12', models.CharField(blank=True, max_length=100, null=True)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='superadmin.Organizations', to_field='org_id')),
                ('visa_request', models.ForeignKey(blank=True, max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='visa_request_document', to='visa.Visa_Request', to_field='visa_req_id')),
            ],
            options={
                'verbose_name': 'Visa Request Document',
                'verbose_name_plural': 'Visa Request Document',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Visa_Request_Document_Draft',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default='system', max_length=100, null=True)),
                ('modified_by', models.CharField(default='system', max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('uploaded_document_name', models.ImageField(max_length=255, null=True, upload_to='visaimage/')),
                ('document_name', models.CharField(blank=True, max_length=100, null=True)),
                ('document_type', models.CharField(blank=True, max_length=100, null=True)),
                ('column1', models.CharField(blank=True, max_length=100, null=True)),
                ('column2', models.CharField(blank=True, max_length=100, null=True)),
                ('column3', models.CharField(blank=True, max_length=100, null=True)),
                ('column4', models.CharField(blank=True, max_length=100, null=True)),
                ('column5', models.CharField(blank=True, max_length=100, null=True)),
                ('column6', models.CharField(blank=True, max_length=100, null=True)),
                ('column7', models.CharField(blank=True, max_length=100, null=True)),
                ('column8', models.CharField(blank=True, max_length=100, null=True)),
                ('column9', models.CharField(blank=True, max_length=100, null=True)),
                ('column10', models.CharField(blank=True, max_length=100, null=True)),
                ('column11', models.CharField(blank=True, max_length=100, null=True)),
                ('column12', models.CharField(blank=True, max_length=100, null=True)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='superadmin.Organizations', to_field='org_id')),
                ('visa_request', models.ForeignKey(blank=True, max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, to='visa.Visa_Request', to_field='visa_req_id')),
            ],
            options={
                'verbose_name': 'Visa Request Document Draft',
                'verbose_name_plural': 'Visa Request Document Draft',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Visa_Request_Draft',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default='system', max_length=100, null=True)),
                ('modified_by', models.CharField(default='system', max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('visa_req_id', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('travel_req_id', models.CharField(blank=True, max_length=100, null=True)),
                ('project_name', models.CharField(blank=True, max_length=200, null=True)),
                ('is_billable', models.BooleanField(blank=True, default=False)),
                ('vendor_fees', models.IntegerField(blank=True, null=True)),
                ('govt_fees', models.IntegerField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('travel_start_date', models.DateTimeField(blank=True, null=True)),
                ('travel_end_date', models.DateTimeField(blank=True, null=True)),
                ('visa_purpose', models.CharField(blank=True, max_length=100, null=True)),
                ('applied_visa', models.CharField(blank=True, max_length=20, null=True)),
                ('request_notes', models.CharField(blank=True, max_length=200, null=True)),
                ('visa_status', models.CharField(blank=True, max_length=50, null=True)),
                ('visa_status_notes', models.CharField(blank=True, max_length=200, null=True)),
                ('column1', models.CharField(blank=True, max_length=100, null=True)),
                ('column2', models.CharField(blank=True, max_length=100, null=True)),
                ('column3', models.CharField(blank=True, max_length=100, null=True)),
                ('column4', models.CharField(blank=True, max_length=100, null=True)),
                ('column5', models.CharField(blank=True, max_length=100, null=True)),
                ('column6', models.CharField(blank=True, max_length=100, null=True)),
                ('column7', models.CharField(blank=True, max_length=100, null=True)),
                ('column8', models.CharField(blank=True, max_length=100, null=True)),
                ('column9', models.CharField(blank=True, max_length=100, null=True)),
                ('column10', models.CharField(blank=True, max_length=100, null=True)),
                ('column11', models.CharField(blank=True, max_length=100, null=True)),
                ('column12', models.CharField(blank=True, max_length=100, null=True)),
                ('emp_email', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', to_field='email')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='superadmin.Organizations', to_field='org_id')),
                ('project_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='master.Project', to_field='pid')),
            ],
            options={
                'verbose_name': 'Visa Request Draft',
                'verbose_name_plural': 'Visa Request Draft',
                'managed': True,
            },
        ),
    ]
