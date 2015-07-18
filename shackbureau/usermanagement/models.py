# coding=utf-8
from django.conf import settings
from django.db import models
from localflavor.generic.models import IBANField, BICField


class Member(models.Model):

    member_id = models.IntegerField(
        unique=True,
        help_text="Membership ID")

    name = models.CharField(
        max_length=255,
        help_text="First/Given Name")

    surname = models.CharField(
        max_length=255,
        help_text="Last/Family Name")

    nickname = models.CharField(
        max_length=255,
        blank=True, null=True,
        help_text="Nickname")

    form_of_address = models.CharField(
        choices=(('F', 'Frau'), ('H', 'Herr')),
        max_length=10,
        help_text="How to formally address this person")

    is_underaged = models.BooleanField(
        default=False,
        help_text="Member is not 18+.")

    date_of_birth = models.DateField(
        blank=True, null=True,
        help_text="Date of Birth")

    address1 = models.CharField(
        max_length=255,
        help_text="Address line 1 (e.g. Street / House Number)")

    address2 = models.CharField(
        max_length=255,
        blank=True, null=True,
        help_text="Address line 2 (optional)")

    zip_code = models.CharField(
        max_length=20,
        help_text="ZIP Code")

    city = models.CharField(
        max_length=255,
        help_text="City")

    country = models.CharField(
        max_length=255, default="Deutschland",
        help_text="Country")

    email = models.EmailField(
        max_length=255,
        help_text="E-mail address")

    phone_number = models.CharField(
        max_length=32,
        blank=True, null=True)

    join_date = models.DateField(
        help_text="Member joined on this date")

    leave_date = models.DateField(
        null=True, blank=True,
        help_text="Member left on this date")

    mailing_list_initial_mitglieder = models.BooleanField(
        default=True,
        help_text="Member should be subscribed on the Mitglieder mailing list")

    mailing_list_initial_mitglieder_announce = models.BooleanField(
        default=True,
        help_text="Member should be subscribed on the Mitglieder-announce mailing list")

    membership_type = models.CharField(
        choices=(('full', 'Vollzahler'),
                 ('reduced', 'ermässigt')),
        max_length=20)

    membership_fee_monthly = models.DecimalField(
        default=20,
        max_digits=8,
        decimal_places=2,
        help_text="Monthly Membership Fee")

    membership_fee_interval = models.PositiveIntegerField(
        choices=((1, '1'), (12, '12')),
        help_text="Pays for N months at once")

    is_active = models.BooleanField(
        default=True,
        help_text="Membership is active")

    iban = IBANField(null=True, blank=True, verbose_name="IBAN")
    bic = BICField(null=True, blank=True, verbose_name="BIC")

    iban_fullname = models.CharField(
        max_length=255, verbose_name="IBAN full name",
        help_text="Full name for IBAN account owner")

    iban_address = models.CharField(
        max_length=255, verbose_name="IBAN address",
        help_text="Address line (e.g. Street / House Number)")

    iban_zip_code = models.CharField(
        max_length=20, verbose_name="IBAN zip code",
        help_text="ZIP Code")

    iban_city = models.CharField(
        max_length=255, verbose_name="IBAN City",
        help_text="City")

    iban_country = models.CharField(
        max_length=255, default="Deutschland", verbose_name="IBAN Country",
        help_text="Country")

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='members')

    def __unicode__(self):
        return u"%s, %s [%s]" % (self.surname, self.name, self.nickname or u"")
