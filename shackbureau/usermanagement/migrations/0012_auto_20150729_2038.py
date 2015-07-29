# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0011_member_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankTransactionUploads',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('data_file', models.FileField(upload_to='bank_transaction_uploads')),
                ('status', models.TextField(default='new', choices=[('new', 'New'), ('wip', 'Work in progress'), ('done', 'Imported'), ('fail', 'Could not import')])),
            ],
        ),
        migrations.AlterField(
            model_name='accounttransaction',
            name='booking_type',
            field=models.CharField(max_length=255, choices=[('claim', 'Forderung'), ('fee_claim', 'Forderung (automatischer Mitgliedsbeitrag)'), ('deposit', 'Einzahlung'), ('credit', 'Gutschrift')]),
        ),
        migrations.AlterField(
            model_name='member',
            name='join_date',
            field=models.DateField(help_text='Member joined on this date. The date is forced to the begin of given month.'),
        ),
    ]
