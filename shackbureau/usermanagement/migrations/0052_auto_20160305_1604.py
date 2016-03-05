# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0051_auto_20160215_0147'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accounttransaction',
            options={'ordering': ('-due_date',)},
        ),
    ]
