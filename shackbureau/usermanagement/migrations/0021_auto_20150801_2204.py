# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0020_banktransactionlog_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransactionlog',
            name='booking_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='banktransactionlog',
            name='is_resolved',
            field=models.BooleanField(default=True),
        ),
    ]
