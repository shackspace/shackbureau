# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('documentmanagement', '0013_auto_20160229_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataprotectionagreement',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='donationreceipt',
            name='date',
            field=models.DateField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='letter',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
