# Generated by Django 3.2.7 on 2021-11-18 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0007_alter_appointment_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='payed',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Pago'),
        ),
    ]