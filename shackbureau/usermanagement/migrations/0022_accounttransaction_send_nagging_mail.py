# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0021_auto_20150801_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounttransaction',
            name='send_nagging_mail',
            field=models.BooleanField(default=False),
        ),
    ]
