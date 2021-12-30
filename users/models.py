####----------------- MODELS.PY -----------------
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions.text import Upper
# Create your models here.

class User(AbstractUser):
    pass
    client = models.BooleanField(blank=True, null=True, default=False)
    tel = models.CharField(max_length=11, blank=True,null=True, verbose_name="Telefone")
    professional = models.BooleanField(default=False)
    master = models.ForeignKey('User', blank=True,null=True, on_delete=models.PROTECT)
    nickname = models.CharField(max_length=20, blank=True,null=True, verbose_name="Apelido")
    link = models.CharField(max_length=255, blank=True,null=True, verbose_name="Telefone")

    def __str__(self):
        return (f"{self.first_name} | {self.nickname}")

    class Meta:
        ordering = [Upper('first_name')]