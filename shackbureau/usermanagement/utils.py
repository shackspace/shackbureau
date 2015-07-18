import csv


def import_old_shit(filename):
    import pprint
    with open(filename) as fp:
        reader = csv.reader(fp, delimiter=";", quotechar='"')
        headers = reader.__next__()
        for line in reader:
            dataset = dict(zip(headers, line))
            print('#########################################')
            pprint.pprint(dataset)
            kto = int(dataset.get('konto'))
            blz = int(dataset.get('blz'))
            iban_checksum = 98 - (int('{:010d}{:08d}131400'.format(kto, blz)) % 97)
            iban = 'DE{:02d}{:010d}{:08d}'.format(iban_checksum, kto, blz)
            print('IBAN: ' + iban)
            bic = blz_to_bic(blz)
            print('BIC: ' + bic)


bics = {}


def blz_to_bic(blz):
    if blz not in bics:
        import requests
        r = requests.get(
            'https://www.sparkasse.de/privatkunden/konto-karte/iban-resources/iban/iban.php'
            '?bank-code={}&bank-account-number=1234567&_=1437238271816'.format(blz),
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )

        assert r.status_code == 200

        bic = r.json().get('BIC')
        bics[blz] = bic

    return bics[blz]
