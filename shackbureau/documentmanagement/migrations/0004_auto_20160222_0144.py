# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import documentmanagement.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documentmanagement', '0003_auto_20160222_0121'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationReceipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=255)),
                ('data_file', models.FileField(upload_to=documentmanagement.models.Document.upload_to)),
                ('update_document', models.BooleanField(default=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('address', models.TextField()),
                ('date', models.DateField(max_length=255)),
                ('place', models.CharField(max_length=255, default='Stuttgart')),
                ('subject', models.CharField(max_length=255)),
                ('opening', models.CharField(max_length=255, default='Sehr geehrte Damen und Herren,')),
                ('closing', models.CharField(max_length=255, default='Mit freundlichen Grüßen')),
                ('signature', models.CharField(max_length=255, default='Der Vorstand')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.AlterField(
            model_name='letter',
            name='content',
            field=models.TextField(help_text='You can write LaTeX here!'),
        ),
    ]
