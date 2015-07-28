# coding=utf-8
import pytest


PASSWORD = 'secret'
EMAIL = 'test@example.com'
USERNAME = 'Test User'


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
