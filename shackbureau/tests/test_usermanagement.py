# coding=utf-8
import datetime
import pytest
from faker import Factory


@pytest.fixture
def member_fixture_transfer(user_fixture):
    fake = Factory.create('de_DE')
    from usermanagement.models import Member
    member, created = Member.objects.get_or_create(name=fake.first_name(),
                                                   surname=fake.last_name(),
                                                   address1=fake.street_address(),
                                                   zip_code=fake.postcode(),
                                                   city=fake.city(),
                                                   email=fake.free_email(),
                                                   join_date=datetime.date.today(),
                                                   payment_type='transfer',
                                                   created_by=user_fixture)
    return member


@pytest.fixture
def member_fixture_sepa(user_fixture):
    fake = Factory.create('de_DE')
    from usermanagement.models import Member
    member, created = Member.objects.get_or_create(name=fake.first_name(),
                                                   surname=fake.last_name(),
                                                   address1=fake.street_address(),
                                                   zip_code=fake.postcode(),
                                                   city=fake.city(),
                                                   email=fake.free_email(),
                                                   join_date=datetime.date.today(),
                                                   payment_type='sepa',
                                                   iban_fullname=fake.name(),
                                                   iban_address=fake.street_address(),
                                                   iban_zip_code=fake.postcode(),
                                                   iban_city=fake.city(),
                                                   created_by=user_fixture)
    return member


@pytest.mark.django_db
class TestMember:

    def test_member_id_set(self, member_fixture_transfer):
        assert member_fixture_transfer.member_id > 0

    def test_two_member_ids_set(self, member_fixture_transfer, member_fixture_sepa):
        assert member_fixture_sepa.member_id != member_fixture_transfer.member_id
