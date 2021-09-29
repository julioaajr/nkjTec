from django.db import models
from users.models import User

# Create your models here.

class Procedure(models.Model):
    # 'procedure_id', 'name', 'active', 'time', 'price'
    procedure_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Nome")
    active = models.BooleanField(default=True, verbose_name="Ativo")
    time = models.IntegerField(blank=True, null=True, verbose_name="Tempo")
    price = models.FloatField(blank=True, null=True,default= 0, verbose_name="Preço")

    # DESCRICAO
    def __str__(self):
        return self.name


class Status(models.Model):
    #['name','active']
    status_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Nome")
    active = models.BooleanField(default=True, verbose_name="Ativo")

    def __str__(self):
        return self.name


class Payment(models.Model):
    # 'payment_id', 'name', 'active', 'discount','tax'
    payment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Nome")
    active = models.BooleanField(default=True, verbose_name="Ativo")
    discount = models.FloatField(blank=True, null=True, verbose_name="Desconto")
    tax = models.FloatField(blank=True, null=True, verbose_name="Acréscimo")

    def __str__(self):
        return self.name


class BugBounty(models.Model):
    # 'bug_id', 'name', 'content', 'solved', 'created_at', 'description'
    bug_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Nome")
    subject = models.CharField(max_length=255, verbose_name="Assunto")
    solved = models.BooleanField(default=False, verbose_name="Resolvido")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Criado em")
    description = models.TextField(verbose_name="Descrição")

    # DESCRICAO
    def __str__(self):
        return self.name

class Appointment(models.Model):
    #['client','professional','status','procedure','payment' ]
    client = models.ForeignKey(User, models.DO_NOTHING, related_name="clientss", verbose_name="Cliente")
    professional = models.ForeignKey(User, models.DO_NOTHING, related_name="professionalss", verbose_name="Profissional")
    status = models.ForeignKey(Status, models.DO_NOTHING, verbose_name="Status")
    procedure = models.ForeignKey(Procedure, models.DO_NOTHING, verbose_name="Procedimento")
    payment = models.ForeignKey(Payment, models.DO_NOTHING, verbose_name="Pagamento")
    appdate = models.CharField(max_length=10, verbose_name="Data")#format dd/mm/yyyy
    apphour = models.CharField(max_length=5, verbose_name="Horário")#format hh:mm
    total = models.IntegerField(blank = True, null = True, verbose_name="Total")
    active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Criado em")
    def __str__(self):
        return str(self.apphour)
        

    def get_apphour(self):
        return self.__apphour
        


class Schedule(models.Model):
    WEEKDAY = (
        ('0', 'Domingo'),
        ('1', 'Segunda-feira'),
        ('2', 'Terça-feira'),
        ('3', 'Quarta-feira'),
        ('4', 'Quinta-feira'),
        ('5', 'Sexta-feira'),
        ('6', 'Sábado'),
    ) #0 = monday
    weekday = models.CharField(max_length=1, choices=WEEKDAY,default=0, verbose_name="Dia da Semana")
    professional = models.ForeignKey(User, models.DO_NOTHING, verbose_name="Profissional")
    begin = models.CharField(max_length=5, verbose_name="Inicio do Atendimento")#format hh:mm
    end = models.CharField(max_length=5, verbose_name="Final do Atendimento")#format hh:mm
    interval = models.IntegerField(verbose_name="Intervalo(minutos)") #in minutes ex 10
    active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Criado em")
    def __str__(self):
        return "Begin: " + self.begin +"\nEnd: " + self.end+"\nInterval: " + str(self.interval)


class DayOff (models.Model):
    professional = models.ForeignKey(User, models.DO_NOTHING, blank = True, null = True, verbose_name="Profissional")
    daydate = models.CharField(max_length=10, verbose_name="Data do Feriado")#format dd/mm/yyyy
    reason = models.CharField(max_length=255, verbose_name="Motivo")
    active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Criado em.")