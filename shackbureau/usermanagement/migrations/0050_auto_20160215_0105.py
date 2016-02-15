# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0049_auto_20160209_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttransaction',
            name='booking_type',
            field=models.CharField(choices=[('claim', 'Forderung'), ('fee_claim', 'Forderung (automatischer Mitgliedsbeitrag)'), ('deposit', 'Einzahlung'), ('credit', 'Gutschrift'), ('charge back', 'Rücklastschrift')], max_length=255),
        ),
    ]
