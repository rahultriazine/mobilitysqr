from django.db import models
from django.utils import timezone


# Create your models here.

class IDModel(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class TimeStampedModel(IDModel):
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class GeneratedByModel(models.Model):
    created_by = models.CharField(max_length=100, null=True,default="system")
    modified_by = models.CharField(max_length=100, null=True,default="system")

    class Meta:
        abstract = True


class Status(models.Model):
    status = models.BooleanField(default=False)

    class Meta:
        abstract = True





