# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0030_membertrackingcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberspecials',
            name='has_loeffelhardt_account',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='memberspecials',
            name='has_safe_key',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='memberspecials',
            name='signed_DSV',
            field=models.BooleanField(default=False),
        ),
    ]
