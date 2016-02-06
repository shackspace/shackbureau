# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashaccounting', '0005_auto_20160204_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashtransaction',
            name='is_stored_by_account',
            field=models.BooleanField(default=False),
        ),
    ]
