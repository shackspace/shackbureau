# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0056_memberlog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memberlog',
            old_name='timestamp',
            new_name='the_timestamp',
        ),
    ]
