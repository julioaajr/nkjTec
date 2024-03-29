####----------------- MODELS.PY -----------------
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions.text import Upper
# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=255, blank=True,null=True, verbose_name="Nome Completo")
    username = models.CharField(max_length=150, unique=True, verbose_name= "CPF / CNPJ (login)")
    tel = models.CharField(max_length=11, blank=True,null=True, verbose_name="Telefone")
    professional = models.BooleanField(default=False,verbose_name="Profissional")
    master = models.ForeignKey('User', blank=True,null=True, on_delete=models.PROTECT)
    nickname = models.CharField(max_length=20, blank=True,null=True, verbose_name="Apelido", unique= True)
    link = models.CharField(max_length=255, blank=True,null=True, verbose_name="Telefone")
    is_master = models.BooleanField(default=False)
    access_schedules = models.IntegerField(default=0, verbose_name="Acesso ao Link das Agendas Online")
    #future_days = models.IntegerField(null = True,blank = True, verbose_name='Quantidade de dias Agenda Cliente')
    def __str__(self):
        return (f"{self.first_name} | {self.nickname}")

    class Meta:
        ordering = [Upper('first_name')]