# coding=utf-8
import pytest


@pytest.mark.django_db
class TestMemberSpecial:

    def test_member_special(self, member_fixture_keymember, member_fixture_transfer):
        assert member_fixture_keymember == member_fixture_transfer

    def test_member_special_import(self, member_fixture_keymember, admin_fixture):
        from usermanagement.utils import update_keymember
        ssh_key = "x"
        update_keymember(member_fixture_keymember.member_id, ssh_key)
        assert member_fixture_keymember.memberspecials_set.first().is_keyholder == True
        assert member_fixture_keymember.memberspecials_set.first().ssh_public_key == ssh_key



