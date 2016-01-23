# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('districtcourt', '0002_debitor_date_of_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debitor',
            name='date_of_receipt',
            field=models.DateField(),
        ),
    ]
