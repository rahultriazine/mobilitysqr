# Generated by Django 2.1 on 2021-07-12 11:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0001_initial'),
        ('employee', '0001_initial'),
        ('superadmin', '0001_initial'),
        ('master', '0004_auto_20210712_1713'),
    ]

    operations = [
        migrations.CreateModel(
            name='Capital_Gains_Income',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default='system', max_length=100, null=True)),
                ('modified_by', models.CharField(default='system', max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('company_name', models.CharField(blank=True, max_length=200, null=True)),
                ('class_of_share', models.CharField(blank=True, max_length=100, null=True)),
                ('share_sold', models.CharField(blank=True, choices=[('Tax Payer', 'Tax Payer'), ('Spouse', 'Spouse'), ('Joint', 'Joint')], max_length=100, null=True)),
                ('date_purchased', models.CharField(blank=True, max_length=100, null=True)),
                ('date_sold', models.CharField(blank=True, max_length=100, null=True)),
                ('purchase_price', models.CharField(blank=True, max_length=100, null=True)),
                ('sale_price', models.CharField(blank=True, max_length=100, null=True)),
                ('sale_expenses', models.CharField(blank=True, max_length=100, null=True)),
                ('tex_paid', models.CharField(blank=True, max_length=100, null=True)),
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
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='master.Currency')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.Employee')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='superadmin.Organizations')),
                ('travel_req', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='travel.Travel_Request')),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='master.Vendor')),
            ],
            options={
                'verbose_name': 'company_name',
                'verbose_name_plural': 'company_name',
                'managed': True,
            },
        ),
    ]
