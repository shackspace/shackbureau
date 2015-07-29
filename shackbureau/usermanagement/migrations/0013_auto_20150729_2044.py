# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0012_auto_20150729_2038'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankTransactionUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('data_file', models.FileField(upload_to='bank_transaction_uploads')),
                ('status', models.CharField(default='new', choices=[('new', 'New'), ('wip', 'Work in progress'), ('done', 'Imported'), ('fail', 'Could not import')], max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='BankTransactionUploads',
        ),
    ]
