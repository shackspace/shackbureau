# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashaccounting', '0010_auto_20160214_1744'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cashaccountingexport',
            options={'ordering': ('-year',)},
        ),
    ]
