# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0010_auto_20150719_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
