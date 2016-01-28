# coding=utf-8
import pytest


@pytest.mark.django_db
class TestMemberEmails:

    def test_member_statistic(self, member_fixture_transfer, join_date_fixture, membership_fixture):
        from usermanagement.utils import member_statistic
        from decimal import Decimal
        statistic = member_statistic()
        assert len(statistic) > 0
        join_date = join_date_fixture.replace(day=1)
        for stat in statistic:
            if stat.date == join_date:
                assert stat.members > 0
                assert stat.fees[Decimal(membership_fixture.membership_fee_monthly)] > 0
        assert join_date in [stat.date for stat in statistic]
