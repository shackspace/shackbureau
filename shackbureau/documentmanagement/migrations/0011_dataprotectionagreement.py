# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import documentmanagement.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documentmanagement', '0010_auto_20160224_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataProtectionAgreement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('description', models.CharField(max_length=127, help_text='will be used for filename')),
                ('data_file', models.FileField(upload_to=documentmanagement.models.Document.upload_to)),
                ('last_update_of_data_file', models.DateTimeField(null=True, blank=True)),
                ('update_document', models.BooleanField(default=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('address', models.TextField()),
                ('date', models.DateField()),
                ('place', models.CharField(max_length=255, default='Stuttgart')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
    ]
