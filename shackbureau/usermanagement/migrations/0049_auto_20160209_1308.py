# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def set_memberspecials_is_registration_to_key_mailinglist_sent(apps, schema_editor):
    Memberspecials = apps.get_model("usermanagement", "Memberspecials")
    Memberspecials.objects \
        .filter(is_keyholder=True) \
        .update(is_registration_to_key_mailinglist_sent=True)


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0048_memberspecials_is_registration_to_key_mailinglist_sent'),
    ]

    operations = [
        migrations.RunPython(set_memberspecials_is_registration_to_key_mailinglist_sent),
    ]
