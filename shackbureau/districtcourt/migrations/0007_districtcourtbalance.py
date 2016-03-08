# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('districtcourt', '0006_districtcourtaccounttransaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='DistrictcourtBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('debitor', models.OneToOneField(to='districtcourt.Debitor')),
            ],
            options={
                'ordering': ('debitor',),
            },
        ),
    ]
