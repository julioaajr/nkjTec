# Generated by Django 3.2.7 on 2021-10-07 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='empresa',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, related_name='empresas', to='users.user'),
            preserve_default=False,
        ),
    ]
