# coding=utf-8
import pytest
from django.db.models import Q, Sum
from decimal import Decimal
from cashaccounting.models import CashTransaction
from datetime import date


@pytest.mark.django_db
class TestMember:

    def test_transaction_sum(self, cashtransaction_fixture_1, cashtransaction_fixture_2,
                             cashtransaction_fixture_3, cashtransaction_fixture_4):
        self.validate_cashtransactions()

    def test_transaction_reorder(self, cashtransaction_fixture_1, cashtransaction_fixture_2,
                                 cashtransaction_fixture_3, cashtransaction_fixture_4):
        new_date = date(2016, 2, 5)
        order = [3, 4, 2, 1]
        cashtransaction_fixture_1.transaction_date = new_date
        cashtransaction_fixture_1.transaction_date_id = order[0]
        cashtransaction_fixture_1.save()
        self.validate_cashtransactions()
        cashtransaction_fixture_2.transaction_date = new_date
        cashtransaction_fixture_2.transaction_date_id = order[1]
        cashtransaction_fixture_2.save()
        self.validate_cashtransactions()
        cashtransaction_fixture_3.transaction_date = new_date
        cashtransaction_fixture_3.transaction_date_id = order[2]
        cashtransaction_fixture_3.save()
        self.validate_cashtransactions()
        cashtransaction_fixture_4.transaction_date = new_date
        cashtransaction_fixture_4.transaction_date_id = order[3]
        cashtransaction_fixture_4.save()
        self.validate_cashtransactions()

    def test_transaction_delete_first(self, cashtransaction_fixture_1, cashtransaction_fixture_2,
                                      cashtransaction_fixture_3, cashtransaction_fixture_4):
        for _ in range(4):
            CashTransaction.objects.order_by('transaction_date', 'transaction_date_id').first().delete()
            self.validate_cashtransactions()

    def test_transaction_delete_last(self, cashtransaction_fixture_1, cashtransaction_fixture_2,
                                     cashtransaction_fixture_3, cashtransaction_fixture_4):
        for _ in range(4):
            CashTransaction.objects.order_by('transaction_date', 'transaction_date_id').last().delete()
            self.validate_cashtransactions()

    def validate_cashtransactions(self):
        cashtransaction = CashTransaction.objects.order_by('transaction_date', 'transaction_date_id').first()
        ctr = 0
        while cashtransaction:
            # test consitence of transaction_sum und transaction coins and bills
            assert cashtransaction.transaction_sum == sum([cashtransaction.transaction_coin_001 * Decimal("0.01"),
                                                           cashtransaction.transaction_coin_002 * Decimal("0.02"),
                                                           cashtransaction.transaction_coin_005 * Decimal("0.05"),
                                                           cashtransaction.transaction_coin_010 * Decimal("0.10"),
                                                           cashtransaction.transaction_coin_020 * Decimal("0.20"),
                                                           cashtransaction.transaction_coin_050 * Decimal("0.50"),
                                                           cashtransaction.transaction_coin_100 * Decimal("1.00"),
                                                           cashtransaction.transaction_coin_200 * Decimal("2.00"),
                                                           cashtransaction.transaction_bill_005 * Decimal("5.00"),
                                                           cashtransaction.transaction_bill_010 * Decimal("10.00"),
                                                           cashtransaction.transaction_bill_020 * Decimal("20.00"),
                                                           cashtransaction.transaction_bill_050 * Decimal("50.00"),
                                                           cashtransaction.transaction_bill_100 * Decimal("100.00"),
                                                           cashtransaction.transaction_bill_200 * Decimal("200.00"),
                                                           cashtransaction.transaction_bill_500 * Decimal("500.00"),
                                                           ])
            # get account sums based on all previous Cashtransactions
            aggregate = CashTransaction.objects.filter(
                Q(transaction_date__lt=cashtransaction.transaction_date) |
                Q(transaction_date=cashtransaction.transaction_date,
                  transaction_date_id__lte=cashtransaction.transaction_date_id)) \
                .aggregate(Sum('transaction_sum'),
                           Sum('transaction_coin_001'),
                           Sum('transaction_coin_002'),
                           Sum('transaction_coin_005'),
                           Sum('transaction_coin_010'),
                           Sum('transaction_coin_020'),
                           Sum('transaction_coin_050'),
                           Sum('transaction_coin_100'),
                           Sum('transaction_coin_200'),
                           Sum('transaction_bill_005'),
                           Sum('transaction_bill_010'),
                           Sum('transaction_bill_020'),
                           Sum('transaction_bill_050'),
                           Sum('transaction_bill_100'),
                           Sum('transaction_bill_200'),
                           Sum('transaction_bill_500'),
                           )

            # test aggregated sums of older transaction versus sums in cashtransaction
            assert cashtransaction.account_sum == aggregate.get('transaction_sum__sum')
            assert cashtransaction.account_coin_001 == aggregate.get('transaction_coin_001__sum')
            assert cashtransaction.account_coin_002 == aggregate.get('transaction_coin_002__sum')
            assert cashtransaction.account_coin_005 == aggregate.get('transaction_coin_005__sum')
            assert cashtransaction.account_coin_010 == aggregate.get('transaction_coin_010__sum')
            assert cashtransaction.account_coin_020 == aggregate.get('transaction_coin_020__sum')
            assert cashtransaction.account_coin_050 == aggregate.get('transaction_coin_050__sum')
            assert cashtransaction.account_coin_100 == aggregate.get('transaction_coin_100__sum')
            assert cashtransaction.account_coin_200 == aggregate.get('transaction_coin_200__sum')
            assert cashtransaction.account_bill_005 == aggregate.get('transaction_bill_005__sum')
            assert cashtransaction.account_bill_010 == aggregate.get('transaction_bill_010__sum')
            assert cashtransaction.account_bill_020 == aggregate.get('transaction_bill_020__sum')
            assert cashtransaction.account_bill_050 == aggregate.get('transaction_bill_050__sum')
            assert cashtransaction.account_bill_100 == aggregate.get('transaction_bill_100__sum')
            assert cashtransaction.account_bill_200 == aggregate.get('transaction_bill_200__sum')
            assert cashtransaction.account_bill_500 == aggregate.get('transaction_bill_500__sum')

            cashtransaction = cashtransaction.get_next_cashtransaction()
            ctr += 1

        # test amount of test equals amount of CashTransaction in database
        assert ctr == len(CashTransaction.objects.all())
