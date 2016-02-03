# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usermanagement', '0040_auto_20160202_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberdocumenttag',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='memberdocumenttag',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='memberdocumenttag',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 2, 23, 57, 42, 254353, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='memberdocumenttag',
            name='tag',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
