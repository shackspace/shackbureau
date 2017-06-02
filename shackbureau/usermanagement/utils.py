import csv
import hashlib
import os
import requests
import re
from contextlib import redirect_stdout
from datetime import datetime, date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.db import models

from .models import Member, Membership, BankTransactionLog, AccountTransaction, MemberSpecials, Memberlog
from districtcourt.models import Debitor, DistrictcourtAccountTransaction


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

            member_data['member_id'] = int(dataset['id'])
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
            valid_from = datetime.strptime(dataset['eintritt'], "%Y-%m-%d").date()
            membership['created_by'] = User.objects.first()
            membership['is_payment_instruction_sent'] = True

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


def subscribe_to_mailinglist(mailinglist, emailaddress):
    from django.conf import settings
    if not settings.MAILMAN_API_USER or not settings.MAILMAN_API_PASSWORD:
        print("subscribe_to_mailinglist not possible ({} - {})\n".format(mailinglist, emailaddress) +
              "please add MAILMAN_API_USER and MAILMAN_API_PASSWORD to production settings")
        return

    r = requests.post("https://shackspace.de/mlm-api/lists.shackspace.de/{}/{}".format(mailinglist, emailaddress),
                      auth=(settings.MAILMAN_API_USER, settings.MAILMAN_API_PASSWORD),
                      verify=False)
    Memberlog.objects.create(
        action='subscribe to mailinglist {}'.format(mailinglist),
        detail="{email}\n\nHTTP Response:{status_code}\n{text}".format(email=emailaddress,
                                                                       status_code=r.status_code,
                                                                       text=r.text)
    )
    assert r.status_code == 200


def remove_from_mailinglist(mailinglist, emailaddress):
    from django.conf import settings
    if not settings.MAILMAN_API_USER or not settings.MAILMAN_API_PASSWORD:
        print("remove_from_mailinglist not possible ({} - {})\n".format(mailinglist, emailaddress) +
              "please add MAILMAN_API_USER and MAILMAN_API_PASSWORD to production settings")
        return

    r = requests.delete("https://shackspace.de/mlm-api/lists.shackspace.de/{}/{}".format(mailinglist, emailaddress),
                        auth=(settings.MAILMAN_API_USER, settings.MAILMAN_API_PASSWORD),
                        verify=False)
    Memberlog.objects.create(
        action='unsubscribe from mailinglist {}'.format(mailinglist),
        detail="{email}\n\nHTTP Response:{status_code}\n{text}".format(email=emailaddress,
                                                                       status_code=r.status_code,
                                                                       text=r.text)
    )
    assert r.status_code == 200


def is_on_mailinglist(mailinglist, emailaddress):
    from django.conf import settings
    if not settings.MAILMAN_API_USER or not settings.MAILMAN_API_PASSWORD:
        print("is_on_mailinglist not possible ({} - {})\n".format(mailinglist, emailaddress) +
              "please add MAILMAN_API_USER and MAILMAN_API_PASSWORD to production settings")
        return

    r = requests.get("https://shackspace.de/mlm-api/lists.shackspace.de/{}/{}".format(mailinglist, emailaddress),
                     auth=(settings.MAILMAN_API_USER, settings.MAILMAN_API_PASSWORD),
                     verify=False)
    assert r.status_code == 200
    if r.text.strip() == emailaddress:
        return True
    else:
        return False


def add_to_mailman(mailaddr, mitgliederml=True):
    if mitgliederml:
        subscribe_to_mailinglist("mitglieder", mailaddr)
    subscribe_to_mailinglist("mitglieder-announce", mailaddr)


def is_allowed_on_mitglieder_mailinglist(emailaddress):
    return Member.objects.get_active_members().filter(email__iexact=emailaddress).count() > 0


def is_allowed_on_key_mailinglist(emailaddress):
    return Member.objects.get_active_keymembers().filter(email__iexact=emailaddress).count() > 0


class TransactionLogProcessor:
    def __init__(self):
        self.debitors = Debitor.objects.all().values('pk', 'record_token', 'record_token_line_2')

        def build_regex(record_token):
            record_token = [re.escape(element) for element in record_token.lower().split()]
            regex = r".*" + r'\s*'.join(record_token) + ".*"
            return regex

        for i in range(len(self.debitors)):
            self.debitors[i]['regex'] = build_regex(self.debitors[i]['record_token'])
            self.debitors[i]['regex_line_2'] = build_regex(self.debitors[i]['record_token_line_2'])

    def process(self, banktransaction):
        if banktransaction.data_type == 'bank_csv':
            self.process_bank_csv(banktransaction)
        else:
            self.process_accountant_csv(banktransaction)

    def process_accountant_csv(self, banktransaction):
        banktransaction.status = 'wip'
        banktransaction.save()
        reader = csv.reader(open(banktransaction.data_file.file.name, encoding='iso-8859-1'),
                            delimiter=";", quotechar='"')
        reader.__next__()  # first line is meta of accountant
        header = reader.__next__()  # second line is header
        for line in reader:
            if not line:
                continue
            d = dict(zip(header, line))
            member = None
            uid = None
            error = None
            if 'Buchungstext' in d:
                members = Member.objects.filter(surname__iexact=d.get('Buchungstext'))
                if members.count() == 1:
                    member = members.first()
                    uid = member.member_id
            reference = d.get('Buchungstext')
            haben = Decimal(d.get('Umsatz Haben').replace(',', '.') or 0)
            soll = Decimal(d.get('Umsatz Soll').replace(',', '.') or 0)
            amount = haben - soll
            BankTransactionLog.objects.create(
                upload=banktransaction,
                reference=reference,
                member=member,
                error=error, score=0,
                amount=amount,
                booking_date=datetime.strptime(d.get('Datum'), '%d.%m.%Y').date(),
                is_matched=bool(uid),
                is_resolved=bool(uid),
                created_by=banktransaction.created_by
            )
            if member:
                defaults = {
                    'transaction_type': 'membership fee',
                    'amount': amount,
                    'created_by': banktransaction.created_by,
                    'payment_reference': reference
                }
                due_date = datetime.strptime(d.get('Datum'), '%d.%m.%Y').date()
                transation_hash = hashlib.sha256((';'.join(line)).encode('utf-8')).hexdigest()
                AccountTransaction.objects.update_or_create(
                    booking_type='deposit',
                    member=member,
                    due_date=due_date,
                    transaction_hash=transation_hash,
                    defaults=defaults)
        banktransaction.status = 'done'
        banktransaction.save()

    def process_bank_csv(self, banktransaction):
        banktransaction.status = 'wip'
        banktransaction.save()
        reader = csv.reader(open(banktransaction.data_file.file.name, encoding='iso-8859-1'),
                            delimiter=";", quotechar='"')
        header = reader.__next__()
        for line in reader:
            if not line:
                continue
            d = dict(zip(header, line))
            reference = ''
            for key in sorted(header):
                if key.startswith('VWZ'):
                    reference += d[key] + ' '

            uid, score = self.reference_parser(reference)
            member = None
            debitor = self.get_debitor_by_record_token(reference)
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
                debitor=debitor,
                error=error, score=score,
                amount=Decimal(d.get('Betrag').replace('.', '').replace(',', '.')),
                booking_date=datetime.strptime(d.get('Buchungstag'), '%d.%m.%Y').date(),
                transaction_owner=d.get('Auftraggeber/Empfänger'),
                is_matched=bool(uid) or bool(debitor),
                is_resolved=bool(uid) or bool(debitor),
                created_by=banktransaction.created_by
            )
            if member:
                defaults = {
                    'transaction_type': 'membership fee',
                    'amount': Decimal(d.get('Betrag').replace('.', '').replace(',', '.')),
                    'created_by': banktransaction.created_by,
                    'payment_reference': reference
                }
                due_date = datetime.strptime(d.get('Buchungstag'), '%d.%m.%Y').date()
                transation_hash = hashlib.sha256((';'.join(line)).encode('utf-8')).hexdigest()
                AccountTransaction.objects.update_or_create(
                    booking_type='deposit',
                    member=member,
                    due_date=due_date,
                    transaction_hash=transation_hash,
                    defaults=defaults)
            elif debitor:
                defaults = {
                    'amount': Decimal(d.get('Betrag').replace('.', '').replace(',', '.')),
                    'created_by': banktransaction.created_by,
                    'payment_reference': reference
                }
                due_date = datetime.strptime(d.get('Buchungstag'), '%d.%m.%Y').date()
                transation_hash = hashlib.sha256((';'.join(line)).encode('utf-8')).hexdigest()
                DistrictcourtAccountTransaction.objects.update_or_create(
                    booking_type='deposit',
                    debitor=debitor,
                    due_date=due_date,
                    transaction_hash=transation_hash,
                    defaults=defaults)

        banktransaction.status = 'done'
        banktransaction.save()

    def reference_parser(self, reference):
        reference = reference.lower()

        regexes = (
            r'.*mitgliedsbeitrag\s+id\s+(?P<ID>\d{1,4})\s.*',
            r'.*id\s+(?P<ID>\d{1,4})\smitgliedsbeitrag.*',
            r'.*id\s+(?P<ID>\d{1,4})\s.*',
            r'.*mitgliedsbeitrag.*id\s+(?P<ID>\d{1,4})\s.*',
            r'.*mitgliedsbeitrag\s+(?P<ID>\d{1,4})\s.*',
            r'.*beitrag\s+mitglied\s+(?P<ID>\d{1,4})\s.*',
            r'.*mitgliedsbeitrag.*\s+(?P<ID>\d{1,4})[^\d].*',
            r'.*id(?P<ID>\d{1,4})\s+zr\d+.*',
            r'.*id\s+(?P<ID>\d{1,4}),\s+zr\s+\d+.*',
            r'.*mitgliedsbeitrag\s+id[.:-_](?P<ID>\d{1,4})\s.*',
        )

        for score, regex in enumerate(regexes, 1):
            hit = re.match(regex, reference)
            if hit:
                return (int(hit.groupdict().get('ID')), score)

        return (False, 99)

    def get_debitor_by_record_token(self, reference):
        reference = "".join(reference.lower().split())
        for debitor in self.debitors:
            if re.match(debitor['regex'], reference):
                return Debitor.objects.get(pk=debitor['pk'])
        return None


def update_keymember(member_id, ssh_key):
    member = Member.objects.get(member_id=member_id)
    member_special, created = MemberSpecials.objects.get_or_create(member=member,
                                                                   defaults={'created_by': get_shackbureau_user()})
    member_special.is_keyholder = True
    member_special.ssh_public_key = ssh_key
    member_special.save()


def member_statistic(year=None, month=None):
    from collections import namedtuple
    MemberStatistic = namedtuple('MemberStatistic', ['date', 'members', 'joined', 'left', 'full', 'reduced', 'sum', 'fees'])
    statistic = []

    if year:
        if month:
            start_date = date(year, month, 1)
            end_date = date(year, month, 1)
        else:
            start_date = date(year, 1, 1)
            end_date = date(year, 12, 1)
    else:
        start_date = (Member.objects.aggregate(models.Min('join_date')).get('join_date__min') or date.today()).replace(day=1)
        end_date = date.today().replace(day=1)

    def duration(start_date, end_date):
        current_date = start_date
        while True:
            if current_date > end_date:
                return
            yield current_date
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year+1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month+1)

    for current_date in duration(start_date, end_date):
        members = Member.objects.get_active_members(current_date)
        joined_members = Member.objects.get_joined_members(current_date)
        left_members = Member.objects.get_left_members(current_date)

        amount_of_members = len(members)
        amount_of_joined_members = len(joined_members)
        amount_of_left_members = len(left_members)

        membership_full = 0
        membership_reduced = 0
        sum_of_fees = 0
        fees = dict()

        for member in members:
            membership = Membership.objects.get_current_membership(member, current_date)
            if not membership:
                print("{} has no active membership for {}".format(member, current_date))
                continue
            if membership.membership_type == 'full':
                membership_full += 1
            else:
                membership_reduced += 1

            fee = membership.membership_fee_monthly
            sum_of_fees += fee
            if fee in fees:
                fees[fee] += 1
            else:
                fees[fee] = 1

        statistic.append(MemberStatistic(current_date,
                                         amount_of_members,
                                         amount_of_joined_members,
                                         amount_of_left_members,
                                         membership_full,
                                         membership_reduced,
                                         sum_of_fees,
                                         fees))

    if month:
        return statistic[0]
    return statistic


def last_day_of_month(given_date):
    new_date = given_date.replace(day=28) + timedelta(days=5)
    new_date = new_date.replace(day=1) - timedelta(days=1)
    return new_date


def get_shackbureau_user():
    user_model = get_user_model()
    shackbureau, created = user_model.objects.get_or_create(username='shackbureau',
                                                            defaults={'is_active': False})
    return shackbureau


def safe_print(string):
    result = ''
    with redirect_stdout(open(os.devnull, 'w')):
        for letter in string:
            try:
                print(letter)
                result += letter
            except:
                result += '_'
    return result
