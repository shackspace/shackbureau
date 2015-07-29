# coding=utf-8
import pytest


@pytest.mark.django_db
class TestMember:

    def test_member_id_set(self, member_fixture_transfer):
        assert member_fixture_transfer.member_id > 0

    def test_two_member_ids_set(self, member_fixture_transfer, member_fixture_sepa):
        assert member_fixture_sepa.member_id != member_fixture_transfer.member_id

    # not implemented yet
    @pytest.mark.xfail
    def test_join_date_set_to_month_start(self, member_fixture_transfer):
        assert member_fixture_transfer.join_date.day == 1


class TestSepa:

    @pytest.fixture(params=[
        ('64090100', '1234567', 'VBRTDE6RXXX', 'DE80640901000001234567'),
        (64090100, 1234567, 'VBRTDE6RXXX', 'DE80640901000001234567'),
        (11111111, 1111111111, False, 'DE63111111111111111111'),
    ])
    def iban_fixture(self, request):
        return dict(zip(('blz', 'kto', 'bic', 'iban'), request.param))

    def test_iban_creation(self, iban_fixture):
        from usermanagement.utils import konto_to_iban
        assert konto_to_iban(iban_fixture.get('blz'),
                             iban_fixture.get('kto')) == iban_fixture.get('iban')
