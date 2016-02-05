# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashaccounting', '0007_auto_20160205_0126'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cashtransaction',
            unique_together=set([('transaction_date', 'transaction_date_id')]),
        ),
    ]
