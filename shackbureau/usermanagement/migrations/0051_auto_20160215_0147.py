# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usermanagement', '0050_auto_20160215_0105'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('year', models.PositiveIntegerField()),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('member', models.ForeignKey(to='usermanagement.Member')),
            ],
            options={
                'ordering': ('-year', 'member'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='balance',
            unique_together=set([('year', 'member')]),
        ),
    ]
