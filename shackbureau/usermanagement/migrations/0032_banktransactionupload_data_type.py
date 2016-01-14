# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0031_auto_20151219_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransactionupload',
            name='data_type',
            field=models.CharField(max_length=255, default='bank_csv', choices=[('bank_csv', 'Bank [CSV]'), ('accountant_csv', 'Accountant [CSV]')]),
            preserve_default=False,
        ),
    ]
