# Generated by Django 5.0.3 on 2024-04-05 23:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0019_tformatosolicitud'),
    ]

    operations = [
        migrations.AddField(
            model_name='tsolicitud',
            name='id_nombre_formato',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='tasks.tformatosolicitud'),
            preserve_default=False,
        ),
    ]
