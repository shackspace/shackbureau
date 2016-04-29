from datetime import date
import csv

from cashaccounting.models import CashSet, CashTransaction

ORDER = [
    'coin_001',
    'coin_002',
    'coin_005',
    'coin_010',
    'coin_020',
    'coin_050',
    'coin_100',
    'coin_200',
    'bill_005',
    'bill_010',
    'bill_020',
    'bill_050',
    'bill_100',
    'bill_200',
    'bill_500',
]


def export_cashaccounting_csv(year, export_file):
    def write_header_into_csv(csv_writer):
        cash_header = [CashSet._meta.get_field(attr).split() for attr in ORDER]

        transaction_header = ['Transaktion {} {}'.format(f[-3], f[-2]) for f in cash_header]
        transaction_header += ['Transaktion Summe']

        account_header = ['Bestand {} {}'.format(f[-3], f[-2]) for f in cash_header]
        account_header += ['Bestand Summe']

        header = ['Datum', 'Kommentar'] + transaction_header + account_header
        csv_writer.writerow(header)

    def write_cashtransactions_into_csv(csv_writer, cashtransaction):
        transaction_data = [getattr(cashtransaction.transaction_cash, attr) for attr in ORDER]
        transaction_data += [cashtransaction.transaction_cash.sum()]
        account_data = [getattr(cashtransaction.account_cash, attr) for attr in ORDER]
        account_data += [cashtransaction.account_cash.sum()]
        row = [cashtransaction.transaction_date, cashtransaction.description] \
                + transaction_data \
                + account_data
        csv_writer.writerow(row)

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
            previous_ct.transaction_cash = previous_ct.account_cash
            write_cashtransactions_into_csv(csv_writer, previous_ct)
    for ct in cashtransactions:
        print(ct)
        write_cashtransactions_into_csv(csv_writer, ct)

    export_file.close()
    return export_file
