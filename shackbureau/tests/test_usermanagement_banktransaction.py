# coding=utf-8
import pytest
import os.path
import io
from django.core.files.uploadedfile import InMemoryUploadedFile


@pytest.mark.django_db
class TestbankTransactionUploadParser:

    # it's real data, biatch
    @pytest.mark.parametrize(('reference', 'expected', 'score'), [
        ('shack e.V. Mitgliedsbeitrag ID  666 Dauerauftrag:         54', 666, 1),
        ('Beitrag MItglied 724             ', 724, 6),
        ('Beitrag shack AAAA AAAAAAA 466 AAAAAAA AAAA           ', False, 99),
        ('Beitrag shack AAAAAAAAAAAAA AAA 91            ', False, 99),
        ('Beitrag             ', False, 99),
        ('ID 167 AAA AAA             ', 167, 3),
        ('ID 325 MITGLIEDSBEITRAG AAA AAA  AAAAAAA ZV0100189577183000111002           ', 325, 2),
        ('MITGLIEDSBEITRAG ID 123             ', 123, 1),
        ('MITGLIEDSBEITRAG ID 371 9802            ', 371, 1),
        ('MITGLIEDSBEITRAG ID 959 ZV0101183786226509001002            ', 959, 1),
        ('Mitgliedsbeitrag 241             ', 241, 5),
        ('Mitgliedsbeitrag AAAAAA AAA AAAA ID 19 Dauerauftrag            ', 19, 3),
        ('Mitgliedsbeitrag AAAAAAA AA AA            ', False, 99),
        ('Mitgliedsbeitrag ID 091             ', 91, 1),
        ('Mitgliedsbeitrag ID 116             ', 116, 1),
        ('Mitgliedsbeitrag             ', False, 99),
        ('MitgliedsbeitragAAAAAA AAAA A 126Monatlich            ', 126, 7),
        ('shack e.V. Mitgliedsbeitrag ID 007 Dauerauftrag:         82           ', 7, 1),
        ('shack e.V. Mitgliedsbeitrag ID 111 Dauerauftrag:         61           ', 111, 1),
        ('shack e.V. Mitgliedsbeitrag ID 172 AAAAAAA AAAAAA Dauerauftrag:         70          ', 172, 1),
        ('shack e.V. Mitgliedsbeitrag ID 492 Dauerauftrag:         23           ', 492, 1),
        ('ID262 ZR1              ', 262, 8),
        ('ID 348, ZR 1, Mitglieds- be      itrag, DIESER MONAT, AAAAA AAAA       ', 348, 9),
        ('MITGLIEDSBEITRAG ID.274              ', 274, 10),
        ('MITGLIEDSBEITRAG ID:275              ', 275, 10),
    ])
    def test_reference_parser(self, reference, expected, score):
        from usermanagement.utils import TransactionLogProcessor
        assert TransactionLogProcessor().reference_parser(reference) == (expected, score)


@pytest.mark.django_db
class TestBankTransactionUpload:

    @pytest.fixture
    def example_csv_file(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        fn = os.path.join(folder, 'fixtures',
                          'sample_lastschrift.csv')
        dummy_file = io.BytesIO()
        dummy_file.write(open(fn).read().encode('utf-8'))
        text_file = InMemoryUploadedFile(dummy_file, None, 'sample_lastschrift.csv', 'text',
                                         len(dummy_file.read()), None)
        return text_file

    @pytest.fixture
    def import_transaction_csv(self, user_fixture, member_fixture_transfer, example_csv_file):
        from usermanagement.models import BankTransactionUpload
        BankTransactionUpload.objects.create(data_file=example_csv_file,
                                             data_type="bank_csv",
                                             status="new", created_by=user_fixture)

    def test_process_bank_csv_log(self, import_transaction_csv):
        from usermanagement.models import BankTransactionUpload, BankTransactionLog
        assert BankTransactionUpload.objects.first().status == 'done'
        assert BankTransactionLog.objects.count() == 1
        transaction = BankTransactionLog.objects.first()
        assert transaction.member.member_id == 1
        assert transaction.is_matched is True
        assert transaction.is_resolved is True
        assert str(transaction.amount) == '8.00'


@pytest.mark.django_db
class TestAccountantTransactionUpload:

    @pytest.fixture
    def example_accountant_csv_file(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        fn = os.path.join(folder, 'fixtures',
                          'sample_steuerberater.csv')
        dummy_file = io.BytesIO()
        dummy_file.write(open(fn).read().encode('utf-8'))
        text_file = InMemoryUploadedFile(dummy_file, None, 'sample_steuerberater.csv', 'text',
                                         len(dummy_file.read()), None)
        return text_file

    @pytest.fixture
    def member_fixture_koch(self, user_fixture, join_date_fixture):
        from faker import Factory
        fake = Factory.create('de_DE')
        from usermanagement.models import Member
        member, created = Member.objects.get_or_create(name=fake.first_name(),
                                                       surname="Koch",
                                                       address1=fake.street_address(),
                                                       zip_code=fake.postcode(),
                                                       city=fake.city(),
                                                       email=fake.free_email(),
                                                       join_date=join_date_fixture,
                                                       payment_type='transfer',
                                                       created_by=user_fixture)
        return member

    @pytest.fixture
    def import_accountant_transaction_csv(self, user_fixture, member_fixture_koch,
                                          example_accountant_csv_file):
        from usermanagement.models import BankTransactionUpload
        BankTransactionUpload.objects.create(data_file=example_accountant_csv_file,
                                             data_type="accountant_csv",
                                             status="new", created_by=user_fixture)

    def test_process_accountant_csv_log(self, import_accountant_transaction_csv):
        from usermanagement.models import BankTransactionUpload, BankTransactionLog
        assert BankTransactionUpload.objects.first().status == 'done'
        assert BankTransactionLog.objects.count() == 2

        transaction = BankTransactionLog.objects.get(member__surname="Koch")
        assert transaction.member.member_id == 1
        assert transaction.member.surname == "Koch"
        assert transaction.is_matched is True
        assert transaction.is_resolved is True
        assert str(transaction.amount) == '20.00'

        transaction = BankTransactionLog.objects.exclude(member__surname="Koch").first()
        assert transaction.member is None
        assert transaction.is_matched is False
        assert transaction.is_resolved is False
        assert str(transaction.amount) == '8.00'
