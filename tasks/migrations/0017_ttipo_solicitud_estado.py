# Generated by Django 5.0.3 on 2024-04-05 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0016_ttipe_document_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='ttipo_solicitud',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]
