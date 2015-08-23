# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0025_auto_20150802_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberspecials',
            name='has_selgros_card',
            field=models.BooleanField(default=False),
        ),
    ]
