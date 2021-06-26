# Generated by Django 2.1 on 2021-06-09 14:46

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('superadmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calender_Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_name', models.CharField(blank=True, max_length=100, null=True)),
                ('activity_sort_name', models.CharField(blank=True, max_length=100, null=True)),
                ('is_visible', models.CharField(default=True, max_length=50)),
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
            ],
            options={
                'verbose_name': 'Calender Activity',
                'verbose_name_plural': 'Calender Activity',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Calender_Events',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default='system', max_length=100, null=True)),
                ('modified_by', models.CharField(default='system', max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('from_date', models.CharField(blank=True, max_length=50, null=True)),
                ('to_date', models.CharField(blank=True, max_length=50, null=True)),
                ('country_code', models.CharField(blank=True, max_length=50, null=True)),
                ('country_name', models.CharField(blank=True, max_length=100, null=True)),
                ('city_code', models.CharField(blank=True, max_length=50, null=True)),
                ('city_name', models.CharField(blank=True, max_length=100, null=True)),
                ('activity', models.CharField(blank=True, max_length=100, null=True)),
                ('is_visible', models.CharField(default=True, max_length=50)),
                ('is_deleted', models.CharField(default=False, max_length=50)),
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
            ],
            options={
                'verbose_name': 'Calender Events',
                'verbose_name_plural': 'Calender Events',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default='system', max_length=100, null=True)),
                ('modified_by', models.CharField(default='system', max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('emp_code', models.CharField(default='emp001', max_length=50, unique=True)),
                ('person_id', models.CharField(max_length=50)),
                ('login_method', models.CharField(blank=True, max_length=100, null=True)),
                ('termandcondtion', models.CharField(blank=True, max_length=100, null=True)),
                ('istemporary', models.CharField(blank=True, max_length=100, null=True)),
                ('user_name', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('preferred_first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('preferred_last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('salutation', models.CharField(blank=True, max_length=100, null=True)),
                ('initials', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('suffix', models.CharField(blank=True, max_length=100, null=True)),
                ('display_name', models.CharField(blank=True, max_length=100, null=True)),
                ('formal_name', models.CharField(blank=True, max_length=100, null=True)),
                ('birth_name', models.CharField(blank=True, max_length=100, null=True)),
                ('name_prefix', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(blank=True, max_length=100, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=100, null=True)),
                ('marital_status_since', models.CharField(blank=True, max_length=100, null=True)),
                ('country_of_birth', models.CharField(blank=True, max_length=100, null=True)),
                ('nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('second_nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('native_preferred_lang', models.CharField(blank=True, max_length=100, null=True)),
                ('partner_name', models.CharField(blank=True, max_length=100, null=True)),
                ('partner_name_prefix', models.CharField(blank=True, max_length=100, null=True)),
                ('note', models.CharField(blank=True, max_length=100, null=True)),
                ('dob', models.CharField(blank=True, max_length=100, null=True)),
                ('place_of_birth', models.CharField(blank=True, max_length=100, null=True)),
                ('active_start_date', models.CharField(blank=True, default='', max_length=100)),
                ('active_end_date', models.CharField(blank=True, default='', max_length=100)),
                ('email', models.EmailField(blank=True, max_length=100, null=True, unique=True)),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('role', models.CharField(blank=True, max_length=100, null=True)),
                ('photo', models.CharField(blank=True, max_length=255, null=True)),
                ('assignment_role', models.CharField(blank=True, max_length=100, null=True)),
                ('organization', models.CharField(blank=True, max_length=100, null=True)),
                ('supervisor', models.CharField(blank=True, default='demo_supervisor_1', max_length=100)),
                ('last_login', models.CharField(blank=True, max_length=100, null=True)),
                ('recent_login', models.CharField(blank=True, max_length=100, null=True)),
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
                ('is_visa_denied', models.BooleanField(default=False)),
                ('visa_denied_country', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_join', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employee',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Employee_Address',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default='system', max_length=100, null=True)),
                ('modified_by', models.CharField(default='system', max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('address1', models.CharField(blank=True, max_length=100, null=True)),
                ('address2', models.CharField(blank=True, max_length=100, null=True)),
                ('address3', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('address_type', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('is_primary', models.BooleanField(default=False)),
                ('zip', models.CharField(blank=True, max_length=100, null=True)),
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
                ('emp_code', models.ForeignKey(default='emp001', on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', to_field='emp_code')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='superadmin.Organizations', to_field='org_id')),
            ],
            options={
                'verbose_name': 'Employee Address',
                'verbose_name_plural': 'Employee Address',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Employee_Emails',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default='system', max_length=100, null=True)),
                ('modified_by', models.CharField(default='system', max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('email_type', models.CharField(blank=True, max_length=100, null=True)),
                ('email_address', models.EmailField(max_length=100, unique=True)),
                ('isPrimary', models.BooleanField(default=False)),
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
                ('emp_code', models.ForeignKey(default='emp001', on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', to_field='emp_code')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='superadmin.Organizations', to_field='org_id')),
            ],
            options={
                'verbose_name': 'Employee Emails',
                'verbose_name_plural': 'Employee Emails',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Employee_Emergency_Contact',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default='system', max_length=100, null=True)),
                ('modified_by', models.CharField(default='system', max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('relationship', models.CharField(blank=True, max_length=100, null=True)),
                ('primary_flag', models.BooleanField(default=False)),
                ('country_code', models.CharField(blank=True, max_length=100, null=True)),
                ('second_country_code', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('second_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('isDependent', models.BooleanField(default=False)),
                ('isEmergencyContact', models.BooleanField(default=False)),
                ('gender', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('isAddSameAsEmployee', models.BooleanField(default=False)),
                ('address1', models.CharField(blank=True, max_length=100, null=True)),
                ('address2', models.CharField(blank=True, max_length=100, null=True)),
                ('address3', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('address_type', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('zip', models.CharField(blank=True, max_length=100, null=True)),
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
                ('emp_code', models.ForeignKey(default='emp001', on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', to_field='emp_code')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='superadmin.Organizations', to_field='org_id')),
            ],
            options={
                'verbose_name': 'Employee Emergency Contact',
                'verbose_name_plural': 'Employee Emergency Contact',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Employee_Nationalid',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default='system', max_length=100, null=True)),
                ('modified_by', models.CharField(default='system', max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('country_code', models.CharField(blank=True, max_length=100, null=True)),
                ('card_type', models.CharField(blank=True, max_length=100, null=True)),
                ('national_id', models.CharField(blank=True, max_length=100, null=True)),
                ('attachment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('isprimary', models.BooleanField(default=False)),
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
                ('emp_code', models.ForeignKey(default='emp001', on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', to_field='emp_code')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='superadmin.Organizations', to_field='org_id')),
            ],
            options={
                'verbose_name': 'Employee Nationalid',
                'verbose_name_plural': 'Employee Nationalid',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Employee_Org_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org1', models.CharField(blank=True, max_length=100, null=True)),
                ('org2', models.CharField(blank=True, max_length=100, null=True)),
                ('org3', models.CharField(blank=True, max_length=100, null=True)),
                ('org1ID', models.CharField(blank=True, max_length=100, null=True)),
                ('org2ID', models.CharField(blank=True, max_length=100, null=True)),
                ('org3ID', models.CharField(blank=True, max_length=100, null=True)),
                ('home_office_location', models.CharField(blank=True, max_length=100, null=True)),
                ('host_office_location', models.CharField(blank=True, max_length=100, null=True)),
                ('client_office_location', models.CharField(blank=True, max_length=100, null=True)),
                ('home_country_designation', models.CharField(blank=True, max_length=100, null=True)),
                ('host_country_designation', models.CharField(blank=True, max_length=100, null=True)),
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
                ('current_working_country', models.CharField(blank=True, max_length=100, null=True)),
                ('current_working_city', models.CharField(blank=True, max_length=100, null=True)),
                ('home_country_band', models.CharField(blank=True, max_length=100, null=True)),
                ('host_country_band', models.CharField(blank=True, max_length=100, null=True)),
                ('emp_code', models.ForeignKey(default='emp001', on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', to_field='emp_code')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='superadmin.Organizations', to_field='org_id')),
            ],
            options={
                'verbose_name': 'Employee Visa Detail',
                'verbose_name_plural': 'Employee Visa Detail',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Employee_Passport_Detail',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default='system', max_length=100, null=True)),
                ('modified_by', models.CharField(default='system', max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('passport_status', models.BooleanField(default=False)),
                ('passport_number', models.CharField(blank=True, max_length=20, null=True)),
                ('passport_expiry_date', models.CharField(blank=True, max_length=50, null=True)),
                ('isdependent', models.BooleanField(default=False)),
                ('relation', models.CharField(blank=True, max_length=50, null=True)),
                ('nationality', models.CharField(blank=True, max_length=50, null=True)),
                ('country_of_issue', models.CharField(blank=True, max_length=50, null=True)),
                ('place_of_issue', models.CharField(blank=True, max_length=50, null=True)),
                ('date_of_issue', models.CharField(blank=True, max_length=50, null=True)),
                ('date_of_expiration', models.CharField(blank=True, max_length=50, null=True)),
                ('duplicate_passport', models.BooleanField(default=False)),
                ('pages_passport', models.CharField(blank=True, max_length=50, null=True)),
                ('photo', models.CharField(blank=True, max_length=255, null=True)),
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
                ('emp_code', models.ForeignKey(default='emp001', on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', to_field='emp_code')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='superadmin.Organizations', to_field='org_id')),
            ],
            options={
                'verbose_name': 'Employee Passport Detail',
                'verbose_name_plural': 'Employee Passport Detail',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Employee_Phones',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default='system', max_length=100, null=True)),
                ('modified_by', models.CharField(default='system', max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('phone_type', models.CharField(blank=True, max_length=100, null=True)),
                ('country_code', models.CharField(blank=True, max_length=100, null=True)),
                ('area_code', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('extension', models.CharField(blank=True, max_length=100, null=True)),
                ('isprimary', models.BooleanField(default=False)),
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
                ('emp_code', models.ForeignKey(default='emp001', on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', to_field='emp_code')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='superadmin.Organizations', to_field='org_id')),
            ],
            options={
                'verbose_name': 'Employee Address',
                'verbose_name_plural': 'Employee Address',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Employee_Visa_Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(blank=True, max_length=100, null=True)),
                ('document_type', models.CharField(blank=True, max_length=100, null=True)),
                ('document_title', models.CharField(blank=True, max_length=100, null=True)),
                ('isdependent', models.BooleanField(default=False)),
                ('relation', models.CharField(blank=True, max_length=100, null=True)),
                ('document_number', models.CharField(blank=True, max_length=100, null=True)),
                ('issue_date', models.CharField(blank=True, max_length=100, null=True)),
                ('issue_place', models.CharField(blank=True, max_length=100, null=True)),
                ('issuing_authority', models.CharField(blank=True, max_length=100, null=True)),
                ('expiration_date', models.CharField(blank=True, max_length=100, null=True)),
                ('is_validated', models.BooleanField(default=False)),
                ('valid_from', models.CharField(blank=True, max_length=100, null=True)),
                ('attachment_id', models.CharField(blank=True, max_length=255, null=True)),
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
                ('visa_entry_type', models.CharField(blank=True, max_length=100, null=True)),
                ('emp_code', models.ForeignKey(default='emp001', on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', to_field='emp_code')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='superadmin.Organizations', to_field='org_id')),
            ],
            options={
                'verbose_name': 'Employee Visa Detail',
                'verbose_name_plural': 'Employee Visa Detail',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Message_Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_emp_code', models.CharField(max_length=200, null=True)),
                ('receiver_emp_code', models.CharField(max_length=200, null=True)),
                ('thread', models.CharField(max_length=200, null=True)),
                ('chat_message', models.TextField(max_length=1000, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('ticket_id', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default='system', max_length=100, null=True)),
                ('modified_by', models.CharField(default='system', max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('emp_code', models.CharField(default='emp001', max_length=100, unique=True)),
                ('person_id', models.CharField(max_length=50, unique=True)),
                ('role', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('login_method', models.CharField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('termandcondtion', models.CharField(blank=True, max_length=100, null=True)),
                ('istemporary', models.CharField(blank=True, max_length=100, null=True)),
                ('org_id', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Userinfo',
                'verbose_name_plural': 'Userinfo',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='calender_events',
            name='emp_code',
            field=models.ForeignKey(default='emp001', on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', to_field='emp_code'),
        ),
    ]
