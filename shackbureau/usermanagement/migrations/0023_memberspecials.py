# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0022_accounttransaction_send_nagging_mail'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberSpecials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('has_matomat_key', models.BooleanField(default=False)),
                ('has_snackomat_key', models.BooleanField(default=False)),
                ('has_metro_card', models.BooleanField(default=False)),
                ('has_shack_iron_key', models.BooleanField(default=False)),
                ('is_keyholder', models.BooleanField(default=False)),
                ('ssh_public_key', models.TextField(default='')),
                ('member', models.ForeignKey(to='usermanagement.Member')),
            ],
        ),
    ]
