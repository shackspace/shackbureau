# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-02-11 16:09
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import documentmanagement.models


class Migration(migrations.Migration):

    replaces = [('documentmanagement', '0001_initial'), ('documentmanagement', '0002_auto_20160221_1914'), ('documentmanagement', '0003_auto_20160222_0121'), ('documentmanagement', '0004_auto_20160222_0144'), ('documentmanagement', '0005_auto_20160223_1629'), ('documentmanagement', '0006_donationreceipt_address_of_donator'), ('documentmanagement', '0007_auto_20160223_1908'), ('documentmanagement', '0008_auto_20160224_1354'), ('documentmanagement', '0009_remove_donationreceipt_address'), ('documentmanagement', '0010_auto_20160224_1731'), ('documentmanagement', '0011_dataprotectionagreement'), ('documentmanagement', '0012_auto_20160226_1829'), ('documentmanagement', '0013_auto_20160229_1319'), ('documentmanagement', '0014_auto_20160305_1604')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='will be used for filename', max_length=127)),
                ('data_file', models.FileField(upload_to=documentmanagement.models.Document.upload_to)),
                ('update_document', models.BooleanField(default=False, help_text='If you want to update the document after the first save you have to set this.')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('address', models.TextField()),
                ('date', models.DateField(default=datetime.date.today)),
                ('place', models.CharField(default='Stuttgart', max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('opening', models.CharField(default='Sehr geehrte Damen und Herren,', max_length=255)),
                ('content', models.TextField(help_text='You can write LaTeX here!')),
                ('closing', models.CharField(default='Mit freundlichen Grüßen', max_length=255)),
                ('signature', models.CharField(default='Der Vorstand', max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('last_update_of_data_file', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='DonationReceipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='will be used for filename', max_length=127)),
                ('data_file', models.FileField(upload_to=documentmanagement.models.Document.upload_to)),
                ('update_document', models.BooleanField(default=False, help_text='If you want to update the document after the first save you have to set this.')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('place', models.CharField(default='Stuttgart', max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('day_of_donation', models.DateField(default=datetime.datetime(2016, 2, 23, 16, 28, 55, 909270, tzinfo=utc))),
                ('is_waive_of_charge', models.BooleanField(default=False, help_text='Es handelt sich um den Verzicht auf Erstattung von Aufwendungen')),
                ('address_of_donator', models.TextField()),
                ('description_of_benefits', models.TextField(blank=True, help_text='Genaue Bezeichnung der Sachzuwendung mit Alter, Zustand, Kaufpreis usw', null=True)),
                ('donation_type', models.CharField(choices=[('benefits', 'Sachzuwendungen'), ('allowance in money', 'Geldzuwendungen')], default='allowance in money', max_length=25)),
                ('has_documents_of_value', models.BooleanField(default=False, help_text='Geeignete Unterlagen, die zur Wertermittlung gedient haben, z. B. Rechnung, Gutachten, liegen vor.')),
                ('is_from_business_assets', models.BooleanField(default=False, help_text='Die Sachzuwendung stammt nach den Angaben des Zuwendenden aus dem Betriebsvermögen. Die Zuwendung wurde nach dem Wert der Entnahme (ggf. mit dem niedrigeren gemeinen Wert) und nach der Umsatzsteuer, die auf die Entnahme entfällt, bewertet.')),
                ('is_from_private_assets', models.BooleanField(default=False, help_text='Die Sachzuwendung stammt nach den Angaben des Zuwendenden aus dem Privatvermögen')),
                ('no_information_about_origin', models.BooleanField(default=False, help_text='Der Zuwendende hat trotz Aufforderung keine Angaben zur Herkunft der Sachzuwendung gemacht.')),
                ('no_signature', models.BooleanField(default=True)),
                ('last_update_of_data_file', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='DataProtectionAgreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='will be used for filename', max_length=127)),
                ('data_file', models.FileField(upload_to=documentmanagement.models.Document.upload_to)),
                ('last_update_of_data_file', models.DateTimeField(blank=True, null=True)),
                ('update_document', models.BooleanField(default=False, help_text='If you want to update the document after the first save you have to set this.')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('address', models.TextField()),
                ('date', models.DateField(default=datetime.date.today)),
                ('place', models.CharField(default='Stuttgart', max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
    ]
