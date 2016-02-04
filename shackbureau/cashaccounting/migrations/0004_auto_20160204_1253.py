# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashaccounting', '0003_auto_20160204_0122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cashtransaction',
            old_name='bill_005',
            new_name='transaction_bill_005',
        ),
        migrations.RenameField(
            model_name='cashtransaction',
            old_name='bill_010',
            new_name='transaction_bill_010',
        ),
        migrations.RenameField(
            model_name='cashtransaction',
            old_name='bill_020',
            new_name='transaction_bill_020',
        ),
        migrations.RenameField(
            model_name='cashtransaction',
            old_name='bill_050',
            new_name='transaction_bill_050',
        ),
        migrations.RenameField(
            model_name='cashtransaction',
            old_name='bill_100',
            new_name='transaction_bill_100',
        ),
        migrations.RenameField(
            model_name='cashtransaction',
            old_name='bill_200',
            new_name='transaction_bill_200',
        ),
        migrations.RenameField(
            model_name='cashtransaction',
            old_name='bill_500',
            new_name='transaction_bill_500',
        ),
        migrations.RenameField(
            model_name='cashtransaction',
            old_name='coin_001',
            new_name='transaction_coin_001',
        ),
        migrations.RenameField(
            model_name='cashtransaction',
            old_name='coin_002',
            new_name='transaction_coin_002',
        ),
        migrations.RenameField(
            model_name='cashtransaction',
            old_name='coin_005',
            new_name='transaction_coin_005',
        ),
        migrations.RenameField(
            model_name='cashtransaction',
            old_name='coin_010',
            new_name='transaction_coin_010',
        ),
        migrations.RenameField(
            model_name='cashtransaction',
            old_name='coin_020',
            new_name='transaction_coin_020',
        ),
        migrations.RenameField(
            model_name='cashtransaction',
            old_name='coin_050',
            new_name='transaction_coin_050',
        ),
        migrations.RenameField(
            model_name='cashtransaction',
            old_name='coin_100',
            new_name='transaction_coin_100',
        ),
        migrations.RenameField(
            model_name='cashtransaction',
            old_name='coin_200',
            new_name='transaction_coin_200',
        ),
    ]
