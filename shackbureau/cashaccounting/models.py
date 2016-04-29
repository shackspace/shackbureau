from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone
from django.conf import settings

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

CASHNAME = 'Amount of {} {} {}'
class CashSet(models.Model):
    coin_001 = models.IntegerField(verbose_name=CASHNAME.format(1, 'Cent', 'coins'), default=0)
    coin_002 = models.IntegerField(verbose_name=CASHNAME.format(2, 'Cent', 'coins'), default=0)
    coin_005 = models.IntegerField(verbose_name=CASHNAME.format(5, 'Cent', 'coins'), default=0)
    coin_010 = models.IntegerField(verbose_name=CASHNAME.format(10, 'Cent', 'coins'), default=0)
    coin_020 = models.IntegerField(verbose_name=CASHNAME.format(20, 'Cent', 'coins'), default=0)
    coin_050 = models.IntegerField(verbose_name=CASHNAME.format(50, 'Cent', 'coins'), default=0)
    coin_100 = models.IntegerField(verbose_name=CASHNAME.format(1, 'Euro', 'coins'), default=0)
    coin_200 = models.IntegerField(verbose_name=CASHNAME.format(2, 'Euro', 'coins'), default=0)

    bill_005 = models.IntegerField(verbose_name=CASHNAME.format(5, 'Euro', 'bills'), default=0)
    bill_010 = models.IntegerField(verbose_name=CASHNAME.format(10, 'Euro', 'bills'), default=0)
    bill_020 = models.IntegerField(verbose_name=CASHNAME.format(20, 'Euro', 'bills'), default=0)
    bill_050 = models.IntegerField(verbose_name=CASHNAME.format(50, 'Euro', 'bills'), default=0)
    bill_100 = models.IntegerField(verbose_name=CASHNAME.format(100, 'Euro', 'bills'), default=0)
    bill_200 = models.IntegerField(verbose_name=CASHNAME.format(200, 'Euro', 'bills'), default=0)
    bill_500 = models.IntegerField(verbose_name=CASHNAME.format(500, 'Euro', 'bills'), default=0)

    value_mapping = {
        'coin_001': Decimal('0.01'),
        'coin_002': Decimal('0.02'),
        'coin_005': Decimal('0.05'),
        'coin_010': Decimal('0.10'),
        'coin_020': Decimal('0.20'),
        'coin_050': Decimal('0.50'),
        'coin_100': Decimal('1.00'),
        'coin_200': Decimal('2.00'),
        'bill_005': Decimal('5.00'),
        'bill_010': Decimal('10.00'),
        'bill_020': Decimal('20.00'),
        'bill_050': Decimal('50.00'),
        'bill_100': Decimal('100.00'),
        'bill_200': Decimal('200.00'),
        'bill_500': Decimal('500.00'),
    }

    def sum(self):
        return sum(getattr(self, attr) * value for attr, value in self.value_mapping)

    def __add__(self, other):
        result = {attr: getattr(self, attr) + getattr(other, attr) for attr in self.value_mapping}
        return CashSet(**result)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        result = {attr: getattr(self, attr) - getattr(other, attr) for attr in self.value_mapping}
        return CashSet(**result)

    def __str__(self):
        return 'CashSet of {}€'.format(self.sum())


class CashTransaction(models.Model):

    class Meta:
        ordering = ('-transaction_date', '-transaction_date_id')
        unique_together = (('transaction_date', 'transaction_date_id'), )

    transaction_id = models.IntegerField(verbose_name="id", unique=True)
    transaction_date = models.DateField()
    transaction_date_id = models.IntegerField(verbose_name="Transaction of the Day", default=1)
    description = models.CharField(max_length=255)
    is_stored_by_account = models.BooleanField(default=False)

    transaction_cash = models.ForeignKey(CashSet, ondelete=models.CASCADE, help_text='Transaction Cash Set')
    account_cash = models.ForeignKey(CashSet, ondelete=models.CASCADE, help_text='Account Cash Set')

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)

    objects = NoBulkOperationsManager()

    @property
    def transaction_sum(self):
        return self.transaction_cash.sum()

    @property
    def account_sum(self):
        return self.account_cash.sum()

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

    def get_negative_account_states(self):
        negative_account_states = dict()
        for attr in self.account_cash.value_mapping:
            if getattr(self.account_cash, attr) < 0:
                negative_account_states['account_{}'.format(attr)] = getattr(self.account_cash, attr)
        return negative_account_states

    def __str__(self):
        return "{} - {} [id:{}] {} ({} / {})".format(self.transaction_date,
                                                     self.transaction_date_id,
                                                     self.transaction_id,
                                                     self.description,
                                                     self.account_cash.sum(),
                                                     self.transaction_cash.sum())

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = (CashTransaction.objects.aggregate(models.Max('transaction_id'))
                                   .get('transaction_id__max') or 0) + 1

        previous_cashtransaction = self.get_previous_cashtransaction()
        if self.is_stored_by_account:
            if previous_cashtransaction:
                self.transaction_cash = self.account_cash - previous_cashtransaction.account_cash
            else:
                self.transaction_cash = self.account_cash
        else:
            if previous_cashtransaction:
                self.account_cash = previous_cashtransaction.account_cash + self.transaction_cash
            else:
                self.account_cash = self.transaction_cash

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
        ret = super().delete(*args, **kwargs)
        next_cashtransaction = self.get_next_cashtransaction()
        if next_cashtransaction:
            next_cashtransaction.save()
        return ret


class CashAccountingExport(models.Model):
    class Meta:
        ordering = ('-year', )

    year = models.PositiveIntegerField(unique=True)
    data_file = models.FileField(upload_to='cashaccounting_export',
                                 verbose_name="Export file",
                                 null=True,
                                 blank=True)
    data_file_date = models.DateTimeField(verbose_name="Timestamp of export file",
                                          null=True,
                                          blank=True)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)

    objects = NoBulkOperationsManager()

    def update_export_file(self):
        from .utils import export_cashaccounting_csv
        from django.core.files.base import ContentFile
        if not self.data_file:
            self.data_file = ContentFile("")
            self.data_file.name = "cashaccounting_export_{}.csv".format(self.year)
        export_file = export_cashaccounting_csv(self.year, self.data_file)
        self.data_file_date = timezone.now()
        self.data_file = export_file

    def save(self, *args, **kwargs):
        self.update_export_file()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.data_file:
            import os
            try:
                os.remove(self.data_file.path)
            except FileNotFoundError:
                pass
        return super().delete(*args, **kwargs)
