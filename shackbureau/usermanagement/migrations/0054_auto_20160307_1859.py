# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0053_banktransactionlog_debitor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banktransactionlog',
            name='debitor',
            field=models.ForeignKey(null=True, blank=True, verbose_name='Districtcourt debitor', to='districtcourt.Debitor'),
        ),
    ]
