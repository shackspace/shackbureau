# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0047_auto_20160208_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberspecials',
            name='is_registration_to_key_mailinglist_sent',
            field=models.BooleanField(default=False),
        ),
    ]
