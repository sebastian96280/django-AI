# Generated by Django 5.0.3 on 2024-03-12 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_tsolicitud_archivo_pdf_tsolicitud_nombre_archivo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='tTipo_solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_solicitud', models.CharField(max_length=100)),
            ],
        ),
    ]
