# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0041_auto_20160202_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberdocument',
            name='tag',
            field=models.ManyToManyField(null=True, to='usermanagement.MemberDocumentTag', blank=True),
        ),
    ]
