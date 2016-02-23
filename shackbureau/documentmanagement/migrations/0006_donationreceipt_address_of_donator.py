# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentmanagement', '0005_auto_20160223_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationreceipt',
            name='address_of_donator',
            field=models.TextField(null=True, blank=True, help_text='if empty, address will be use'),
        ),
    ]
