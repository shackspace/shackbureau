# coding=utf-8
import datetime
import pytest


@pytest.fixture
def memberships_fixture_very_simple(member_fixture_transfer, first_of_this_month):
    member_fixture_transfer.membership_set.create(
        valid_from=first_of_this_month,
        created_by=member_fixture_transfer.created_by)
    return member_fixture_transfer.membership_set


@pytest.fixture
def memberships_fixture_change_fee(memberships_fixture_very_simple, first_of_this_month, first_of_next_month):
    membership_set = memberships_fixture_very_simple.first().member.membership_set
    membership_set.create(
        valid_from=first_of_next_month,
        membership_fee_monthly=42,
        created_by=membership_set.first().member.created_by)
    return membership_set


@pytest.fixture
def memberships_fixture_change_type(memberships_fixture_very_simple, first_of_this_month, first_of_previous_month):
    membership_set = memberships_fixture_very_simple.first().member.membership_set
    membership_set.create(
        valid_from=first_of_previous_month,
        membership_type='reduced',
        membership_fee_monthly=8,
        created_by=membership_set.first().member.created_by)
    return membership_set


@pytest.fixture
def memberships_fixture_with_leave(member_fixture_transfer, first_of_this_month, first_of_next_month):
    member_fixture_transfer.leave_date = first_of_next_month
    member_fixture_transfer.save()
    member_fixture_transfer.membership_set.create(
        valid_from=first_of_this_month,
        created_by=member_fixture_transfer.created_by)
    return member_fixture_transfer.membership_set


@pytest.mark.django_db
class TestMemberShipManager:

    def test_membership(self, memberships_fixture_very_simple):
        assert memberships_fixture_very_simple.count() == 1
        x = memberships_fixture_very_simple.first()
        assert x.membership_fee_monthly == 20

    def test_membership_join_date_valid_from(self, memberships_fixture_very_simple):
        x = memberships_fixture_very_simple.first()
        assert x.valid_from.day == 1
        assert x.valid_from >= x.member.join_date

    @pytest.mark.parametrize(('day', 'expected'), [
        (datetime.date(2015, 1, 1), 12 + 12),
        (datetime.date(2015, 12, 1), 12 + 1),
        (datetime.date(2015, 7, 1), 12 + 6),
    ])
    def test_clarify_expected_months(self, day, expected):
        """ only to show how we expect the behaviour of expected months
        """
        assert 12 - day.month + 1 + 12 == expected

    def test_membership_created_claims_very_simple(self, memberships_fixture_very_simple, join_date_fixture):
        x = memberships_fixture_very_simple.first()
        today = datetime.date.today()
        expected_months = 12 - join_date_fixture.month + 1 + (today.year - join_date_fixture.year + 1) * 12
        assert x.member.accounttransaction_set.count() == expected_months

    def test_membership_created_claims_change_type(self, memberships_fixture_change_type, first_of_this_month,
                                                   first_of_next_month, first_of_previous_month):
        x = memberships_fixture_change_type.first()
        today = datetime.date.today()
        expected_months = 12 - first_of_previous_month.month + 1 + (today.year - first_of_previous_month.year + 1) * 12
        assert x.member.accounttransaction_set.count() == expected_months
        assert x.member.accounttransaction_set.filter(
            due_date=first_of_next_month).first().amount == -20
        assert x.member.accounttransaction_set.filter(
            due_date=first_of_previous_month).first().amount == -8
        # the month the fee changed is the current month
        assert x.member.accounttransaction_set.filter(
            due_date=first_of_this_month).first().amount == -20

    def test_membership_created_claims_change_fee(self, memberships_fixture_change_fee,
                                                  first_of_next_month, join_date_fixture):
        x = memberships_fixture_change_fee.first()
        today = datetime.date.today()
        expected_months = 12 - join_date_fixture.month + 1 + (today.year - join_date_fixture.year + 1) * 12
        assert x.member.accounttransaction_set.count() == expected_months
        assert x.member.accounttransaction_set.filter(
            due_date=first_of_next_month).first().amount == -42

    def test_membership_created_with_leave(self, memberships_fixture_with_leave):
        x = memberships_fixture_with_leave.first()
        # joined this month. leave next month
        expected_months = 1
        assert x.member.accounttransaction_set.count() == expected_months

    def test_membership_booking_date_persists_on_update(self, memberships_fixture_very_simple, first_of_next_month):
        x = memberships_fixture_very_simple.first()
        # save booking date
        booking_date = x.member.accounttransaction_set.first().booking_date
        modified = x.member.accounttransaction_set.first().modified
        assert x.member.accounttransaction_set.first().amount == -20
        # change
        x.membership_fee_monthly = 23
        x.save()
        # check for persistance
        assert x.member.accounttransaction_set.first().booking_date == booking_date
        assert x.member.accounttransaction_set.first().amount == -23
        assert not x.member.accounttransaction_set.first().modified == modified
