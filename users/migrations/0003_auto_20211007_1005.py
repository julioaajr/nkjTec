# Generated by Django 3.2.7 on 2021-10-07 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_empresa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='empresa',
        ),
        migrations.AddField(
            model_name='user',
            name='client',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='master',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='professional',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
