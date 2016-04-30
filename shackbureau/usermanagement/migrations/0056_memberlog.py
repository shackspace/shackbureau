# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usermanagement', '0055_balance_accumulated_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Memberlog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('action', models.CharField(max_length=255)),
                ('detail', models.TextField(null=True, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
                ('member', models.ForeignKey(null=True, blank=True, to='usermanagement.Member')),
            ],
        ),
    ]
