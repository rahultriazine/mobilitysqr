# Generated by Django 2.1 on 2021-07-13 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0003_vendor_service_list_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor_service_list',
            name='test',
        ),
    ]
