# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('districtcourt', '0004_debitor_is_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='debitor',
            name='record_token_line_2',
            field=models.CharField(max_length=255, blank=True, help_text='Aktenzeichen Zeile 2', null=True),
        ),
    ]
