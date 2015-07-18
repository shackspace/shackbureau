# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.generic.models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='bic',
            field=localflavor.generic.models.BICField(null=True, blank=True, max_length=11),
        ),
        migrations.AddField(
            model_name='member',
            name='iban',
            field=localflavor.generic.models.IBANField(null=True, blank=True, max_length=34),
        ),
    ]
