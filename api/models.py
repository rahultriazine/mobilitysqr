from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.utils.translation import ugettext_lazy as _




class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    otp=models.IntegerField(max_length=50, null=True, blank=True)
    create_time = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    def __str__(self):
        return str(self.email)
