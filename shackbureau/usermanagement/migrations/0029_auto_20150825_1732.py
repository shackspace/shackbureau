# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0028_member_iban_issue_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='iban_issue_date',
            field=models.DateField(blank=True, verbose_name='IBAN Issue Date', null=True, help_text='The issue date of the direct debit mandate'),
        ),
    ]
