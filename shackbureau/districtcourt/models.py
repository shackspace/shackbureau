import datetime

from django.db import models
from django.conf import settings


class Debitor(models.Model):
    class Meta:
        ordering = ('-created', )

    debitor_id = models.IntegerField(
        unique=True,
        help_text="Debitor ID")

    comment = models.TextField(
        blank=True,
        null=True)

    districtcourt = models.CharField(
        choices=(('reutlingen', 'Amtsgericht Reutlingen'), ),
        max_length=10,
        default="reutlingen",)

    date_of_receipt = models.DateField()

    record_token = models.CharField(
        max_length=255,
        help_text="Aktenzeichen")

    record_token_line_2 = models.CharField(
        max_length=255,
        help_text="Aktenzeichen Zeile 2",
        blank=True, null=True)

    name = models.CharField(
        max_length=255,)

    debt_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,)

    due_date = models.DateField()

    is_done = models.BooleanField(
        default=False,)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)

    def __str__(self):
        return "{}, {} [ID: {}]".format(self.name,
                                        self.record_token,
                                        self.debitor_id)

    def save(self, *args, **kwargs):
        if not self.debitor_id:
            self.debitor_id = (Debitor.objects.aggregate(models.Max('debitor_id'))
                               .get('debitor_id__max') or 0) + 1
        ret = super().save(*args, **kwargs)

        accounttransaction, created = DistrictcourtAccountTransaction.objects.get_or_create(
            debitor=self,
            booking_type='districtcourt_claim',
            defaults={'amount': - self.debt_amount,
                      'due_date': self.date_of_receipt,
                      'created_by': self.created_by}
        )
        accounttransaction.amount = - self.debt_amount
        accounttransaction.due_date = self.date_of_receipt
        accounttransaction.payment_reference = "debt defined by districtcourt {}".format(self.districtcourt)
        accounttransaction.save()
        return ret


class DistrictcourtAccountTransaction(models.Model):

    class Meta:
        ordering = ('-due_date', )

    debitor = models.ForeignKey(Debitor)
    amount = models.DecimalField(max_digits=8,
                                 decimal_places=2)
    due_date = models.DateField()
    booking_date = models.DateField(default=datetime.date.today)
    booking_type = models.CharField(max_length=255,
                                    choices=(
                                        ('claim', 'Forderung'),
                                        ('districtcourt_claim', 'Automatische Forderung des Amtsgericht'),
                                        ('deposit', 'Einzahlung'),
                                        ('credit', 'Gutschrift'),
                                    ))
    payment_reference = models.TextField()
    transaction_hash = models.TextField(null=True, blank=True)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)

    def __str__(self):
        return "{}: {} [{}]".format(self.debitor,
                                    self.booking_type,
                                    self.due_date)

    def save(self, *args, **kwargs):
        # claims are always negative. all others are positive
        self.amount = abs(self.amount)
        if 'claim' in self.booking_type:
            self.amount = self.amount * -1
        return super().save(*args, **kwargs)
