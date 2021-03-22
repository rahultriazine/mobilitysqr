from django.db import models
from mobility_apps.employee.models import *
from django.utils.translation import ugettext_lazy as _

# Create your models here.



class Vault_type(TimeStampedModel, GeneratedByModel, Status):
    vault_id = models.CharField(max_length=100, unique=True)
    vault_type = models.CharField(max_length=100, unique=True)
    vault_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Vault Type')
        verbose_name_plural = _('Vault Type')

    def __str__(self):
        return self.vault_id

    def __unicode__(self):
        return self.vault_id


class Vault_type_info(TimeStampedModel, GeneratedByModel, Status):
    emp_code = models.ForeignKey(Employee,to_field='emp_code', default="emp001", on_delete=models.CASCADE)
    vault_type = models.ForeignKey(Vault_type,to_field='vault_id', null=True, blank=True, on_delete=models.CASCADE)
    doc_name = models.CharField(max_length=100, null=True, blank=True)
    doc_description = models.CharField(max_length=250, null=True, blank=True)
    document_url = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        managed = True
        verbose_name = _('Vault Type Info')
        verbose_name_plural = _('Vault Type Info')

    def __str__(self):
        return self.emp_code

    def __unicode__(self):
        return self.emp_code