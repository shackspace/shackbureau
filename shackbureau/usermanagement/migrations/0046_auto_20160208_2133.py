# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from datetime import date


def set_iban_issue_date(apps, schema_editor):
    Member = apps.get_model("usermanagement", "Member")
    Member.objects.filter(payment_type="SEPA", iban_issue_date=None).update(iban_issue_date=date(1970, 1, 1))


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0045_auto_20160208_1104'),
    ]

    operations = [
        migrations.RunPython(set_iban_issue_date),
    ]
