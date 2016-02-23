# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentmanagement', '0006_donationreceipt_address_of_donator'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationreceipt',
            name='description_of_benefits',
            field=models.TextField(null=True, help_text='Genaue Bezeichnung der Sachzuwendung mit Alter, Zustand, Kaufpreis usw', blank=True),
        ),
        migrations.AddField(
            model_name='donationreceipt',
            name='donation_type',
            field=models.CharField(choices=[('benefits', 'Sachzuwendungen'), ('allowance in money', 'Geldzuwendungen')], default='allowance in money', max_length=25),
        ),
        migrations.AddField(
            model_name='donationreceipt',
            name='has_documents_of_value',
            field=models.BooleanField(default=False, help_text='Geeignete Unterlagen, die zur Wertermittlung gedient haben, z. B. Rechnung, Gutachten, liegen vor.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donationreceipt',
            name='is_from_business_assets',
            field=models.BooleanField(default=False, help_text='Die Sachzuwendung stammt nach den Angaben des Zuwendenden aus dem Betriebsvermögen. Die Zuwendung wurde nach dem Wert der Entnahme (ggf. mit dem niedrigeren gemeinen Wert) und nach der Umsatzsteuer, die auf die Entnahme entfällt, bewertet.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donationreceipt',
            name='is_from_private_assets',
            field=models.BooleanField(default=False, help_text='Die Sachzuwendung stammt nach den Angaben des Zuwendenden aus dem Privatvermögen'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donationreceipt',
            name='no_information_about_origin',
            field=models.BooleanField(default=False, help_text='Der Zuwendende hat trotz Aufforderung keine Angaben zur Herkunft der Sachzuwendung gemacht.'),
            preserve_default=False,
        ),
    ]
