# Generated by Django 4.0.3 on 2023-07-29 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0030_appointment_appbegin_appointment_append'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procedure',
            name='price',
            field=models.FloatField(default=0, verbose_name='Preço R$'),
        ),
    ]
