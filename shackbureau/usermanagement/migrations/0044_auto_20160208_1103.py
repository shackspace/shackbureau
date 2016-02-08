# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0043_auto_20160207_2023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='is_payment_instruction_sent',
        ),
        migrations.AddField(
            model_name='membership',
            name='is_payment_instruction_sent',
            field=models.BooleanField(default=False),
        ),
    ]
