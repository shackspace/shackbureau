# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usermanagement', '0007_auto_20150719_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountTransaction',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('due_date', models.DateField(null=True, blank=True)),
                ('booking_date', models.DateField()),
                ('transaction_type', models.CharField(choices=[('membership fee', 'membership fee'), ('donation', 'donation')], max_length=255)),
                ('booking_type', models.CharField(choices=[('claim', 'Forderung'), ('deposit', 'Einzahlung')], max_length=255)),
                ('payment_reference', models.TextField()),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('member', models.ForeignKey(to='usermanagement.Member')),
            ],
        ),
    ]
