# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cashaccounting', '0008_auto_20160205_0132'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashAccountingExport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('year', models.PositiveIntegerField(unique=True)),
                ('data_file', models.FileField(blank=True, upload_to='cashaccounting_export', null=True)),
                ('data_file_date', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
