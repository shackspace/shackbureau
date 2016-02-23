# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('documentmanagement', '0004_auto_20160222_0144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donationreceipt',
            name='closing',
        ),
        migrations.RemoveField(
            model_name='donationreceipt',
            name='opening',
        ),
        migrations.RemoveField(
            model_name='donationreceipt',
            name='signature',
        ),
        migrations.RemoveField(
            model_name='donationreceipt',
            name='subject',
        ),
        migrations.AddField(
            model_name='donationreceipt',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=8, default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donationreceipt',
            name='amount_in_words',
            field=models.CharField(max_length=255, default='Null'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donationreceipt',
            name='day_of_donation',
            field=models.DateField(default=datetime.datetime(2016, 2, 23, 16, 28, 55, 909270, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donationreceipt',
            name='is_waive_of_charge',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='donationreceipt',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='letter',
            name='date',
            field=models.DateField(),
        ),
    ]
