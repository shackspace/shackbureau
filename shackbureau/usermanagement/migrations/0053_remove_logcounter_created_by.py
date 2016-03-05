# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0052_logcounter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logcounter',
            name='created_by',
        ),
    ]
