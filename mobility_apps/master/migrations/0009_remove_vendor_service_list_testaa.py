# Generated by Django 2.1 on 2021-07-13 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0008_vendor_service_list_testaa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor_service_list',
            name='testaa',
        ),
    ]