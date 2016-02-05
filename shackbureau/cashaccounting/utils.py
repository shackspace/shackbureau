from django.conf import settings

from os import path
import csv

from cashaccounting.models import CashTransaction


def export_cashaccounting_csv(year):
    cashtransactions = CashTransaction.objects.filter(transaction_date__year=year) \
        .order_by('transaction_date', 'transaction_date_id')
    export_path = path.join(settings.EXPORT_ROOT, "cashaccounting_{}.csv".format(year))

    with open(export_path, 'w') as export_file:
        csv_writer = csv.writer(export_file, csv.excel)
        for ct in cashtransactions:
            csv_writer.writerow([ct.transaction_date,
                                 ct.description,
                                 ct.transaction_coin_001,
                                 ct.transaction_coin_002,
                                 ct.transaction_coin_005,
                                 ct.transaction_coin_010,
                                 ct.transaction_coin_020,
                                 ct.transaction_coin_050,
                                 ct.transaction_coin_100,
                                 ct.transaction_coin_200,
                                 ct.transaction_bill_005,
                                 ct.transaction_bill_010,
                                 ct.transaction_bill_020,
                                 ct.transaction_bill_050,
                                 ct.transaction_bill_100,
                                 ct.transaction_bill_200,
                                 ct.transaction_bill_500,
                                 ct.account_coin_001,
                                 ct.account_coin_002,
                                 ct.account_coin_005,
                                 ct.account_coin_010,
                                 ct.account_coin_020,
                                 ct.account_coin_050,
                                 ct.account_coin_100,
                                 ct.account_coin_200,
                                 ct.account_bill_005,
                                 ct.account_bill_010,
                                 ct.account_bill_020,
                                 ct.account_bill_050,
                                 ct.account_bill_100,
                                 ct.account_bill_200,
                                 ct.account_bill_500,
                                 ct.transaction_sum,
                                 ct.account_sum,
                                 ])
    return export_path
