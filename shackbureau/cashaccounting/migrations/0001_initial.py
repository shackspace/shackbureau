# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CashTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('transaction_id', models.IntegerField(unique=True)),
                ('transaction_date', models.DateField()),
                ('description', models.CharField(max_length=255)),
                ('coin_001', models.IntegerField(help_text='amount of 1 cent coins')),
                ('coin_002', models.IntegerField(help_text='amount of 2 cent coins')),
                ('coin_005', models.IntegerField(help_text='amount of 5 cent coins')),
                ('coin_010', models.IntegerField(help_text='amount of 10 cent coins')),
                ('coin_020', models.IntegerField(help_text='amount of 20 cent coins')),
                ('coin_050', models.IntegerField(help_text='amount of 50 cent coins')),
                ('coin_100', models.IntegerField(help_text='amount of 1 euro coins')),
                ('coin_200', models.IntegerField(help_text='amount of 2 euro coins')),
                ('bill_005', models.IntegerField(help_text='amount of 5 euro bills')),
                ('bill_010', models.IntegerField(help_text='amount of 10 euro bills')),
                ('bill_020', models.IntegerField(help_text='amount of 20 euro bills')),
                ('bill_050', models.IntegerField(help_text='amount of 50 euro bills')),
                ('bill_100', models.IntegerField(help_text='amount of 100 euro bills')),
                ('bill_200', models.IntegerField(help_text='amount of 200 euro bills')),
                ('bill_500', models.IntegerField(help_text='amount of 500 euro bills')),
                ('transaction_sum', models.DecimalField(decimal_places=2, max_digits=8)),
                ('account_sum', models.DecimalField(decimal_places=2, max_digits=8)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
