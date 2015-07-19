# coding=utf-8
import datetime

from django.conf import settings
from django.db import models
from localflavor.generic.models import IBANField, BICField


class Member(models.Model):

    class Meta:
        ordering = ('-created', )

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
        blank=True, null=True)

    form_of_address = models.CharField(
        choices=(('F', 'Frau'), ('H', 'Herr')),
        max_length=10,
        default="H",
        help_text="How to formally address this person")

    is_underaged = models.BooleanField(
        default=False,
        help_text="Member is not 18+.")

    date_of_birth = models.DateField(
        blank=True, null=True,)

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
        max_length=255,)

    country = models.CharField(
        max_length=255, default="Deutschland",)

    email = models.EmailField(
        max_length=255,)

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

    is_active = models.BooleanField(
        default=True,)

    is_cancellation_confirmed = models.BooleanField(
        default=False)

    payment_type = models.CharField(
        choices=(('SEPA', 'Lastschrift'),
                 ('transfer', 'Überweisung')),
        default="SEPA", max_length=20)

    iban = IBANField(null=True, blank=True, verbose_name="IBAN")
    bic = BICField(null=True, blank=True, verbose_name="BIC")

    iban_fullname = models.CharField(
        null=True, blank=True,
        max_length=255, verbose_name="IBAN full name",
        help_text="Full name for IBAN account owner")

    iban_address = models.CharField(
        null=True, blank=True,
        max_length=255, verbose_name="IBAN address",
        help_text="Address line (e.g. Street / House Number)")

    iban_zip_code = models.CharField(
        null=True, blank=True,
        max_length=20, verbose_name="IBAN zip code",
        help_text="ZIP Code")

    iban_city = models.CharField(
        null=True, blank=True,
        max_length=255, verbose_name="IBAN City",)

    iban_country = models.CharField(
        null=True, blank=True,
        max_length=255, default="Deutschland",
        verbose_name="IBAN Country",)

    is_welcome_mail_sent = models.BooleanField(
        default=False)

    is_payment_instruction_sent = models.BooleanField(
        default=False)

    is_registration_to_mailinglists_sent = models.BooleanField(
        default=False)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)

    def __str__(self):
        return "{} {} [ID: {}]".format(self.name, self.surname, self.member_id)

    def save(self, *args, **kwargs):
        if not self.member_id:
            self.member_id = (Member.objects.aggregate(models.Max('member_id'))
                              .get('member_id__max') or 0) + 1
        if not self.is_welcome_mail_sent:
            from .views import send_welcome_email
            send_welcome_email(self.email, self.__dict__)
            self.is_welcome_mail_sent = True
        if not self.is_registration_to_mailinglists_sent:
            from .utils import add_to_mailman
            add_to_mailman(self.email, self.mailing_list_initial_mitglieder)
            self.is_registration_to_mailinglists_sent = True
        if not self.is_payment_instruction_sent:
            from .views import send_payment_mail
            send_payment_mail(self.__dict__)
            self.is_payment_instruction_sent = True

        return super().save(*args, **kwargs)


class MembershipManager(models.Manager):
    pass


class Membership(models.Model):

    class Meta:
        ordering = ('-valid_from', )

    member = models.ForeignKey(Member)

    # FIXME: validator. no date before join_date
    valid_from = models.DateField()

    membership_type = models.CharField(
        choices=(('full', 'Vollzahler'),
                 ('reduced', 'ermässigt')),
        default="full", max_length=20)

    membership_fee_monthly = models.DecimalField(
        default=20,
        max_digits=8,
        decimal_places=2,)

    membership_fee_interval = models.PositiveIntegerField(
        choices=((1, '1'), (12, '12')), default=1,
        help_text="Pays for N months at once")

    objects = MembershipManager()

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)

    def __str__(self):
        return "{}: {} seit {}".format(self.member,
                                       self.membership_type,
                                       self.valid_from)

    def save(self, *args, **kwargs):
        # FIXME: fix all claims according to changed Memberships
        # FIXME: first valid_from MUST be join_date!
        return super().save(*args, **kwargs)


class AccountTransaction(models.Model):

    member = models.ForeignKey(Member)
    amount = models.DecimalField(max_digits=8,
                                 decimal_places=2)
    due_date = models.DateField(null=True, blank=True)
    booking_date = models.DateField(default=datetime.date.today)
    transaction_type = models.CharField(max_length=255,
                                        choices=(
                                            ('membership fee', 'Mitgliedsbeitrag'),
                                            ('donation', 'Spende'),
                                        ))
    booking_type = models.CharField(max_length=255,
                                    choices=(
                                        ('claim', 'Forderung'),
                                        ('deposit', 'Einzahlung'),
                                        ('credit', 'Gutschrift'),
                                    ))
    payment_reference = models.TextField()

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)

    def __str__(self):
        return "{}: {} {} [{}]".format(self.member,
                                       self.transaction_type,
                                       self.booking_type,
                                       self.booking_date)

    def save(self, *args, **kwargs):
        # claims are always negative. all others are positive
        self.amount = abs(self.amount)
        if self.booking_type == 'claim':
            self.amount = self.amount * -1
        return super().save(*args, **kwargs)
