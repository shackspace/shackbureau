# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentmanagement', '0007_auto_20160223_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationreceipt',
            name='no_signature',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='donationreceipt',
            name='description',
            field=models.CharField(help_text='will be used for filename', max_length=127),
        ),
        migrations.AlterField(
            model_name='donationreceipt',
            name='is_waive_of_charge',
            field=models.BooleanField(help_text='Es handelt sich um den Verzicht auf Erstattung von Aufwendungen'),
        ),
        migrations.AlterField(
            model_name='letter',
            name='description',
            field=models.CharField(help_text='will be used for filename', max_length=127),
        ),
    ]
