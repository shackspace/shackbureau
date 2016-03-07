# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('districtcourt', '0005_debitor_record_token_line_2'),
        ('usermanagement', '0052_auto_20160305_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransactionlog',
            name='debitor',
            field=models.ForeignKey(to='districtcourt.Debitor', null=True, blank=True),
        ),
    ]
