# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashaccounting', '0004_auto_20160204_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashtransaction',
            name='account_bill_005',
            field=models.IntegerField(verbose_name='account 5 euro', help_text='amount of 5 euro bills', default=0),
        ),
        migrations.AddField(
            model_name='cashtransaction',
            name='account_bill_010',
            field=models.IntegerField(verbose_name='account 10 euro', help_text='amount of 10 euro bills', default=0),
        ),
        migrations.AddField(
            model_name='cashtransaction',
            name='account_bill_020',
            field=models.IntegerField(verbose_name='account 20 euro', help_text='amount of 20 euro bills', default=0),
        ),
        migrations.AddField(
            model_name='cashtransaction',
            name='account_bill_050',
            field=models.IntegerField(verbose_name='account 50 euro', help_text='amount of 50 euro bills', default=0),
        ),
        migrations.AddField(
            model_name='cashtransaction',
            name='account_bill_100',
            field=models.IntegerField(verbose_name='account 100 euro', help_text='amount of 100 euro bills', default=0),
        ),
        migrations.AddField(
            model_name='cashtransaction',
            name='account_bill_200',
            field=models.IntegerField(verbose_name='account 200 euro', help_text='amount of 200 euro bills', default=0),
        ),
        migrations.AddField(
            model_name='cashtransaction',
            name='account_bill_500',
            field=models.IntegerField(verbose_name='account 500 euro', help_text='amount of 500 euro bills', default=0),
        ),
        migrations.AddField(
            model_name='cashtransaction',
            name='account_coin_001',
            field=models.IntegerField(verbose_name='account 1 cent', help_text='amount of 1 cent coins', default=0),
        ),
        migrations.AddField(
            model_name='cashtransaction',
            name='account_coin_002',
            field=models.IntegerField(verbose_name='account 2 cent', help_text='amount of 2 cent coins', default=0),
        ),
        migrations.AddField(
            model_name='cashtransaction',
            name='account_coin_005',
            field=models.IntegerField(verbose_name='account 5 cent', help_text='amount of 5 cent coins', default=0),
        ),
        migrations.AddField(
            model_name='cashtransaction',
            name='account_coin_010',
            field=models.IntegerField(verbose_name='account 10 cent', help_text='amount of 10 cent coins', default=0),
        ),
        migrations.AddField(
            model_name='cashtransaction',
            name='account_coin_020',
            field=models.IntegerField(verbose_name='account 20 cent', help_text='amount of 20 cent coins', default=0),
        ),
        migrations.AddField(
            model_name='cashtransaction',
            name='account_coin_050',
            field=models.IntegerField(verbose_name='account 50 cent', help_text='amount of 50 cent coins', default=0),
        ),
        migrations.AddField(
            model_name='cashtransaction',
            name='account_coin_100',
            field=models.IntegerField(verbose_name='account 1 euro', help_text='amount of 1 euro coins', default=0),
        ),
        migrations.AddField(
            model_name='cashtransaction',
            name='account_coin_200',
            field=models.IntegerField(verbose_name='account 2 euro', help_text='amount of 2 euro coins', default=0),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_bill_005',
            field=models.IntegerField(verbose_name='transaction 5 euro', help_text='amount of 5 euro bills', default=0),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_bill_010',
            field=models.IntegerField(verbose_name='transaction 10 euro', help_text='amount of 10 euro bills', default=0),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_bill_020',
            field=models.IntegerField(verbose_name='transaction 20 euro', help_text='amount of 20 euro bills', default=0),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_bill_050',
            field=models.IntegerField(verbose_name='transaction 50 euro', help_text='amount of 50 euro bills', default=0),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_bill_100',
            field=models.IntegerField(verbose_name='transaction 100 euro', help_text='amount of 100 euro bills', default=0),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_bill_200',
            field=models.IntegerField(verbose_name='transaction 200 euro', help_text='amount of 200 euro bills', default=0),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_bill_500',
            field=models.IntegerField(verbose_name='transaction 500 euro', help_text='amount of 500 euro bills', default=0),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_coin_001',
            field=models.IntegerField(verbose_name='transaction 1 cent', help_text='amount of 1 cent coins', default=0),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_coin_002',
            field=models.IntegerField(verbose_name='transaction 2 cent', help_text='amount of 2 cent coins', default=0),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_coin_005',
            field=models.IntegerField(verbose_name='transaction 5 cent', help_text='amount of 5 cent coins', default=0),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_coin_010',
            field=models.IntegerField(verbose_name='transaction 10 cent', help_text='amount of 10 cent coins', default=0),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_coin_020',
            field=models.IntegerField(verbose_name='transaction 20 cent', help_text='amount of 20 cent coins', default=0),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_coin_050',
            field=models.IntegerField(verbose_name='transaction 50 cent', help_text='amount of 50 cent coins', default=0),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_coin_100',
            field=models.IntegerField(verbose_name='transaction 1 euro', help_text='amount of 1 euro coins', default=0),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_coin_200',
            field=models.IntegerField(verbose_name='transaction 2 euro', help_text='amount of 2 euro coins', default=0),
        ),
    ]
