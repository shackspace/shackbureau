# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0027_member_is_cancellation_mail_sent_to_cashmaster'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='iban_issue_date',
            field=models.DateField(help_text='The issue date of the direct debit mandate', blank=True, null=True),
        ),
    ]
