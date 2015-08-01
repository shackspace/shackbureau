# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0015_auto_20150801_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounttransaction',
            name='transaction_hash',
            field=models.TextField(null=True, blank=True),
        ),
    ]
