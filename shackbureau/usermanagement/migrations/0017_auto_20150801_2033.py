# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0016_accounttransaction_transaction_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banktransactionlog',
            name='error',
            field=models.TextField(blank=True, null=True),
        ),
    ]
