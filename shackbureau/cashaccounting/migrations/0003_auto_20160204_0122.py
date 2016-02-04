# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashaccounting', '0002_auto_20160204_0040'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cashtransaction',
            options={'ordering': ('-transaction_date',)},
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='bill_005',
            field=models.IntegerField(default=0, verbose_name='5 euro', help_text='amount of 5 euro bills'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='bill_010',
            field=models.IntegerField(default=0, verbose_name='10 euro', help_text='amount of 10 euro bills'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='bill_020',
            field=models.IntegerField(default=0, verbose_name='20 euro', help_text='amount of 20 euro bills'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='bill_050',
            field=models.IntegerField(default=0, verbose_name='50 euro', help_text='amount of 50 euro bills'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='bill_100',
            field=models.IntegerField(default=0, verbose_name='100 euro', help_text='amount of 100 euro bills'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='bill_200',
            field=models.IntegerField(default=0, verbose_name='200 euro', help_text='amount of 200 euro bills'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='bill_500',
            field=models.IntegerField(default=0, verbose_name='500 euro', help_text='amount of 500 euro bills'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='coin_001',
            field=models.IntegerField(default=0, verbose_name='1 cent', help_text='amount of 1 cent coins'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='coin_002',
            field=models.IntegerField(default=0, verbose_name='2 cent', help_text='amount of 2 cent coins'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='coin_005',
            field=models.IntegerField(default=0, verbose_name='5 cent', help_text='amount of 5 cent coins'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='coin_010',
            field=models.IntegerField(default=0, verbose_name='10 cent', help_text='amount of 10 cent coins'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='coin_020',
            field=models.IntegerField(default=0, verbose_name='20 cent', help_text='amount of 20 cent coins'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='coin_050',
            field=models.IntegerField(default=0, verbose_name='50 cent', help_text='amount of 50 cent coins'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='coin_100',
            field=models.IntegerField(default=0, verbose_name='1 euro', help_text='amount of 1 euro coins'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='coin_200',
            field=models.IntegerField(default=0, verbose_name='2 euro', help_text='amount of 2 euro coins'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_id',
            field=models.IntegerField(unique=True, verbose_name='id'),
        ),
    ]
