# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0057_auto_20160410_1850'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memberlog',
            old_name='the_timestamp',
            new_name='timestamp',
        ),
    ]
