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
            name='Debitor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('debitor_id', models.IntegerField(help_text='Debitor ID', unique=True)),
                ('comment', models.TextField(null=True, blank=True)),
                ('districtcourt', models.CharField(choices=[('reutlingen', 'Amtsgericht Reutlingen')], max_length=10, default='reutlingen')),
                ('record_token', models.CharField(help_text='Aktenzeichen', max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('debt_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('due_date', models.DateField()),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
