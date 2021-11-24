# Generated by Django 3.2.7 on 2021-11-23 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0009_alter_appointment_payed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('0', 'Não Confirmado'), ('1', 'Confirmado'), ('2', 'Esperando'), ('3', 'Em Atendimento'), ('4', 'Atendido'), ('5', 'Faltou'), ('6', 'Cancelado'), ('7', 'Remarcado')], default=0, max_length=1, verbose_name='Status do Agendamento'),
        ),
    ]