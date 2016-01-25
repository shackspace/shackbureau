# coding=utf-8
import datetime
import uuid

from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from localflavor.generic.models import IBANField, BICField
from django.db.models import Q


class MemberManager(models.Manager):
    def get_active_members(self, date):
        return self.filter(join_date__lte=date)\
                   .filter(Q(is_active=True) | Q(leave_date__gt=date))\
                   .order_by("member_id")


class Member(models.Model):

    class Meta:
        ordering = ('-created', )

    member_id = models.IntegerField(
        unique=True,
        help_text="Membership ID")

    comment = models.TextField(blank=True, null=True)
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
        help_text="Member joined on this date. The date is forced to the begin of given month.")

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

    iban_issue_date = models.DateField(
        null=True, blank=True,
        verbose_name="IBAN Issue Date",
        help_text="The issue date of the direct debit mandate")

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

    is_cancellation_mail_sent_to_cashmaster = models.BooleanField(
        default=False)

    objects = MemberManager()

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)

    def __str__(self):
        if self.nickname:
            return "{}, {} ({}) [ID: {}]".format(self.surname, self.name, self.nickname, self.member_id)

        return "{}, {} [ID: {}]".format(self.surname, self.name, self.member_id)

    def save(self, *args, **kwargs):
        if not self.member_id:
            self.member_id = (Member.objects.aggregate(models.Max('member_id'))
                              .get('member_id__max') or 0) + 1
        if self.join_date and not self.join_date.day == 1:
            self.join_date = self.join_date.replace(day=1)
        if self.is_cancellation_confirmed:
            # if the membership is cancelled the member isn't active anymore
            self.is_active = False
            # send mail to cashmaster if member cancelled and uses SEPA
            # but only if mail not already sent
            if not self.is_cancellation_mail_sent_to_cashmaster and self.payment_type == 'SEPA':
                from .views import send_cancellation_mail_to_cashmaster
                send_cancellation_mail_to_cashmaster(self.__dict__)
                self.is_cancellation_mail_sent_to_cashmaster = True
        if not self.is_welcome_mail_sent:
            from .views import send_welcome_email
            send_welcome_email(self.email, self.__dict__)
            self.is_welcome_mail_sent = True
        if not self.is_registration_to_mailinglists_sent:
            from .utils import add_to_mailman
            add_to_mailman(self.email, self.mailing_list_initial_mitglieder)
            self.is_registration_to_mailinglists_sent = True
        if not self.is_payment_instruction_sent:
            from .views import send_payment_email
            send_payment_email(self.__dict__)
            self.is_payment_instruction_sent = True

        return super().save(*args, **kwargs)

    def get_ssh_public_key(self):
        memberspecials = self.memberspecials_set.first()
        if memberspecials:
            return memberspecials.ssh_public_key
        return None

    def get_nickname(self):
        if self.nickname:
            return self.nickname
        return "{} {}.".format(self.name, self.surname[:2])


class MembershipManager(models.Manager):

    def get_current_membership(self, member, date):
        return self.filter(member=member)\
                   .filter(valid_from__lte=date)\
                   .order_by("-valid_from").first()

    def fix_or_create_claims(self, member):
        for year in range(2015, datetime.date.today().year + 1 + 1):
            for month in range(1, 12 + 1):
                current_day = datetime.date(year, month, 1)
                membership = self.get_current_membership(member, current_day)
                if not membership:
                    AccountTransaction.objects.filter(member=member)\
                                              .filter(booking_type='fee_claim')\
                                              .filter(due_date=current_day).delete()
                    continue

                if member.leave_date and member.leave_date.year == year:
                    if month + 1 > member.leave_date.month:
                        AccountTransaction.objects.filter(member=member)\
                                                  .filter(booking_type='fee_claim')\
                                                  .filter(due_date=current_day).delete()
                        continue
                if member.leave_date and member.leave_date.year < year:
                    AccountTransaction.objects.filter(member=member)\
                                              .filter(booking_type='fee_claim')\
                                              .filter(due_date=current_day).delete()
                    continue
                defaults = {
                    'transaction_type': 'membership fee',
                    'amount': membership.membership_fee_monthly,
                    'created_by': User.objects.first(),
                    'payment_reference': 'Mitgliedsbeitragsforderung {}/{} ID {}'.format(
                        month, year, member.member_id
                    )
                }
                AccountTransaction.objects.update_or_create(
                    booking_type='fee_claim',
                    member=member,
                    due_date=datetime.date(year, month, 1),
                    defaults=defaults)


class Membership(models.Model):

    class Meta:
        ordering = ('-valid_from', )
        unique_together = (('member' ,'valid_from') )

    member = models.ForeignKey(Member)

    # FIXME: validator. no date before join_date
    valid_from = models.DateField(
        help_text="Membership starts on this date. The date is forced to the begin of given month.")

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
        if self.valid_from and not self.valid_from.day == 1:
            self.valid_from = self.valid_from.replace(day=1)
        # if self.valid_from and not self.valid_from.day == 1:
        #     self.valid_from = self.valid_from.replace(day=1)
        # FIXME: first valid_from MUST be join_date!
        result = super().save(*args, **kwargs)
        Membership.objects.fix_or_create_claims(self.member)
        return result


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
                                        ('fee_claim', 'Forderung (automatischer Mitgliedsbeitrag)'),
                                        ('deposit', 'Einzahlung'),
                                        ('credit', 'Gutschrift'),
                                    ))
    payment_reference = models.TextField()
    transaction_hash = models.TextField(null=True, blank=True)
    send_nagging_mail = models.BooleanField(default=False)

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
        if 'claim' in self.booking_type:
            self.amount = self.amount * -1
        if self.send_nagging_mail:
            from .views import send_nagging_email
            send_nagging_email(self.member.email, self.member.__dict__)
            self.send_nagging_mail = False
        return super().save(*args, **kwargs)


class BankTransactionUpload(models.Model):
    data_file = models.FileField(upload_to='bank_transaction_uploads')
    status = models.CharField(choices=(('new', 'New'),
                                       ('wip', 'Work in progress'),
                                       ('done', 'Imported'),
                                       ('fail', 'Could not import')),
                              default='new', max_length=10)
    data_type = models.CharField(max_length=255,
                                 choices=(
                                     ('bank_csv', 'Bank [CSV]'),
                                     ('accountant_csv', 'Accountant [CSV]'),
                                 ))

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)

    def __str__(self):
        return "Uploads <{data_file}>".format(
            data_file=self.data_file)

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        if self.status == 'new':
            from .utils import TransactionLogProcessor
            TransactionLogProcessor().process(self)
        return result


class BankTransactionLog(models.Model):
    upload = models.ForeignKey("BankTransactionUpload")
    reference = models.TextField()
    member = models.ForeignKey("Member", null=True, blank=True)
    is_matched = models.BooleanField(default=True)
    is_resolved = models.BooleanField(default=True)
    score = models.IntegerField()
    error = models.TextField(null=True, blank=True)
    transaction_owner = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=8,
                                 decimal_places=2)
    booking_date = models.DateField(default=datetime.date.today)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)

    def __str__(self):
        return "Log <{upload} / {member} / {interaction}>".format(
            upload=self.upload, member=self.member,
            interaction=self.is_matched)


class MemberSpecials(models.Model):
    member = models.ForeignKey("Member")
    has_matomat_key = models.BooleanField(default=False)
    has_snackomat_key = models.BooleanField(default=False)
    has_metro_card = models.BooleanField(default=False)
    has_selgros_card = models.BooleanField(default=False)
    has_shack_iron_key = models.BooleanField(default=False)
    is_keyholder = models.BooleanField(default=False)
    has_safe_key = models.BooleanField(default=False)
    has_loeffelhardt_account = models.BooleanField(default=False)
    signed_DSV = models.BooleanField(default=False)
    ssh_public_key = models.TextField(null=True, blank=True)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)

    class Meta:
        verbose_name = "Member Specials"
        verbose_name_plural = "Member Specials"

    def __str__(self):
        return "{member} keyholder: {is_keyholder}".format(
            member=self.member,
            is_keyholder=self.is_keyholder)

    def save(self, *args, **kwargs):
        if self.ssh_public_key:
            # format ssh-key in on line seperated by one whitespace
            self.ssh_public_key = " ".join(self.ssh_public_key.strip().split())

        return super().save(*args, **kwargs)


class MemberTrackingCode(models.Model):
    """ uuid to use in tracking urls in emails
    """
    member = models.ForeignKey("Member")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    validated = models.BooleanField(default=False)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)


class Balance:
    """ calculated balance for given user per year
    """
    member = models.ForeignKey("Member")
    balance = models.DecimalField(max_digits=8,
                                  decimal_places=2)
    year = models.PositiveIntegerField()

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)
