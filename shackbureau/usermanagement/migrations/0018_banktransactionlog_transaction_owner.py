# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0017_auto_20150801_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransactionlog',
            name='transaction_owner',
            field=models.TextField(null=True, blank=True),
        ),
    ]
