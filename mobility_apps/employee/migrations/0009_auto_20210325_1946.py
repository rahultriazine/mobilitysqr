# Generated by Django 2.1.15 on 2021-03-25 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_message_column2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='column2',
            new_name='column26',
        ),
    ]
