# Generated by Django 2.1 on 2021-07-13 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0002_auto_20210713_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_service_list',
            name='test',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
