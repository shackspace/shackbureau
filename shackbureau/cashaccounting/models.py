from django.db import models
from django.conf import settings

from decimal import Decimal


class CashTransaction(models.Model):

    class Meta:
        ordering = ('-transaction_date', )

    transaction_id = models.IntegerField(verbose_name="id", unique=True)

    transaction_date = models.DateField(unique=True)

    description = models.CharField(max_length=255)

    coin_001 = models.IntegerField(help_text="amount of 1 cent coins",
                                   verbose_name="1 cent",
                                   default=0)
    coin_002 = models.IntegerField(help_text="amount of 2 cent coins",
                                   verbose_name="2 cent",
                                   default=0)
    coin_005 = models.IntegerField(help_text="amount of 5 cent coins",
                                   verbose_name="5 cent",
                                   default=0)
    coin_010 = models.IntegerField(help_text="amount of 10 cent coins",
                                   verbose_name="10 cent",
                                   default=0)
    coin_020 = models.IntegerField(help_text="amount of 20 cent coins",
                                   verbose_name="20 cent",
                                   default=0)
    coin_050 = models.IntegerField(help_text="amount of 50 cent coins",
                                   verbose_name="50 cent",
                                   default=0)
    coin_100 = models.IntegerField(help_text="amount of 1 euro coins",
                                   verbose_name="1 euro",
                                   default=0)
    coin_200 = models.IntegerField(help_text="amount of 2 euro coins",
                                   verbose_name="2 euro",
                                   default=0)

    bill_005 = models.IntegerField(help_text="amount of 5 euro bills",
                                   verbose_name="5 euro",
                                   default=0)
    bill_010 = models.IntegerField(help_text="amount of 10 euro bills",
                                   verbose_name="10 euro",
                                   default=0)
    bill_020 = models.IntegerField(help_text="amount of 20 euro bills",
                                   verbose_name="20 euro",
                                   default=0)
    bill_050 = models.IntegerField(help_text="amount of 50 euro bills",
                                   verbose_name="50 euro",
                                   default=0)
    bill_100 = models.IntegerField(help_text="amount of 100 euro bills",
                                   verbose_name="100 euro",
                                   default=0)
    bill_200 = models.IntegerField(help_text="amount of 200 euro bills",
                                   verbose_name="200 euro",
                                   default=0)
    bill_500 = models.IntegerField(help_text="amount of 500 euro bills",
                                   verbose_name="500 euro",
                                   default=0)

    transaction_sum = models.DecimalField(
        max_digits=8,
        decimal_places=2,)

    account_sum = models.DecimalField(
        max_digits=8,
        decimal_places=2,)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)

    def __str__(self):
        return "{} [id:{}] {} ({})".format(self.transaction_date,
                                           self.transaction_id,
                                           self.description,
                                           self.transaction_sum)

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = (CashTransaction.objects.aggregate(models.Max('transaction_id'))
                                   .get('transaction_id__max') or 0) + 1
        self.transaction_sum = self.coin_001 * Decimal("0.01") + \
            self.coin_002 * Decimal("0.02") + \
            self.coin_005 * Decimal("0.05") + \
            self.coin_010 * Decimal("0.10") + \
            self.coin_020 * Decimal("0.20") + \
            self.coin_050 * Decimal("0.50") + \
            self.coin_100 * Decimal("1.00") + \
            self.coin_200 * Decimal("2.00") + \
            self.bill_005 * Decimal("5.00") + \
            self.bill_010 * Decimal("10.00") + \
            self.bill_020 * Decimal("20.00") + \
            self.bill_050 * Decimal("50.00") + \
            self.bill_100 * Decimal("100.00") + \
            self.bill_200 * Decimal("200.00") + \
            self.bill_500 * Decimal("500.00")

        self.account_sum = (CashTransaction.objects.filter(transaction_date__lt=self.transaction_date)
                            .aggregate(models.Sum('transaction_sum')).get("transaction_sum__sum") or 0) \
            + self.transaction_sum

        ret = super().save(*args, **kwargs)

        # update later CashTransaction recursive
        next_cashtransaction = CashTransaction.objects.filter(transaction_date__gt=self.transaction_date) \
            .order_by("transaction_date").first()
        if next_cashtransaction:
            next_cashtransaction.save()

        return ret
