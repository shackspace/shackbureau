# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usermanagement', '0013_auto_20150729_2044'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankTransactionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('reference', models.TextField()),
                ('needs_manual_interaction', models.BooleanField(default=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('member', models.ForeignKey(blank=True, to='usermanagement.Member', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='banktransactionupload',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now()),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='banktransactionupload',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='banktransactionupload',
            name='modified',
            field=models.DateTimeField(auto_now=True, default=timezone.now()),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='banktransactionlog',
            name='upload',
            field=models.ForeignKey(to='usermanagement.BankTransactionUpload'),
        ),
    ]
