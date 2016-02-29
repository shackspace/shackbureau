# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentmanagement', '0012_auto_20160226_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationreceipt',
            name='has_documents_of_value',
            field=models.BooleanField(help_text='Geeignete Unterlagen, die zur Wertermittlung gedient haben, z. B. Rechnung, Gutachten, liegen vor.', default=False),
        ),
        migrations.AlterField(
            model_name='donationreceipt',
            name='is_from_business_assets',
            field=models.BooleanField(help_text='Die Sachzuwendung stammt nach den Angaben des Zuwendenden aus dem Betriebsvermögen. Die Zuwendung wurde nach dem Wert der Entnahme (ggf. mit dem niedrigeren gemeinen Wert) und nach der Umsatzsteuer, die auf die Entnahme entfällt, bewertet.', default=False),
        ),
        migrations.AlterField(
            model_name='donationreceipt',
            name='is_from_private_assets',
            field=models.BooleanField(help_text='Die Sachzuwendung stammt nach den Angaben des Zuwendenden aus dem Privatvermögen', default=False),
        ),
        migrations.AlterField(
            model_name='donationreceipt',
            name='is_waive_of_charge',
            field=models.BooleanField(help_text='Es handelt sich um den Verzicht auf Erstattung von Aufwendungen', default=False),
        ),
        migrations.AlterField(
            model_name='donationreceipt',
            name='no_information_about_origin',
            field=models.BooleanField(help_text='Der Zuwendende hat trotz Aufforderung keine Angaben zur Herkunft der Sachzuwendung gemacht.', default=False),
        ),
    ]
