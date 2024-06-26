# Generated by Django 5.0.3 on 2024-05-10 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0022_alter_tsolicitud_apellidos_alter_tsolicitud_nombre'),
    ]

    operations = [
        migrations.CreateModel(
            name='configuracion_correo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_backend', models.CharField(max_length=255)),
                ('email_host', models.CharField(max_length=255)),
                ('email_port', models.IntegerField()),
                ('email_host_user', models.CharField(max_length=255)),
                ('email_host_password', models.CharField(max_length=255)),
                ('email_use_tls', models.BooleanField()),
            ],
        ),
    ]
