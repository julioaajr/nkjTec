# Generated by Django 3.2.7 on 2022-03-02 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0028_schedule_is_shared'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='total',
            field=models.FloatField(blank=True, null=True, verbose_name='Total'),
        ),
    ]
