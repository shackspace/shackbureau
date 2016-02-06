# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashaccounting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashtransaction',
            name='bill_005',
            field=models.IntegerField(default=0, help_text='amount of 5 euro bills'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='bill_010',
            field=models.IntegerField(default=0, help_text='amount of 10 euro bills'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='bill_020',
            field=models.IntegerField(default=0, help_text='amount of 20 euro bills'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='bill_050',
            field=models.IntegerField(default=0, help_text='amount of 50 euro bills'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='bill_100',
            field=models.IntegerField(default=0, help_text='amount of 100 euro bills'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='bill_200',
            field=models.IntegerField(default=0, help_text='amount of 200 euro bills'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='bill_500',
            field=models.IntegerField(default=0, help_text='amount of 500 euro bills'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='coin_001',
            field=models.IntegerField(default=0, help_text='amount of 1 cent coins'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='coin_002',
            field=models.IntegerField(default=0, help_text='amount of 2 cent coins'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='coin_005',
            field=models.IntegerField(default=0, help_text='amount of 5 cent coins'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='coin_010',
            field=models.IntegerField(default=0, help_text='amount of 10 cent coins'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='coin_020',
            field=models.IntegerField(default=0, help_text='amount of 20 cent coins'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='coin_050',
            field=models.IntegerField(default=0, help_text='amount of 50 cent coins'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='coin_100',
            field=models.IntegerField(default=0, help_text='amount of 1 euro coins'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='coin_200',
            field=models.IntegerField(default=0, help_text='amount of 2 euro coins'),
        ),
        migrations.AlterField(
            model_name='cashtransaction',
            name='transaction_date',
            field=models.DateField(unique=True),
        ),
    ]
