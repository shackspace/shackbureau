# coding=utf-8
from django.core.management import BaseCommand

from cashaccounting.models import CashTransaction


class Command(BaseCommand):

    help = "check CashAccounting."

    # def add_arguments(self, parser):
    #     parser.add_argument('year', type=int)

    def handle(self, *args, **options):
        cashtransactions = CashTransaction.objects.all().order_by('transaction_date', 'transaction_date_id')
        for cashtransaction in cashtransactions:
            negative_account_states = cashtransaction.get_negative_account_states()
            if negative_account_states:
                print("{} has negative account stats: {}".format(cashtransaction,
                                                                 ', '.join(negative_account_states.keys())))
