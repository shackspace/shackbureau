# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0014_auto_20150801_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransactionlog',
            name='error',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='banktransactionlog',
            name='score',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
