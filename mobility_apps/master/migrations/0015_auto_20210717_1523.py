# Generated by Django 2.1 on 2021-07-17 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0014_auto_20210717_1446'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vaccine_autho_country',
            old_name='country_code',
            new_name='country_id',
        ),
    ]