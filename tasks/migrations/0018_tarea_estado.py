# Generated by Django 5.0.3 on 2024-04-05 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0017_ttipo_solicitud_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarea',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]
