from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from mobility_apps.base.models import TimeStampedModel, GeneratedByModel, Status


class Letters(TimeStampedModel, GeneratedByModel, Status):
    letter_type = models.CharField(max_length=100)
    letter_name = models.FileField(upload_to='templates/', null=True, max_length=255)
    letter_data = models.TextField(null=True, blank=True)
    letter_term= models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
    column1 = models.CharField(max_length=100, null=True, blank=True)
    column2 = models.CharField(max_length=100, null=True, blank=True)
    column3 = models.CharField(max_length=100, null=True, blank=True)
    column4 = models.CharField(max_length=100, null=True, blank=True)
    column5 = models.CharField(max_length=100, null=True, blank=True)
    column6 = models.CharField(max_length=100, null=True, blank=True)
    column7 = models.CharField(max_length=100, null=True, blank=True)
    column8 = models.CharField(max_length=100, null=True, blank=True)
    column9 = models.CharField(max_length=100, null=True, blank=True)
    column10 = models.CharField(max_length=100, null=True, blank=True)
    column11 = models.CharField(max_length=100, null=True, blank=True)
    column12 = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Letters')
        verbose_name_plural = _('Letters')

    def __str__(self):
        return self.letter_type

    def __unicode__(self):
        return self.letter_type