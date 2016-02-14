# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashaccounting', '0009_cashaccountingexport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashaccountingexport',
            name='data_file',
            field=models.FileField(verbose_name='Export file', null=True, upload_to='cashaccounting_export', blank=True),
        ),
        migrations.AlterField(
            model_name='cashaccountingexport',
            name='data_file_date',
            field=models.DateTimeField(verbose_name='Timestamp of export file', blank=True, null=True),
        ),
    ]
