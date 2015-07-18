# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0003_auto_20150718_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='payment_type',
            field=models.CharField(max_length=20, choices=[('SEPA', 'Lastschrift'), ('transfer', 'Überweisung')], default='SEPA'),
        ),
        migrations.AlterField(
            model_name='member',
            name='iban_address',
            field=models.CharField(help_text='Address line (e.g. Street / House Number)', verbose_name='IBAN address', max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='iban_city',
            field=models.CharField(help_text='City', verbose_name='IBAN City', max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='iban_country',
            field=models.CharField(help_text='Country', max_length=255, default='Deutschland', null=True, verbose_name='IBAN Country', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='iban_fullname',
            field=models.CharField(help_text='Full name for IBAN account owner', verbose_name='IBAN full name', max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='iban_zip_code',
            field=models.CharField(help_text='ZIP Code', verbose_name='IBAN zip code', max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='membership_fee_interval',
            field=models.PositiveIntegerField(help_text='Pays for N months at once', choices=[(1, '1'), (12, '12')], default=1),
        ),
        migrations.AlterField(
            model_name='member',
            name='membership_type',
            field=models.CharField(max_length=20, choices=[('full', 'Vollzahler'), ('reduced', 'ermässigt')], default='full'),
        ),
    ]
