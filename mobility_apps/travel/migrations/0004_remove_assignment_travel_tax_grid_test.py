# Generated by Django 2.1 on 2021-07-13 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0003_assignment_travel_tax_grid_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment_travel_tax_grid',
            name='test',
        ),
    ]
