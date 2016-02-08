# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def set_is_payment_instruction_sent(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Membership = apps.get_model("usermanagement", "Membership")
    Membership.objects.update(is_payment_instruction_sent=True)
    # for membership in Membership.objects.all():
    #     membership.is_payment_instruction_sent = True
    #     membership.save()


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0044_auto_20160208_1103'),
    ]

    operations = [
        migrations.RunPython(set_is_payment_instruction_sent),
    ]
