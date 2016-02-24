# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentmanagement', '0009_remove_donationreceipt_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationreceipt',
            name='last_update_of_data_file',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='letter',
            name='last_update_of_data_file',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='donationreceipt',
            name='address_of_donator',
            field=models.TextField(),
        ),
    ]
