# coding=utf-8
import datetime
import pytest
from faker import Factory


PASSWORD = 'secret'
EMAIL = 'test@example.com'
USERNAME = 'Test User'


@pytest.fixture
def first_of_this_month():
    import datetime
    td = datetime.date.today()
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
def user_fixture():
    from django.contrib.auth import get_user_model

    user_model = get_user_model()

    user = user_model.objects.create_user(
        username=USERNAME, email=EMAIL, password=PASSWORD
    )
    user.set_password(PASSWORD)
    user.save()

    return user
