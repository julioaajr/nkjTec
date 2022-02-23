from django.db import models
from django.db.models.functions.text import Upper
from users.models import User

# Create your models here.

class Procedure(models.Model):
    # 'procedure_id', 'name', 'active', 'time', 'price'
    procedure_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Nome do Procedimento")
    active = models.BooleanField(default=True, verbose_name="Ativo")
    time = models.IntegerField(blank=True, null=True, verbose_name="Tempo (minutos)")
    price = models.FloatField(blank=True, null=True, verbose_name="Preço R$")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    master = models.ForeignKey(User, models.DO_NOTHING, blank = True, null = True, related_name="mastersprocedure", verbose_name="Master")
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank = True, null = True, related_name="createdbyprocedure", verbose_name="Criado por")

    def __str__(self):
        return f"{self.name} | R$ {self.price}"


class Client (models.Model):
    
    name = models.CharField(max_length=255, verbose_name="Nome")
    tel = models.CharField(max_length=11, verbose_name="Telefone")
    cpf = models.CharField(null= True, blank=True,max_length=14, verbose_name="CPF")
    email = models.CharField(null= True, blank=True, max_length=60, verbose_name="E-mail")
    obs = models.TextField(null=True,blank=True, verbose_name="Obervações")
    birth = models.CharField(null=True,blank=True, max_length=10, verbose_name="Data de nascimento")#format dd/mm/yyyy
    created_at = models.DateTimeField(auto_now=True, verbose_name="Criado em.")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    master = models.ForeignKey(User, models.DO_NOTHING, blank = True, null = True, related_name="masterclient", verbose_name="Master")
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank = True, null = True, related_name="createdbyclient", verbose_name="Criado por")

    def __str__(self):
        return f"{self.name} | {self.tel}"

    class Meta:
        ordering = [Upper('name')]


class Appointment(models.Model):
    PAYED = (
        ('N', 'Não'),
        ('S', 'Sim'),
    )
    STATUS = (
        ('0', 'Não Confirmado'),
        ('1', 'Confirmado'),
        ('2', 'Esperando'),
        ('3', 'Em Atendimento'),
        ('4', 'Atendido'),
        ('5', 'Faltou'),
        ('6', 'Cancelado'),
        ('7', 'Remarcado'),
    )
    #['client','professional','status','procedure','payment' ]
    client = models.ForeignKey(Client, models.DO_NOTHING, related_name="clientss", verbose_name="Cliente")
    professional = models.ForeignKey(User, models.DO_NOTHING, related_name="professionalss", verbose_name="Profissional")
    status = models.CharField(max_length=1, choices=STATUS,default=0, verbose_name="Status do Agendamento")
    procedure = models.ForeignKey(Procedure, models.DO_NOTHING, verbose_name="Procedimento")
    payed = models.CharField(max_length=1, choices=PAYED,default='N', verbose_name="Pago")
    appdate = models.CharField(max_length=10, verbose_name="Data")#format dd/mm/yyyy
    apphour = models.CharField(max_length=5, verbose_name="Horário")#format hh:mm
    total = models.DecimalField(decimal_places=2,max_digits=4, blank = True, null = True, verbose_name="Total")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Criado em")
    master = models.ForeignKey(User, models.DO_NOTHING, blank = True, null = True, related_name="masterappointment", verbose_name="Master")
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank = True, null = True, related_name="createdbyappointmen", verbose_name="Criado por")
    date = models.DateField(null=True,blank=True)
    def __str__(self):
        return (f"Nome: {self.client} | Data: {self.appdate} | Horário: {self.apphour} | Date: {self.date}")


    def get_apphour(self):
        return self.__apphour
        

class Schedule(models.Model):
    SHARED = (
        ('N', 'Não'),
        ('S', 'Sim'),
    )
    WEEKDAY = (
        ('0', 'Segunda-feira'),
        ('1', 'Terça-feira'),
        ('2', 'Quarta-feira'),
        ('3', 'Quinta-feira'),
        ('4', 'Sexta-feira'),
        ('5', 'Sábado'),
        ('6', 'Domingo'),
    ) #0 = monday
    weekday = models.CharField(max_length=1, choices=WEEKDAY,default=0, verbose_name="Dia da Semana")
    professional = models.ForeignKey(User, models.DO_NOTHING, verbose_name="Profissional")
    begin = models.CharField(max_length=5, verbose_name="Inicio do Atendimento")#format hh:mm
    end = models.CharField(max_length=5, verbose_name="Final do Atendimento")#format hh:mm
    interval = models.IntegerField(verbose_name="Intervalo(minutos)") #in minutes ex 10
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Criado em")
    master = models.ForeignKey(User, models.DO_NOTHING, blank = True, null = True, related_name="masterschedule", verbose_name="Master")
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank = True, null = True, related_name="createdbyschedule", verbose_name="Criado por")
    is_shared = models.CharField(max_length=1, choices=SHARED,default='S', verbose_name="Compartilhar na Agenda Online")

    def __str__(self):
        return f"Profissional: {self.professional.first_name} Begin: {self.begin} \nEnd: {self.end} \nInterval: " + str(self.interval)


class DayOff (models.Model):
    professional = models.ForeignKey(User, models.DO_NOTHING, blank = True, null = True, verbose_name="Profissional")
    daydate = models.CharField(max_length=10, verbose_name="Data do Feriado")#format dd/mm/yyyy
    reason = models.CharField(max_length=255, verbose_name="Motivo")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Criado em.")
    master = models.ForeignKey(User, models.DO_NOTHING, blank = True, null = True, related_name="masterdayoff", verbose_name="Master")
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank = True, null = True, related_name="createdbydayoff", verbose_name="Criado por")

    def __str__(self):
        if self.professional:
            return f"PROFISSIONAL: {self.professional.first_name} DATA: {self.daydate} | MOTIVO: {self.reason}"
        return f"DATA: {self.daydate} | MOTIVO: {self.reason}"



