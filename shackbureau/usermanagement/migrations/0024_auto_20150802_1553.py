# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usermanagement', '0023_memberspecials'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberspecials',
            name='created',
            field=models.DateTimeField(default=timezone.now(), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='memberspecials',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='memberspecials',
            name='modified',
            field=models.DateTimeField(default=timezone.now(), auto_now=True),
            preserve_default=False,
        ),
    ]
