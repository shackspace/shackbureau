import csv
import hashlib
import requests
import re
from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import User

from .models import Member, Membership, BankTransactionLog, AccountTransaction, MemberSpecials


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
                    member_data['iban'] = konto_to_iban(blz, kto)
                    member_data['bic'] = blz_to_bic(blz)
                else:
                    member_data['iban'] = kto
                    member_data['bic'] = dataset.get('blz')

            member_data['member_id'] = dataset['id']
            member_data['surname'] = dataset['name']
            member_data['name'] = dataset['vorname']
            member_data['nickname'] = dataset.get('nickname')
            member_data['join_date'] = datetime.strptime(dataset['eintritt'], '%Y-%m-%d').date()
            member_data['leave_date'] = None
            if dataset.get('austritt'):
                member_data['leave_date'] = datetime.strptime(dataset['austritt'], '%Y-%m-%d').date()
            member_data['email'] = dataset['email']
            member_data['is_active'] = not bool(member_data.get('leave_date'))

            if dataset['zahlweise'] == 'L':
                member_data['payment_type'] = 'SEPA'
            elif dataset['zahlweise'] in ['U', 'D']:
                member_data['payment_type'] = 'transfer'

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

            member_data['is_welcome_mail_sent'] = True
            member_data['is_payment_instruction_sent'] = True
            member_data['is_registration_to_mailinglists_sent'] = True

            print('#' * 40)
            print('Saving {member_id} (BIC: {bic})'.format(**member_data))
            member_id = member_data.pop('member_id')
            member, created = Member.objects.update_or_create(member_id=member_id,
                                                              defaults=member_data)

            membership = {}
            membership['membership_type'], membership['membership_fee_interval'] = [
                None,
                ('full', 1),
                ('full', 12),
                ('reduced', 1),
                ('reduced', 12),
            ][int(dataset['beitragsart'])]
            membership['membership_fee_monthly'] = Decimal(dataset['beitrag'].replace(' €', ''))
            valid_from = dataset['eintritt']
            membership['created_by'] = User.objects.first()

            Membership.objects.update_or_create(member=member,
                                                valid_from=valid_from,
                                                defaults=membership)


def konto_to_iban(blz, kto):
    blz = int(blz)
    kto = int(kto)
    iban_checksum = 98 - (int('{:08d}{:010d}131400'.format(blz, kto)) % 97)
    return 'DE{:02d}{:08d}{:010d}'.format(iban_checksum, blz, kto)


bics = {}


def blz_to_bic(blz):
    if blz not in bics:
        import requests
        r = requests.get('https://banking.stupig.org/v1/bank?blz={}'.format(blz))

        assert r.status_code == 200

        for bank in r.json().get('results'):
            bics[blz] = bank.get('bic')
            # use first bank in list
            break
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
                         'admlogin': 'Let me in...'}
        r = s.post(mitglieder_url, params=login_payload, verify=False)
        assert r.status_code == 200
        subscribe_payload = {'subscribe_or_invite': 0,
                             'send_welcome_msg_to_this_batch': 1,
                             'send_notifications_to_list_owner': 0,
                             'subscribees': mailaddr,
                             'invitation': '',
                             'setmemberopts_btn': 'Submit Your Changes'}
        r = s.post(mitglieder_subscribe_url, params=subscribe_payload, verify=False)
        assert r.status_code == 200

    login_payload = {'adminpw': settings.MAILMAN_MITGLIEDER_ANNOUNCE_PW,
                     'admlogin': 'Let me in...'}
    r = s.post(mitglieder_announce_url, params=login_payload, verify=False)
    assert r.status_code == 200
    subscribe_payload = {'subscribe_or_invite': 0,
                         'send_welcome_msg_to_this_batch': 1,
                         'send_notifications_to_list_owner': 0,
                         'subscribees': mailaddr,
                         'invitation': '',
                         'setmemberopts_btn': 'Submit Your Changes'}
    r = s.post(mitglieder_announce_subscribe_url, params=subscribe_payload, verify=False)
    assert r.status_code == 200


class TransactionLogProcessor:

    def process(self, banktransaction):
        if not banktransaction.data_type == 'bank_csv':
            # bail out because other format is not implemented yet.
            return
        self.process_bank_csv(banktransaction)

    def process_accountant_csv(self, banktransaction):
        banktransaction.status = 'wip'
        banktransaction.save()
        reader = csv.reader(open(banktransaction.data_file.file.name, encoding='iso-8859-1'),
                            delimiter=";", quotechar='"')
        reader.__next__()  # first line is meta of accountant
        header = reader.__next__()  # second line is header
        for line in reader:
            d = dict(zip(header, line))
            print(d)
            # strategy:
            # - search for lastname from csv
            # - if lastname is more than one time in database; tag transaction as
            #      is_matched=False, is_resolved=False
            # - otherwise match and add entry, see in other processor.
        return

    def process_bank_csv(self, banktransaction):
        banktransaction.status = 'wip'
        banktransaction.save()
        reader = csv.reader(open(banktransaction.data_file.file.name, encoding='iso-8859-1'),
                            delimiter=";", quotechar='"')
        header = reader.__next__()
        for line in reader:
            d = dict(zip(header, line))
            reference = ''
            for key in sorted(header):
                if key.startswith('VWZ'):
                    reference += d[key] + ' '

            uid, score = self.reference_parser(reference)
            member = None
            error = None
            try:
                if uid:
                    member = Member.objects.get(member_id=uid)
            except Member.DoesNotExist:
                error = "Member does not exist"
            BankTransactionLog.objects.create(
                upload=banktransaction,
                reference=reference,
                member=member,
                error=error, score=score,
                amount=Decimal(d.get('Betrag').replace(',', '.')),
                booking_date=datetime.strptime(d.get('Buchungstag'), '%d.%m.%Y').date(),
                transaction_owner=d.get('Auftraggeber/Empfänger'),
                is_matched=bool(uid),
                is_resolved=bool(uid),
                created_by=banktransaction.created_by
            )
            if member:
                defaults = {
                    'transaction_type': 'membership fee',
                    'amount': Decimal(d.get('Betrag').replace(',', '.')),
                    'created_by': banktransaction.created_by,
                    'payment_reference': reference
                }
                booking_date = datetime.strptime(d.get('Buchungstag'), '%d.%m.%Y').date()
                transation_hash = hashlib.sha256((';'.join(line)).encode('utf-8')).hexdigest()
                AccountTransaction.objects.update_or_create(
                    booking_type='deposit',
                    member=member,
                    booking_date=booking_date,
                    transaction_hash=transation_hash,
                    defaults=defaults)

        banktransaction.status = 'done'
        banktransaction.save()

    def reference_parser(self, reference):
        reference = reference.lower()

        regexes = (
            r'.*mitgliedsbeitrag\s+id\s+(?P<ID>\d{1,3})\s.*',
            r'.*id\s+(?P<ID>\d{1,3})\smitgliedsbeitrag.*',
            r'.*id\s+(?P<ID>\d{1,3})\s.*',
            r'.*mitgliedsbeitrag.*id\s+(?P<ID>\d{1,3})\s.*',
            r'.*mitgliedsbeitrag\s+(?P<ID>\d{1,3})\s.*',
            r'.*beitrag\s+mitglied\s+(?P<ID>\d{1,3})\s.*',
            r'.*mitgliedsbeitrag.*\s+(?P<ID>\d{1,3})[^\d].*',
        )

        for score, regex in enumerate(regexes, 1):
            hit = re.match(regex, reference)
            if hit:
                return (int(hit.groupdict().get('ID')), score)

        return (False, 99)


def update_keymember(member_id, ssh_key):
    member = Member.objects.get(member_id=member_id)
    member_special, created = MemberSpecials.objects.get_or_create(member=member,
                                                                   defaults={'created_by': User.objects.get(username="admin")})
    member_special.is_keyholder = True
    member_special.ssh_public_key = ssh_key
    member_special.save()
