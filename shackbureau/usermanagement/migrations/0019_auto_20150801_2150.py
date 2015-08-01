# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0018_banktransactionlog_transaction_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banktransactionlog',
            old_name='needs_manual_interaction',
            new_name='is_matched',
        ),
    ]
