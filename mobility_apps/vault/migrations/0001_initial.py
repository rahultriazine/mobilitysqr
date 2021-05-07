# Generated by Django 2.1.15 on 2021-03-25 13:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vault_type',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default='system', max_length=100, null=True)),
                ('modified_by', models.CharField(default='system', max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('vault_id', models.CharField(max_length=100, unique=True)),
                ('vault_type', models.CharField(max_length=100, unique=True)),
                ('vault_name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Vault Type',
                'verbose_name_plural': 'Vault Type',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Vault_type_info',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.CharField(default='system', max_length=100, null=True)),
                ('modified_by', models.CharField(default='system', max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('doc_name', models.CharField(blank=True, max_length=100, null=True)),
                ('doc_description', models.CharField(blank=True, max_length=250, null=True)),
                ('document_url', models.CharField(blank=True, max_length=250, null=True)),
                ('test', models.CharField(blank=True, max_length=250, null=True)),
                ('emp_code', models.ForeignKey(default='emp001', on_delete=django.db.models.deletion.CASCADE, to='employee.Employee', to_field='emp_code')),
                ('vault_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vault.Vault_type', to_field='vault_id')),
            ],
            options={
                'verbose_name': 'Vault Type Info',
                'verbose_name_plural': 'Vault Type Info',
                'managed': True,
            },
        ),
    ]
