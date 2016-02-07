# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0042_auto_20160203_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='leave_date',
            field=models.DateField(help_text='Member left on this date. The date is forced to the end of given month', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='memberdocument',
            name='tag',
            field=models.ManyToManyField(to='usermanagement.MemberDocumentTag', blank=True),
        ),
    ]
