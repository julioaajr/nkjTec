# Generated by Django 3.2.7 on 2022-01-25 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0024_alter_appointment_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='clientss', to='registrations.client', verbose_name='Cliente'),
        ),
    ]
