# Generated by Django 2.1 on 2021-07-15 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0007_auto_20210715_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment_travel_request_status',
            name='capital_gains_amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assignment_travel_request_status',
            name='capital_gains_owner',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assignment_travel_request_status',
            name='dividend_income_amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assignment_travel_request_status',
            name='dividend_income_owner',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assignment_travel_request_status',
            name='employment_income_amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assignment_travel_request_status',
            name='employment_income_owner',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assignment_travel_request_status',
            name='income_from_partnership_amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assignment_travel_request_status',
            name='income_from_partnership_owner',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assignment_travel_request_status',
            name='interest_income_amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assignment_travel_request_status',
            name='interest_income_owner',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assignment_travel_request_status',
            name='rent_and_royalty_income_amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assignment_travel_request_status',
            name='rent_and_royalty_income_owner',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assignment_travel_request_status',
            name='retirement_income_amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assignment_travel_request_status',
            name='retirement_income_owner',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assignment_travel_request_status',
            name='self_employment_income_amount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assignment_travel_request_status',
            name='self_employment_income_owner',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='assignment_travel_request_status',
            name='file_attachments',
            field=models.TextField(blank=True, null=True),
        ),
    ]
