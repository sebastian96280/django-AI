# Generated by Django 5.0.3 on 2024-03-22 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_tsolicitud_archivo_respuesta_tsolicitud_id_usuario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarioextendido',
            name='cargo',
            field=models.CharField(default='Barrendero', max_length=100),
            preserve_default=False,
        ),
    ]