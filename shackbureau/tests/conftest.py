# coding=utf-8
import datetime
import pytest
from faker import Factory
from random import randint


PASSWORD = 'secret'
EMAIL = 'test@example.com'
USERNAME = 'Test User'


@pytest.fixture
def join_date_fixture():
    return datetime.date(2015, 10, 17)


@pytest.fixture
def leave_date_fixture():
    return datetime.date(2018, 1, 15)


@pytest.fixture
def first_of_this_month(join_date_fixture):
    td = join_date_fixture
    td = td.replace(day=1)
    return td


@pytest.fixture
def first_of_previous_month(first_of_this_month):
    td = first_of_this_month
    td = td.replace(month=td.month - 1)
    return td


@pytest.fixture
def first_of_next_month(first_of_this_month):
    td = first_of_this_month
    td = td.replace(month=td.month + 1)
    return td


@pytest.fixture
def last_of_next_month(first_of_next_month):
    td = first_of_next_month
    td = td.replace(month=td.month + 1)
    td = td - datetime.timedelta(days=1)
    return td


@pytest.fixture
def member_fixture_sepa(user_fixture, join_date_fixture):
    fake = Factory.create('de_DE')
    from usermanagement.models import Member
    member, created = Member.objects.get_or_create(name=fake.first_name(),
                                                   surname=fake.last_name(),
                                                   address1=fake.street_address(),
                                                   zip_code=fake.postcode(),
                                                   city=fake.city(),
                                                   email=fake.free_email(),
                                                   join_date=join_date_fixture,
                                                   payment_type='sepa',
                                                   iban_issue_date=join_date_fixture,
                                                   iban_fullname=fake.name(),
                                                   iban_address=fake.street_address(),
                                                   iban_zip_code=fake.postcode(),
                                                   iban_city=fake.city(),
                                                   created_by=user_fixture)
    return member


@pytest.fixture
def membership_fixture_sepa(user_fixture, member_fixture_sepa, join_date_fixture):
    from usermanagement.models import Membership
    membership, created = Membership.objects.get_or_create(member=member_fixture_sepa,
                                                           valid_from=join_date_fixture,
                                                           membership_fee_monthly=20,
                                                           membership_type='Full',
                                                           created_by=user_fixture)
    membership.save()
    return membership


@pytest.fixture
def member_fixture_transfer(user_fixture, join_date_fixture):
    fake = Factory.create('de_DE')
    from usermanagement.models import Member
    member, created = Member.objects.get_or_create(name=fake.first_name(),
                                                   surname=fake.last_name(),
                                                   address1=fake.street_address(),
                                                   zip_code=fake.postcode(),
                                                   city=fake.city(),
                                                   email=fake.free_email(),
                                                   join_date=join_date_fixture,
                                                   payment_type='transfer',
                                                   created_by=user_fixture)
    return member


@pytest.fixture
def member_fixture_inactive(user_fixture, join_date_fixture, leave_date_fixture):
    fake = Factory.create('de_DE')
    from usermanagement.models import Member
    member, created = Member.objects.get_or_create(name=fake.first_name(),
                                                   surname=fake.last_name(),
                                                   address1=fake.street_address(),
                                                   zip_code=fake.postcode(),
                                                   city=fake.city(),
                                                   email=fake.free_email(),
                                                   join_date=join_date_fixture,
                                                   is_active=False,
                                                   leave_date=leave_date_fixture,
                                                   payment_type='transfer',
                                                   created_by=user_fixture)
    return member


@pytest.fixture
def member_fixture_not_keymember(member_fixture_transfer, user_fixture, join_date_fixture):
    fake = Factory.create('de_DE')
    from usermanagement.models import Member
    member, created = Member.objects.get_or_create(name=fake.first_name(),
                                                   surname=fake.last_name(),
                                                   address1=fake.street_address(),
                                                   zip_code=fake.postcode(),
                                                   city=fake.city(),
                                                   email=fake.free_email(),
                                                   join_date=join_date_fixture,
                                                   payment_type='sepa',
                                                   iban_fullname=fake.name(),
                                                   iban_address=fake.street_address(),
                                                   iban_zip_code=fake.postcode(),
                                                   iban_city=fake.city(),
                                                   created_by=user_fixture)
    return member


@pytest.fixture
def member_fixture_keymember(user_fixture, join_date_fixture):
    fake = Factory.create('de_DE')
    from usermanagement.models import Member
    member, created = Member.objects.get_or_create(name=fake.first_name(),
                                                   surname=fake.last_name(),
                                                   address1=fake.street_address(),
                                                   zip_code=fake.postcode(),
                                                   city=fake.city(),
                                                   email=fake.free_email(),
                                                   join_date=join_date_fixture,
                                                   payment_type='sepa',
                                                   iban_fullname=fake.name(),
                                                   iban_address=fake.street_address(),
                                                   iban_zip_code=fake.postcode(),
                                                   iban_city=fake.city(),
                                                   created_by=user_fixture)
    from usermanagement.models import MemberSpecials
    memberspecial, created = MemberSpecials.objects.get_or_create(member=member, created_by=user_fixture)
    memberspecial.is_keyholder = True
    memberspecial.ssh_public_key = "a"
    memberspecial.save()
    return member


@pytest.fixture
def member_fixture_memberspecials(user_fixture, join_date_fixture):
    fake = Factory.create('de_DE')
    from usermanagement.models import Member
    member, created = Member.objects.get_or_create(name=fake.first_name(),
                                                   surname=fake.last_name(),
                                                   address1=fake.street_address(),
                                                   zip_code=fake.postcode(),
                                                   city=fake.city(),
                                                   email=fake.free_email(),
                                                   join_date=join_date_fixture,
                                                   payment_type='sepa',
                                                   iban_fullname=fake.name(),
                                                   iban_address=fake.street_address(),
                                                   iban_zip_code=fake.postcode(),
                                                   iban_city=fake.city(),
                                                   created_by=user_fixture)
    from usermanagement.models import MemberSpecials
    memberspecial, created = MemberSpecials.objects.get_or_create(member=member,
                                                                  created_by=user_fixture,
                                                                  has_matomat_key=True,
                                                                  has_snackomat_key=True,
                                                                  has_laser_key=True,
                                                                  has_metro_card=True,
                                                                  has_selgros_card=True,
                                                                  has_shack_iron_key=True,
                                                                  has_safe_key=True,
                                                                  has_loeffelhardt_account=True,
                                                                  signed_DSV=True,)
    return member


@pytest.fixture
def membership_fixture(member_fixture_transfer, join_date_fixture):
    from usermanagement.models import Membership
    from decimal import Decimal
    membership, created = Membership.objects.get_or_create(
        member=member_fixture_transfer,
        created_by=member_fixture_transfer.created_by,
        defaults = {"valid_from": join_date_fixture, "membership_fee_monthly": Decimal('23.42')}
    )
    return membership


@pytest.fixture
def user_fixture():
    from django.contrib.auth import get_user_model

    user_model = get_user_model()

    user = user_model.objects.create_user(
        username=USERNAME, email=EMAIL, password=PASSWORD
    )
    user.set_password(PASSWORD)
    user.save()

    return user


@pytest.fixture
def admin_fixture():
    from django.contrib.auth import get_user_model

    user_model = get_user_model()

    user = user_model.objects.create_user(
        username="admin", password="admin"
    )
    user.save()

    return user


@pytest.fixture
def cashtransaction_fixtures(user_fixture):
    from cashaccounting.models import CashTransaction
    from datetime import date

    cashtransactions = []
    for i in range(5):
        day, day_id = divmod(i, 2)
        day += 1
        day_id += 1
        cashtransaction, created = CashTransaction.objects.get_or_create(
            transaction_date=date(2016, 2, day),
            transaction_date_id=day_id,
            description="cashtransaction_fixture_1",
            is_stored_by_account=not bool(randint(0, 3)),
            transaction_coin_001=randint(-100, 100),
            transaction_coin_002=randint(-100, 100),
            transaction_coin_005=randint(-100, 100),
            transaction_coin_010=randint(-100, 100),
            transaction_coin_020=randint(-100, 100),
            transaction_coin_050=randint(-100, 100),
            transaction_coin_100=randint(-100, 100),
            transaction_coin_200=randint(-100, 100),
            transaction_bill_005=randint(-100, 100),
            transaction_bill_010=randint(-100, 100),
            transaction_bill_020=randint(-100, 100),
            transaction_bill_050=randint(-100, 100),
            transaction_bill_100=randint(-100, 10),
            transaction_bill_200=randint(-100, 10),
            transaction_bill_500=randint(-100, 10),
            created_by=user_fixture,
        )
        cashtransactions.append(cashtransaction)
    return cashtransactions


@pytest.fixture
def letter_fixture(user_fixture):
    from documentmanagement.models import Letter
    from datetime import date
    letter = Letter()
    letter.description = "Karl Koch"
    letter.address = "Karl Koch\nUlmer Straße 255\n70327 Stuttgart"
    letter.content = "this is a letter."
    letter.date = date.today()
    letter.subject = "This is the subject of the letter"
    letter.created_by = user_fixture
    letter.save()
    return letter


@pytest.fixture
def donationreceipt_fixture(user_fixture):
    from documentmanagement.models import DonationReceipt
    from datetime import date
    from decimal import Decimal
    donationreceipt = DonationReceipt()
    donationreceipt.address_of_donator = "Karl Koch\nUlmer Straße 255\n70327 Stuttgart"
    donationreceipt.amount = Decimal('133.37')
    donationreceipt.created_by = user_fixture
    donationreceipt.date = date.today()
    donationreceipt.day_of_donation = date.today()
    donationreceipt.description = "Karl Koch"
    donationreceipt.donation_type = 'allowance in money'
    donationreceipt.save()
    return donationreceipt


@pytest.fixture
def dataprotectionagreement_fixture(user_fixture):
    from documentmanagement.models import DataProtectionAgreement
    from datetime import date
    dataprotectionagreement = DataProtectionAgreement()
    dataprotectionagreement.address = "Karl Koch\nUlmer Straße 255\n70327 Stuttgart"
    dataprotectionagreement.date = date.today()
    dataprotectionagreement.description = "Karl Koch"
    dataprotectionagreement.created_by = user_fixture
    dataprotectionagreement.save()
    return dataprotectionagreement
