# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0024_auto_20150802_1553'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='memberspecials',
            options={'verbose_name_plural': 'Member Specials', 'verbose_name': 'Member Specials'},
        ),
        migrations.AlterField(
            model_name='memberspecials',
            name='ssh_public_key',
            field=models.TextField(null=True, blank=True),
        ),
    ]
