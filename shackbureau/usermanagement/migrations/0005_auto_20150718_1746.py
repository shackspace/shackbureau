# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0004_auto_20150718_1410'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ('-created',)},
        ),
        migrations.AddField(
            model_name='member',
            name='is_cancellation_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='member',
            name='form_of_address',
            field=models.CharField(max_length=10, choices=[('F', 'Frau'), ('H', 'Herr')], help_text='How to formally address this person', default='H'),
        ),
    ]
