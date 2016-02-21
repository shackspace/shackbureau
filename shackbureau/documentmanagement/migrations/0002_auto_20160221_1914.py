# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentmanagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter',
            name='date',
            field=models.DateField(max_length=255),
        ),
    ]
