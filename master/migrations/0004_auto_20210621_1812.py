# Generated by Django 2.2 on 2021-06-21 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0003_auto_20210621_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_master',
            name='vendor_id',
            field=models.IntegerField(max_length=100, unique=True),
        ),
    ]
