from django.db import models
from django.db.models import Q
from django.conf import settings
from django.db.models.query import QuerySet

from decimal import Decimal


class NoBulkOperationsQuerySet(QuerySet):
    def delete(self):
        for obj in self:
            obj.delete()

    def update(self, *args, **kwargs):
        ret = super(NoBulkOperationsQuerySet, self).update(*args, **kwargs)
        for obj in self:
            obj.save()
        return ret

    def update_or_create(self, *args, **kwargs):
        obj, created = super(NoBulkOperationsQuerySet, self).update_or_create(*args, **kwargs)
        obj.save()
        return obj, created

    def bulk_create(self, objs, batch_size=None):
        # new_objs = super(NoBulkOperationsQuerySet, self).bulk_create(objs, batch_size=batch_size)
        for obj in objs:
            obj.save()
        return objs


class NoBulkOperationsManager(models.Manager):
    def get_queryset(self):
        return NoBulkOperationsQuerySet(self.model)


class CashTransaction(models.Model):

    class Meta:
        ordering = ('-transaction_date', '-transaction_date_id')
        unique_together = (('transaction_date', 'transaction_date_id'), )

    transaction_id = models.IntegerField(verbose_name="id", unique=True)

    transaction_date = models.DateField()

    transaction_date_id = models.IntegerField(verbose_name="Transaction of the Day", default=1)

    description = models.CharField(max_length=255)

    is_stored_by_account = models.BooleanField(default=False)

    transaction_coin_001 = models.IntegerField(help_text="amount of 1 cent coins",
                                               verbose_name="transaction 1 cent",
                                               default=0)
    transaction_coin_002 = models.IntegerField(help_text="amount of 2 cent coins",
                                               verbose_name="transaction 2 cent",
                                               default=0)
    transaction_coin_005 = models.IntegerField(help_text="amount of 5 cent coins",
                                               verbose_name="transaction 5 cent",
                                               default=0)
    transaction_coin_010 = models.IntegerField(help_text="amount of 10 cent coins",
                                               verbose_name="transaction 10 cent",
                                               default=0)
    transaction_coin_020 = models.IntegerField(help_text="amount of 20 cent coins",
                                               verbose_name="transaction 20 cent",
                                               default=0)
    transaction_coin_050 = models.IntegerField(help_text="amount of 50 cent coins",
                                               verbose_name="transaction 50 cent",
                                               default=0)
    transaction_coin_100 = models.IntegerField(help_text="amount of 1 euro coins",
                                               verbose_name="transaction 1 euro",
                                               default=0)
    transaction_coin_200 = models.IntegerField(help_text="amount of 2 euro coins",
                                               verbose_name="transaction 2 euro",
                                               default=0)

    transaction_bill_005 = models.IntegerField(help_text="amount of 5 euro bills",
                                               verbose_name="transaction 5 euro",
                                               default=0)
    transaction_bill_010 = models.IntegerField(help_text="amount of 10 euro bills",
                                               verbose_name="transaction 10 euro",
                                               default=0)
    transaction_bill_020 = models.IntegerField(help_text="amount of 20 euro bills",
                                               verbose_name="transaction 20 euro",
                                               default=0)
    transaction_bill_050 = models.IntegerField(help_text="amount of 50 euro bills",
                                               verbose_name="transaction 50 euro",
                                               default=0)
    transaction_bill_100 = models.IntegerField(help_text="amount of 100 euro bills",
                                               verbose_name="transaction 100 euro",
                                               default=0)
    transaction_bill_200 = models.IntegerField(help_text="amount of 200 euro bills",
                                               verbose_name="transaction 200 euro",
                                               default=0)
    transaction_bill_500 = models.IntegerField(help_text="amount of 500 euro bills",
                                               verbose_name="transaction 500 euro",
                                               default=0)

    account_coin_001 = models.IntegerField(help_text="amount of 1 cent coins",
                                           verbose_name="account 1 cent",
                                           default=0)
    account_coin_002 = models.IntegerField(help_text="amount of 2 cent coins",
                                           verbose_name="account 2 cent",
                                           default=0)
    account_coin_005 = models.IntegerField(help_text="amount of 5 cent coins",
                                           verbose_name="account 5 cent",
                                           default=0)
    account_coin_010 = models.IntegerField(help_text="amount of 10 cent coins",
                                           verbose_name="account 10 cent",
                                           default=0)
    account_coin_020 = models.IntegerField(help_text="amount of 20 cent coins",
                                           verbose_name="account 20 cent",
                                           default=0)
    account_coin_050 = models.IntegerField(help_text="amount of 50 cent coins",
                                           verbose_name="account 50 cent",
                                           default=0)
    account_coin_100 = models.IntegerField(help_text="amount of 1 euro coins",
                                           verbose_name="account 1 euro",
                                           default=0)
    account_coin_200 = models.IntegerField(help_text="amount of 2 euro coins",
                                           verbose_name="account 2 euro",
                                           default=0)

    account_bill_005 = models.IntegerField(help_text="amount of 5 euro bills",
                                           verbose_name="account 5 euro",
                                           default=0)
    account_bill_010 = models.IntegerField(help_text="amount of 10 euro bills",
                                           verbose_name="account 10 euro",
                                           default=0)
    account_bill_020 = models.IntegerField(help_text="amount of 20 euro bills",
                                           verbose_name="account 20 euro",
                                           default=0)
    account_bill_050 = models.IntegerField(help_text="amount of 50 euro bills",
                                           verbose_name="account 50 euro",
                                           default=0)
    account_bill_100 = models.IntegerField(help_text="amount of 100 euro bills",
                                           verbose_name="account 100 euro",
                                           default=0)
    account_bill_200 = models.IntegerField(help_text="amount of 200 euro bills",
                                           verbose_name="account 200 euro",
                                           default=0)
    account_bill_500 = models.IntegerField(help_text="amount of 500 euro bills",
                                           verbose_name="account 500 euro",
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

    objects = NoBulkOperationsManager()

    def get_previous_cashtransaction(self):
        return CashTransaction.objects.exclude(id=self.id) \
            .filter(Q(transaction_date__lt=self.transaction_date) |
                    Q(transaction_date=self.transaction_date,
                      transaction_date_id__lt=self.transaction_date_id)) \
            .order_by("transaction_date", "transaction_date_id").last()

    def get_next_cashtransaction(self):
        return CashTransaction.objects.exclude(id=self.id) \
            .filter(Q(transaction_date__gt=self.transaction_date) |
                    Q(transaction_date=self.transaction_date,
                      transaction_date_id__gt=self.transaction_date_id)) \
            .order_by("transaction_date", "transaction_date_id").first()

    def __str__(self):
        return "{} - {} [id:{}] {} ({} / {})".format(self.transaction_date,
                                                     self.transaction_date_id,
                                                     self.transaction_id,
                                                     self.description,
                                                     self.account_sum,
                                                     self.transaction_sum)

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = (CashTransaction.objects.aggregate(models.Max('transaction_id'))
                                   .get('transaction_id__max') or 0) + 1

        previous_cashtransaction = self.get_previous_cashtransaction()
        if self.is_stored_by_account:
            if previous_cashtransaction:
                self.transaction_coin_001 = self.account_coin_001 - previous_cashtransaction.account_coin_001
                self.transaction_coin_002 = self.account_coin_002 - previous_cashtransaction.account_coin_002
                self.transaction_coin_005 = self.account_coin_005 - previous_cashtransaction.account_coin_005
                self.transaction_coin_010 = self.account_coin_010 - previous_cashtransaction.account_coin_010
                self.transaction_coin_020 = self.account_coin_020 - previous_cashtransaction.account_coin_020
                self.transaction_coin_050 = self.account_coin_050 - previous_cashtransaction.account_coin_050
                self.transaction_coin_100 = self.account_coin_100 - previous_cashtransaction.account_coin_100
                self.transaction_coin_200 = self.account_coin_200 - previous_cashtransaction.account_coin_200
                self.transaction_bill_005 = self.account_bill_005 - previous_cashtransaction.account_bill_005
                self.transaction_bill_010 = self.account_bill_010 - previous_cashtransaction.account_bill_010
                self.transaction_bill_020 = self.account_bill_020 - previous_cashtransaction.account_bill_020
                self.transaction_bill_050 = self.account_bill_050 - previous_cashtransaction.account_bill_050
                self.transaction_bill_100 = self.account_bill_100 - previous_cashtransaction.account_bill_100
                self.transaction_bill_200 = self.account_bill_200 - previous_cashtransaction.account_bill_200
                self.transaction_bill_500 = self.account_bill_500 - previous_cashtransaction.account_bill_500
            else:
                self.transaction_coin_001 = self.account_coin_001
                self.transaction_coin_002 = self.account_coin_002
                self.transaction_coin_005 = self.account_coin_005
                self.transaction_coin_010 = self.account_coin_010
                self.transaction_coin_020 = self.account_coin_020
                self.transaction_coin_050 = self.account_coin_050
                self.transaction_coin_100 = self.account_coin_100
                self.transaction_coin_200 = self.account_coin_200
                self.transaction_bill_005 = self.account_bill_005
                self.transaction_bill_010 = self.account_bill_010
                self.transaction_bill_020 = self.account_bill_020
                self.transaction_bill_050 = self.account_bill_050
                self.transaction_bill_100 = self.account_bill_100
                self.transaction_bill_200 = self.account_bill_200
                self.transaction_bill_500 = self.account_bill_500
        else:
            if previous_cashtransaction:
                self.account_coin_001 = previous_cashtransaction.account_coin_001 + self.transaction_coin_001
                self.account_coin_002 = previous_cashtransaction.account_coin_002 + self.transaction_coin_002
                self.account_coin_005 = previous_cashtransaction.account_coin_005 + self.transaction_coin_005
                self.account_coin_010 = previous_cashtransaction.account_coin_010 + self.transaction_coin_010
                self.account_coin_020 = previous_cashtransaction.account_coin_020 + self.transaction_coin_020
                self.account_coin_050 = previous_cashtransaction.account_coin_050 + self.transaction_coin_050
                self.account_coin_100 = previous_cashtransaction.account_coin_100 + self.transaction_coin_100
                self.account_coin_200 = previous_cashtransaction.account_coin_200 + self.transaction_coin_200
                self.account_bill_005 = previous_cashtransaction.account_bill_005 + self.transaction_bill_005
                self.account_bill_010 = previous_cashtransaction.account_bill_010 + self.transaction_bill_010
                self.account_bill_020 = previous_cashtransaction.account_bill_020 + self.transaction_bill_020
                self.account_bill_050 = previous_cashtransaction.account_bill_050 + self.transaction_bill_050
                self.account_bill_100 = previous_cashtransaction.account_bill_100 + self.transaction_bill_100
                self.account_bill_200 = previous_cashtransaction.account_bill_200 + self.transaction_bill_200
                self.account_bill_500 = previous_cashtransaction.account_bill_500 + self.transaction_bill_500
            else:
                self.account_coin_001 = self.transaction_coin_001
                self.account_coin_002 = self.transaction_coin_002
                self.account_coin_005 = self.transaction_coin_005
                self.account_coin_010 = self.transaction_coin_010
                self.account_coin_020 = self.transaction_coin_020
                self.account_coin_050 = self.transaction_coin_050
                self.account_coin_100 = self.transaction_coin_100
                self.account_coin_200 = self.transaction_coin_200
                self.account_bill_005 = self.transaction_bill_005
                self.account_bill_010 = self.transaction_bill_010
                self.account_bill_020 = self.transaction_bill_020
                self.account_bill_050 = self.transaction_bill_050
                self.account_bill_100 = self.transaction_bill_100
                self.account_bill_200 = self.transaction_bill_200
                self.account_bill_500 = self.transaction_bill_500

        self.transaction_sum = self.transaction_coin_001 * Decimal("0.01") + \
            self.transaction_coin_002 * Decimal("0.02") + \
            self.transaction_coin_005 * Decimal("0.05") + \
            self.transaction_coin_010 * Decimal("0.10") + \
            self.transaction_coin_020 * Decimal("0.20") + \
            self.transaction_coin_050 * Decimal("0.50") + \
            self.transaction_coin_100 * Decimal("1.00") + \
            self.transaction_coin_200 * Decimal("2.00") + \
            self.transaction_bill_005 * Decimal("5.00") + \
            self.transaction_bill_010 * Decimal("10.00") + \
            self.transaction_bill_020 * Decimal("20.00") + \
            self.transaction_bill_050 * Decimal("50.00") + \
            self.transaction_bill_100 * Decimal("100.00") + \
            self.transaction_bill_200 * Decimal("200.00") + \
            self.transaction_bill_500 * Decimal("500.00")

        if previous_cashtransaction:
            self.account_sum = previous_cashtransaction.account_sum + self.transaction_sum
        else:
            self.account_sum = self.transaction_sum

        if self.pk:
            old_next_cashtransaction = CashTransaction.objects.get(id=self.id).get_next_cashtransaction()
        else:
            old_next_cashtransaction = None

        ret = super().save(*args, **kwargs)

        # update CashTransaction recursive
        next_cashtransaction = self.get_next_cashtransaction()
        if old_next_cashtransaction:
            if not next_cashtransaction:
                old_next_cashtransaction.save()
                return ret
            if old_next_cashtransaction.transaction_date < next_cashtransaction.transaction_date:
                old_next_cashtransaction.save()
                return ret
            if next_cashtransaction.transaction_date < old_next_cashtransaction.transaction_date:
                next_cashtransaction.save()
                return ret
            if next_cashtransaction.transaction_date == old_next_cashtransaction.transaction_date:
                if old_next_cashtransaction.transaction_date_id < next_cashtransaction.transaction_date_id:
                    old_next_cashtransaction.save()
                    return ret
                else:
                    next_cashtransaction.save()
                    return ret
                return ret
            old_next_cashtransaction.save()
        if next_cashtransaction:
            next_cashtransaction.save()
            return ret
        return ret

    def delete(self, *args, **kwargs):
        print("delete")
        ret = super().delete(*args, **kwargs)
        next_cashtransaction = self.get_next_cashtransaction()
        if next_cashtransaction:
            print(next_cashtransaction)
            next_cashtransaction.save()
        return ret
