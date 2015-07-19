# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0006_auto_20150718_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_payment_instruction_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='member',
            name='is_registration_to_mailinglists_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='member',
            name='is_welcome_mail_sent',
            field=models.BooleanField(default=False),
        ),
    ]
