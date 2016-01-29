# coding=utf-8
import pytest


@pytest.mark.django_db
class TestMemberUtils:

    def test_member_utils_last_day_of_month(self):
        from usermanagement.utils import last_day_of_month
        from datetime import date
        assert last_day_of_month(date(2015, 1, 24)) == date(2015, 1, 31)
        assert last_day_of_month(date(2016, 2, 28)) == date(2016, 2, 29)  # leap year
        assert last_day_of_month(date(2015, 2, 28)) == date(2016, 2, 28)  # not a leap year
        assert last_day_of_month(date(2014, 12, 3)) == date(2014, 12, 31)
        assert last_day_of_month(date(1994, 1, 1)) == date(1994, 1, 31)
        assert last_day_of_month(date(2023, 12, 24)) == date(2023, 12, 31)
