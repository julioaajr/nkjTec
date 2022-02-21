# Generated by Django 3.2.7 on 2022-02-21 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0026_appointment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Total'),
        ),
    ]
