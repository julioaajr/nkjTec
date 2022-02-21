# Generated by Django 3.2.7 on 2022-02-21 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20220221_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_nome',
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome Completo'),
        ),
    ]
