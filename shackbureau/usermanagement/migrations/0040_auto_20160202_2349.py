# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0039_memberdocumenttag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memberdocumenttag',
            name='document',
        ),
        migrations.AddField(
            model_name='memberdocument',
            name='tag',
            field=models.ManyToManyField(to='usermanagement.MemberDocumentTag'),
        ),
    ]
