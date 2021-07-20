# Generated by Django 2.1 on 2021-07-20 15:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0001_initial'),
        ('employee', '0006_remove_employee_vaccine_name'),
        ('travel', '0008_auto_20210715_1910'),
        ('master', '0017_auto_20210720_1504'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor_Authorized_Service_List',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default='system', max_length=100, null=True)),
                ('modified_by', models.CharField(default='system', max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('services', models.CharField(blank=True, max_length=200, null=True)),
                ('authorization', models.BooleanField(default=False)),
                ('home_completed', models.BooleanField(default=False)),
                ('host_completed', models.BooleanField(default=False)),
                ('completion_date', models.CharField(blank=True, max_length=100, null=True)),
                ('home_tax_year', models.CharField(blank=True, max_length=100, null=True)),
                ('host_tax_year', models.CharField(blank=True, max_length=100, null=True)),
                ('validity', models.CharField(blank=True, max_length=100, null=True)),
                ('emp_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', to_field='emp_code')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='superadmin.Organizations', to_field='org_id')),
                ('travel_req', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='travel.Travel_Request', to_field='travel_req_id')),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='master.Vendor', to_field='vendor_id')),
            ],
            options={
                'verbose_name': 'Vendor Authorized Service List',
                'verbose_name_plural': 'Vendor Authorized Service List',
                'managed': True,
            },
        ),
    ]
