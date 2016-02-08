# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0046_auto_20160208_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='iban_issue_date',
            field=models.DateField(null=True, blank=True, help_text='The issue date of the direct debit mandate. (1970-01-01 means there is no issue date in the database )', verbose_name='IBAN Issue Date'),
        ),
    ]
