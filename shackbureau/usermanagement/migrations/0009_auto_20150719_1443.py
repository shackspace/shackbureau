# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usermanagement', '0008_accounttransaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('valid_from', models.DateField()),
                ('membership_type', models.CharField(choices=[('full', 'Vollzahler'), ('reduced', 'ermässigt')], default='full', max_length=20)),
                ('membership_fee_monthly', models.DecimalField(decimal_places=2, default=20, max_digits=8)),
                ('membership_fee_interval', models.PositiveIntegerField(help_text='Pays for N months at once', default=1, choices=[(1, '1'), (12, '12')])),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='member',
            name='membership_fee_interval',
        ),
        migrations.RemoveField(
            model_name='member',
            name='membership_fee_monthly',
        ),
        migrations.RemoveField(
            model_name='member',
            name='membership_type',
        ),
        migrations.AlterField(
            model_name='accounttransaction',
            name='booking_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='accounttransaction',
            name='booking_type',
            field=models.CharField(choices=[('claim', 'Forderung'), ('deposit', 'Einzahlung'), ('credit', 'Gutschrift')], max_length=255),
        ),
        migrations.AlterField(
            model_name='accounttransaction',
            name='transaction_type',
            field=models.CharField(choices=[('membership fee', 'Mitgliedsbeitrag'), ('donation', 'Spende')], max_length=255),
        ),
        migrations.AddField(
            model_name='membership',
            name='member',
            field=models.ForeignKey(to='usermanagement.Member'),
        ),
    ]
