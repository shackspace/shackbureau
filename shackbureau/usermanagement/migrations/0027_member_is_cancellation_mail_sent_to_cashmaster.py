# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0026_memberspecials_has_selgros_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_cancellation_mail_sent_to_cashmaster',
            field=models.BooleanField(default=False),
        ),
    ]
