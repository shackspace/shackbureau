from datetime import date
import csv

from cashaccounting.models import CashTransaction


def export_cashaccounting_csv(year, export_file):
    def write_header_into_csv(csv_writer):
        csv_writer.writerow(['Datum',
                             'Komentar',
                             'Transaktion 1 Cent',
                             'Transaktion 2 Cent',
                             'Transaktion 5 Cent',
                             'Transaktion 10 Cent',
                             'Transaktion 20 Cent',
                             'Transaktion 50 Cent',
                             'Transaktion 1 Euro',
                             'Transaktion 2 Euro',
                             'Transaktion 5 Euro',
                             'Transaktion 10 Euro',
                             'Transaktion 20 Euro',
                             'Transaktion 50 Euro',
                             'Transaktion 100 Euro',
                             'Transaktion 200 Euro',
                             'Transaktion 500 Euro',
                             'Transaktion Summe',
                             'Bestand 1 Cent',
                             'Bestand 2 Cent',
                             'Bestand 5 Cent',
                             'Bestand 10 Cent',
                             'Bestand 20 Cent',
                             'Bestand 50 Cent',
                             'Bestand 1 Euro',
                             'Bestand 2 Euro',
                             'Bestand 5 Euro',
                             'Bestand 10 Euro',
                             'Bestand 20 Euro',
                             'Bestand 50 Euro',
                             'Bestand 100 Euro',
                             'Bestand 200 Euro',
                             'Bestand 500 Euro',
                             'Bestand Summe',
                             ])

    def write_ashtransactions_into_csv(csv_writer, cashtransaction):
        csv_writer.writerow([cashtransaction.transaction_date,
                             cashtransaction.description,
                             cashtransaction.transaction_coin_001,
                             cashtransaction.transaction_coin_002,
                             cashtransaction.transaction_coin_005,
                             cashtransaction.transaction_coin_010,
                             cashtransaction.transaction_coin_020,
                             cashtransaction.transaction_coin_050,
                             cashtransaction.transaction_coin_100,
                             cashtransaction.transaction_coin_200,
                             cashtransaction.transaction_bill_005,
                             cashtransaction.transaction_bill_010,
                             cashtransaction.transaction_bill_020,
                             cashtransaction.transaction_bill_050,
                             cashtransaction.transaction_bill_100,
                             cashtransaction.transaction_bill_200,
                             cashtransaction.transaction_bill_500,
                             cashtransaction.transaction_sum,
                             cashtransaction.account_coin_001,
                             cashtransaction.account_coin_002,
                             cashtransaction.account_coin_005,
                             cashtransaction.account_coin_010,
                             cashtransaction.account_coin_020,
                             cashtransaction.account_coin_050,
                             cashtransaction.account_coin_100,
                             cashtransaction.account_coin_200,
                             cashtransaction.account_bill_005,
                             cashtransaction.account_bill_010,
                             cashtransaction.account_bill_020,
                             cashtransaction.account_bill_050,
                             cashtransaction.account_bill_100,
                             cashtransaction.account_bill_200,
                             cashtransaction.account_bill_500,
                             cashtransaction.account_sum,
                             ])

    cashtransactions = CashTransaction.objects.filter(transaction_date__year=year) \
        .order_by('transaction_date', 'transaction_date_id')
    export_file.close()
    export_file.file.close()
    export_file.open('w')
    csv_writer = csv.writer(export_file, csv.excel)
    write_header_into_csv(csv_writer)
    if cashtransactions:
        previous_ct = cashtransactions[0].get_previous_cashtransaction()
        if previous_ct:
            previous_ct.description = "Übertrag aus {}".format(year - 1)
            previous_ct.transaction_date = date(year, 1, 1)
            previous_ct.transaction_coin_001 = previous_ct.account_coin_001
            previous_ct.transaction_coin_002 = previous_ct.account_coin_002
            previous_ct.transaction_coin_005 = previous_ct.account_coin_005
            previous_ct.transaction_coin_010 = previous_ct.account_coin_010
            previous_ct.transaction_coin_020 = previous_ct.account_coin_020
            previous_ct.transaction_coin_050 = previous_ct.account_coin_050
            previous_ct.transaction_coin_100 = previous_ct.account_coin_100
            previous_ct.transaction_coin_200 = previous_ct.account_coin_200
            previous_ct.transaction_bill_005 = previous_ct.account_bill_005
            previous_ct.transaction_bill_010 = previous_ct.account_bill_010
            previous_ct.transaction_bill_020 = previous_ct.account_bill_020
            previous_ct.transaction_bill_050 = previous_ct.account_bill_050
            previous_ct.transaction_bill_100 = previous_ct.account_bill_100
            previous_ct.transaction_bill_200 = previous_ct.account_bill_200
            previous_ct.transaction_bill_500 = previous_ct.account_bill_500
            previous_ct.transaction_sum = previous_ct.account_sum
            write_ashtransactions_into_csv(csv_writer, previous_ct)
    for ct in cashtransactions:
        print(ct)
        write_ashtransactions_into_csv(csv_writer, ct)

    export_file.close()
    return export_file
