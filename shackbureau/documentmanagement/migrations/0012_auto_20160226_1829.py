# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentmanagement', '0011_dataprotectionagreement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donationreceipt',
            name='amount_in_words',
        ),
        migrations.AlterField(
            model_name='dataprotectionagreement',
            name='update_document',
            field=models.BooleanField(help_text='If you want to update the document after the first save you have to set this.', default=False),
        ),
        migrations.AlterField(
            model_name='donationreceipt',
            name='update_document',
            field=models.BooleanField(help_text='If you want to update the document after the first save you have to set this.', default=False),
        ),
        migrations.AlterField(
            model_name='letter',
            name='update_document',
            field=models.BooleanField(help_text='If you want to update the document after the first save you have to set this.', default=False),
        ),
    ]
