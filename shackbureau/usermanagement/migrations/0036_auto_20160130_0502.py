# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0035_member_is_revoke_memberspecials_mail_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberspecials',
            name='member',
            field=models.OneToOneField(to='usermanagement.Member'),
        ),
    ]
