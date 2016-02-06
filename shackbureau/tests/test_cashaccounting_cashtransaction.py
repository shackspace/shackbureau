# coding=utf-8
import pytest

from django.db.models import Q, Sum

from cashaccounting.models import CashTransaction


# def get_account_state(date, date_id):
#     CashTransaction.objects.filter(Q(transaction_date__lt=date) |
#                                    Q(transaction_date=date, transaction_date_id__lte=date_id)) \
#         .order_by().aggreagte(Sum('transaction_sum'),
#                               Sum('transaction_coin_001'),
#                               Sum('transaction_coin_002'),
#                               Sum('transaction_coin_005'),
#                               Sum('transaction_coin_010'),
#                               Sum('transaction_coin_020'),
#                               Sum('transaction_coin_050'),
#                               Sum('transaction_coin_100'),
#                               Sum('transaction_coin_200'),
#                               Sum('transaction_bill_005'),
#                               Sum('transaction_bill_010'),
#                               Sum('transaction_bill_020'),
#                               Sum('transaction_bill_050'),
#                               Sum('transaction_bill_100'),
#                               Sum('transaction_bill_200'),
#                               Sum('transaction_bill_500'),
#                               )


@pytest.mark.django_db
class TestMember:

    def test_transaction_sum(self, cashtransaction_fixture_1, cashtransaction_fixture_2,
                             cashtransaction_fixture_3, cashtransaction_fixture_4):
        from decimal import Decimal
        first_cashtransaction = CashTransaction.objects.order_by('transaction_date', 'transaction_date_id').first()
        # last_cashtransaction = CashTransaction.objects.order_by('transaction_date', 'transaction_date_id').last()
        cashtransaction = first_cashtransaction
        ctr = 0
        while cashtransaction:
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
            aggregate = CashTransaction.objects.filter(
                Q(transaction_date__lt=cashtransaction.transaction_date) |
                Q(transaction_date=cashtransaction.transaction_date, transaction_date_id__lte=cashtransaction.transaction_date_id)) \
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

            # test aggregate sums of older transaction versus sums in cashtransaction
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

        assert ctr == len(CashTransaction.objects.all())
