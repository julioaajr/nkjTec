# Generated by Django 3.2.7 on 2022-02-23 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='access_schedules',
            field=models.IntegerField(default=0, verbose_name='Acesso ao Link das Agendas Online'),
        ),
    ]
