# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('description', models.CharField(max_length=255)),
                ('data_file', models.FileField(upload_to='documentmanagement_')),
                ('update_document', models.BooleanField(default=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('address', models.TextField()),
                ('date', models.DateField(max_length=255, auto_now_add=True)),
                ('place', models.CharField(max_length=255, default='Stuttgart')),
                ('subject', models.CharField(max_length=255)),
                ('opening', models.CharField(max_length=255, default='Sehr geehrte Damen und Herren,')),
                ('content', models.TextField()),
                ('closing', models.CharField(max_length=255, default='Mit freundlichen Grüßen')),
                ('signature', models.CharField(max_length=255, default='Der Vorstand')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
    ]
