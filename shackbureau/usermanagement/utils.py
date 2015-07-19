import csv
import requests
from decimal import Decimal

from django.contrib.auth.models import User

from .models import Member


def import_old_shit(filename):
    with open(filename) as fp:
        reader = csv.reader(fp, delimiter=";", quotechar='"')
        headers = reader.__next__()
        for line in reader:
            dataset = dict(zip(headers, line))
            member_data = {}
            kto = dataset.get('konto')
            blz = dataset.get('blz')
            member_data['bic'] = None
            if kto and blz:
                if kto in ['outdated', '?']:
                    pass
                elif len(str(kto)) < 11:
                    iban_checksum = 98 - (int('{:08d}{:010d}131400'.format(int(blz), int(kto))) % 97)
                    member_data['iban'] = 'DE{:02d}{:08d}{:010d}'.format(iban_checksum, int(blz), int(kto))
                    member_data['bic'] = blz_to_bic(blz)
                else:
                    member_data['iban'] = kto
                    member_data['bic'] = dataset.get('blz')

            member_data['member_id'] = dataset['id']
            member_data['surname'] = dataset['name']
            member_data['name'] = dataset['vorname']
            member_data['nickname'] = dataset.get('nickname')
            member_data['join_date'] = dataset['eintritt']
            member_data['leave_date'] = dataset.get('austritt') or None
            member_data['email'] = dataset['email']
            member_data['is_active'] = not bool(member_data.get('leave_date'))

            member_data['membership_type'], member_data['membership_fee_interval'] = [
                None,
                ('full', 1),
                ('full', 12),
                ('reduced', 1),
                ('reduced', 12),
            ][int(dataset['beitragsart'])]

            if dataset['zahlweise'] == 'L':
                member_data['payment_type'] = 'SEPA'
            elif dataset['zahlweise'] in ['U', 'D']:
                member_data['payment_type'] = 'transfer'

            member_data['membership_fee_monthly'] = Decimal(dataset['beitrag'].replace(' €', ''))
            member_data['address1'] = dataset.get('strasse') or '-'
            member_data['city'] = dataset.get('ort')
            member_data['zip_code'] = dataset.get('plz') or '-'
            if not member_data['payment_type'] == 'transfer':
                member_data['iban_fullname'] = dataset.get('kontoinhaber')
                member_data['iban_address'] = dataset.get('strasse')
                member_data['iban_zip_code'] = dataset.get('plz') or '-'
                member_data['iban_city'] = dataset.get('ort')
            member_data['date_of_birth'] = dataset.get('geburtsdatum') or None
            member_data['form_of_address'] = dataset.get('geschlecht').upper()\
                .replace('W', 'F').replace('M', 'H') or 'H'
            member_data['phone_number'] = dataset.get('telefon')
            member_data['created_by'] = User.objects.first()

            print('#' * 40)
            print('Saving {member_id} (BIC: {bic})'.format(**member_data))
            member_id = member_data.pop('member_id')
            Member.objects.update_or_create(member_id=member_id,
                                            defaults=member_data)


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

def add_to_mailman(mailaddr, mitgliederml=True):
    from django.conf import settings
    mitglieder_url = 'https://lists.shackspace.de/mailman/admin/mitglieder'
    mitglieder_subscribe_url = 'https://lists.shackspace.de/mailman/admin/mitglieder/members/add'
    mitglieder_announce_url = 'https://lists.shackspace.de/mailman/admin/mitglieder-announce'
    mitglieder_announce_subscribe_url = 'https://lists.shackspace.de/mailman/admin/mitglieder-announce/members/add'

    s = requests.Session()
    if mitgliederml:
        login_payload = {'adminpw': settings.MAILMAN_MITGLIEDER_PW,
                         'admlogin':  'Let me in...'}
        r = s.post(mitglieder_url, params=login_payload, verify=False)
        assert r.status_code == 200
        subscribe_payload = { 'subscribe_or_invite': 0,
                              'send_welcome_msg_to_this_batch': 1,
                              'send_notifications_to_list_owner': 0,
                              'subscribees': mailaddr,
                              'invitation': '',
                              'setmemberopts_btn': 'Submit Your Changes'}
        r = s.post(mitglieder_subscribe_url, params=subscribe_payload, verify=False) 
        assert r.status_code == 200
    

    login_payload = {'adminpw': settings.MAILMAN_MITGLIEDER_ANNOUNCE_PW,
                     'admlogin':  'Let me in...'}
    r = s.post(mitglieder_announce_url, params=login_payload, verify=False)
    assert r.status_code == 200
    subscribe_payload = { 'subscribe_or_invite': 0,
                          'send_welcome_msg_to_this_batch': 1,
                          'send_notifications_to_list_owner': 0,
                          'subscribees': mailaddr,
                          'invitation': '',
                          'setmemberopts_btn': 'Submit Your Changes'}
    r = s.post(mitglieder_announce_subscribe_url, params=subscribe_payload, verify=False) 
    assert r.status_code == 200
    




