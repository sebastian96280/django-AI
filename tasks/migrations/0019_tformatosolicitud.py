# Generated by Django 5.0.3 on 2024-04-05 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0018_tarea_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='tformatoSolicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_formato', models.CharField(max_length=100)),
            ],
        ),
    ]