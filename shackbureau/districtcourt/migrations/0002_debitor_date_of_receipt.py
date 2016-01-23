# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('districtcourt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='debitor',
            name='date_of_receipt',
            field=models.DateField(default=datetime.datetime(2016, 1, 23, 20, 14, 8, 124219, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
