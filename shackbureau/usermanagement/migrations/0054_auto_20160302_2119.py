# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0053_remove_logcounter_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logcounter',
            name='amount',
        ),
        migrations.AddField(
            model_name='logcounter',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
