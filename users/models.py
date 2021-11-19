####----------------- MODELS.PY -----------------
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class User(AbstractUser):
    pass
    client = models.BooleanField(blank=True, null=True, default=False)
    tel = models.CharField(max_length=11, blank=True,null=True, verbose_name="Telefone")
    professional = models.BooleanField(default=False)
    master = models.ForeignKey('User', blank=True,null=True, on_delete=models.PROTECT)

    