# Generated by Django 2.1 on 2021-06-03 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0004_employee_compliance_compl_ques_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='compliance',
            name='compl_ques_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
