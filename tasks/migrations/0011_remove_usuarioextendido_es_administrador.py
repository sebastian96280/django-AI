# Generated by Django 5.0.3 on 2024-03-21 00:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_remove_usuarioextendido_correo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuarioextendido',
            name='es_administrador',
        ),
    ]
