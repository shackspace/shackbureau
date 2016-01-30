# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0034_auto_20160124_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_revoke_memberspecials_mail_sent',
            field=models.BooleanField(default=False),
        ),
    ]
