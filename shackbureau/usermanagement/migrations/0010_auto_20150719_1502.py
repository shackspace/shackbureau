# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0009_auto_20150719_1443'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='membership',
            options={'ordering': ('-valid_from',)},
        ),
    ]
