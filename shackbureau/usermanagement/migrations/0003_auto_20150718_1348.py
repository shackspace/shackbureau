# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.generic.models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0002_auto_20150718_1322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='active',
            new_name='is_active',
        ),
        migrations.AddField(
            model_name='member',
            name='iban_address',
            field=models.CharField(max_length=255, default=1, help_text='Address line (e.g. Street / House Number)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='iban_city',
            field=models.CharField(max_length=255, default=1, help_text='City'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='iban_country',
            field=models.CharField(max_length=255, default='Deutschland', help_text='Country'),
        ),
        migrations.AddField(
            model_name='member',
            name='iban_fullname',
            field=models.CharField(max_length=255, default=1, help_text='Full name for IBAN account owner'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='iban_zip_code',
            field=models.CharField(max_length=20, default=1, help_text='ZIP Code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='is_underaged',
            field=models.BooleanField(default=False, help_text='Member is not 18+.'),
        ),
        migrations.AlterField(
            model_name='member',
            name='bic',
            field=localflavor.generic.models.BICField(max_length=11, null=True, verbose_name='BIC', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='iban',
            field=localflavor.generic.models.IBANField(max_length=34, null=True, verbose_name='IBAN', blank=True),
        ),
    ]
