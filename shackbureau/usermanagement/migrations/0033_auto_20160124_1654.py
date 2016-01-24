# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0032_banktransactionupload_data_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='valid_from',
            field=models.DateField(help_text='Membership starts on this date. The date is forced to the begin of given month.'),
        ),
    ]
