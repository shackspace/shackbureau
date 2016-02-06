# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashaccounting', '0006_cashtransaction_is_stored_by_account'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cashtransaction',
            options={'ordering': ('-transaction_date', '-transaction_date_id')},
        ),
        migrations.AddField(
            model_name='cashtransaction',
            name='transaction_date_id',
            field=models.IntegerField(verbose_name='Transaction of the Day', default=1),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_date',
            field=models.DateField(),
        ),
    ]
