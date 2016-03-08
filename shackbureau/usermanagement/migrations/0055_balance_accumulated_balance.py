# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0054_auto_20160307_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='accumulated_balance',
            field=models.DecimalField(max_digits=8, default='0.0', decimal_places=2),
            preserve_default=False,
        ),
    ]
