# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('member_id', models.IntegerField(unique=True, help_text='Membership ID')),
                ('name', models.CharField(help_text='First/Given Name', max_length=255)),
                ('surname', models.CharField(help_text='Last/Family Name', max_length=255)),
                ('nickname', models.CharField(blank=True, null=True, help_text='Nickname', max_length=255)),
                ('form_of_address', models.CharField(max_length=10, help_text='How to formally address this person', choices=[('F', 'Frau'), ('H', 'Herr')])),
                ('date_of_birth', models.DateField(blank=True, null=True, help_text='Date of Birth')),
                ('address1', models.CharField(help_text='Address line 1 (e.g. Street / House Number)', max_length=255)),
                ('address2', models.CharField(blank=True, null=True, help_text='Address line 2 (optional)', max_length=255)),
                ('zip_code', models.CharField(help_text='ZIP Code', max_length=20)),
                ('city', models.CharField(help_text='City', max_length=255)),
                ('country', models.CharField(default='Deutschland', help_text='Country', max_length=255)),
                ('email', models.EmailField(help_text='E-mail address', max_length=255)),
                ('phone_number', models.CharField(blank=True, null=True, max_length=32)),
                ('join_date', models.DateField(help_text='Member joined on this date')),
                ('leave_date', models.DateField(blank=True, null=True, help_text='Member left on this date')),
                ('mailing_list_initial_mitglieder', models.BooleanField(default=True, help_text='Member should be subscribed on the Mitglieder mailing list')),
                ('mailing_list_initial_mitglieder_announce', models.BooleanField(default=True, help_text='Member should be subscribed on the Mitglieder-announce mailing list')),
                ('membership_type', models.CharField(max_length=20, choices=[('full', 'Vollzahler'), ('reduced', 'ermässigt')])),
                ('membership_fee_monthly', models.DecimalField(decimal_places=2, max_digits=8, default=20, help_text='Monthly Membership Fee')),
                ('membership_fee_interval', models.PositiveIntegerField(help_text='Pays for N months at once', choices=[(1, '1'), (12, '12')])),
                ('active', models.BooleanField(default=True, help_text='Membership is active')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(related_name='members', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
