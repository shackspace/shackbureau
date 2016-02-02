# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usermanagement', '0037_auto_20160131_2015'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('description', models.CharField(max_length=255)),
                ('data_file', models.FileField(upload_to='member_documents')),
                ('comment', models.TextField(blank=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('member', models.ForeignKey(to='usermanagement.Member')),
            ],
        ),
    ]
