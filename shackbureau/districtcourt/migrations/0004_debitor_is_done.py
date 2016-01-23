# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('districtcourt', '0003_auto_20160123_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='debitor',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]
