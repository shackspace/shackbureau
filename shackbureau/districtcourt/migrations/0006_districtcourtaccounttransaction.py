# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('districtcourt', '0005_debitor_record_token_line_2'),
    ]

    operations = [
        migrations.CreateModel(
            name='DistrictcourtAccountTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(max_digits=8, decimal_places=2)),
                ('due_date', models.DateField()),
                ('booking_date', models.DateField(default=datetime.date.today)),
                ('booking_type', models.CharField(choices=[('claim', 'Forderung'), ('districtcourt_claim', 'Automatische Forderung des Amtsgericht'), ('deposit', 'Einzahlung'), ('credit', 'Gutschrift')], max_length=255)),
                ('payment_reference', models.TextField()),
                ('transaction_hash', models.TextField(blank=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('debitor', models.ForeignKey(to='districtcourt.Debitor')),
            ],
            options={
                'ordering': ('-due_date',),
            },
        ),
    ]
