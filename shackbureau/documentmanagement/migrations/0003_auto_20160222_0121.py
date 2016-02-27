# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import documentmanagement.models


class Migration(migrations.Migration):

    dependencies = [
        ('documentmanagement', '0002_auto_20160221_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter',
            name='content',
            field=models.TextField(help_text='You can write latex here'),
        ),
        migrations.AlterField(
            model_name='letter',
            name='data_file',
            field=models.FileField(upload_to=documentmanagement.models.Document.upload_to),
        ),
    ]
