# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0036_auto_20160130_0502'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='iban_institute',
            field=models.CharField(null=True, blank=True, verbose_name='IBAN Institute', max_length=255),
        ),
        migrations.AlterField(
            model_name='memberspecials',
            name='ssh_public_key',
            field=models.TextField(null=True, help_text='The format ist forced into one line, with single whitespaces as seperators', blank=True),
        ),
    ]
