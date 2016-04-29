# coding=utf-8
from django.core.management import BaseCommand
from django.db.models import Max, Min

from cashaccounting.models import CashTransaction
from cashaccounting.utils import export_cashaccounting_csv


class Command(BaseCommand):

    help = "Export CashAccounting."

    def handle(self, *args, **options):
        cashtransaction_aggregate = CashTransaction.objects.aggregate(Min('transaction_date'), Max('transaction_date'))
        first_date = cashtransaction_aggregate.get('transaction_date__min')
        last_date = cashtransaction_aggregate.get('transaction_date__max')
        for year in range(first_date.year, last_date.year + 1):
            export_path = export_cashaccounting_csv(year)
            print("year {} exported into {}".format(year, export_path))
