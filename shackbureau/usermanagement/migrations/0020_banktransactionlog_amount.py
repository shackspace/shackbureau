# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0019_auto_20150801_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransactionlog',
            name='amount',
            field=models.DecimalField(default=1, max_digits=8, decimal_places=2),
            preserve_default=False,
        ),
    ]
