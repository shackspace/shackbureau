# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0038_memberdocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberDocumentTag',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('tag', models.CharField(max_length=255)),
                ('document', models.ManyToManyField(to='usermanagement.MemberDocument')),
            ],
        ),
    ]
