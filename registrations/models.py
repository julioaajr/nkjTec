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
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    # 'payment_id', 'name', 'active', 'discount','tax'
    payment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    discount = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class BugBounty(models.Model):
    # 'bug_id', 'name', 'content', 'solved', 'created_at', 'description'
    bug_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    solved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    description = models.TextField()

    # DESCRICAO
    def __str__(self):
        return self.name

class Appointment(models.Model):
    #['client','professional','status','procedure','payment' ]
    client = models.ForeignKey(User, models.DO_NOTHING, related_name="clientss")
    professional = models.ForeignKey(User, models.DO_NOTHING, related_name="professionalss")
    status = models.ForeignKey(Status, models.DO_NOTHING)
    procedure = models.ForeignKey(Procedure, models.DO_NOTHING)
    payment = models.ForeignKey(Payment, models.DO_NOTHING)
    appdate = models.CharField(max_length=10)#format dd/mm/yyyy
    apphour = models.CharField(max_length=5)#format hh:mm
    total = models.IntegerField(blank = True, null = True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.apphour)
        

    def get_apphour(self):
        return self.__apphour
        


class Schedule(models.Model):
    professional = models.ForeignKey(User, models.DO_NOTHING)
    begin = models.CharField(max_length=5)#format hh:mm
    end = models.CharField(max_length=5)#format hh:mm
    interval = models.IntegerField() #in minutes ex 10
    weekday = models.IntegerField() #0 = monday
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "Begin: " + self.begin +"\nEnd: " + self.end+"\nInterval: " + str(self.interval)


class DayOff (models.Model):
    professional = models.ForeignKey(User, models.DO_NOTHING, blank = True, null = True)
    daydate = models.CharField(max_length=10)#format dd/mm/yyyy
    reason = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)