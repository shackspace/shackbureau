# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0005_auto_20150718_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='city',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='member',
            name='country',
            field=models.CharField(max_length=255, default='Deutschland'),
        ),
        migrations.AlterField(
            model_name='member',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='member',
            name='date_of_birth',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(max_length=255),
        ),
        migrations.AlterField(
            model_name='member',
            name='iban_city',
            field=models.CharField(verbose_name='IBAN City', max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='iban_country',
            field=models.CharField(blank=True, verbose_name='IBAN Country', null=True, default='Deutschland', max_length=255),
        ),
        migrations.AlterField(
            model_name='member',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='membership_fee_monthly',
            field=models.DecimalField(max_digits=8, default=20, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='member',
            name='nickname',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
