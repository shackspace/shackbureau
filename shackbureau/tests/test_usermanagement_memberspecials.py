# coding=utf-8
import pytest


@pytest.mark.django_db
class TestMemberSpecial:

    def test_member_special_import(self, member_fixture_not_keymember, member_fixture_keymember, admin_fixture):
        from usermanagement.utils import update_keymember
        from usermanagement.models import Member
        ssh_key1 = "x"
        ssh_key2 = "y"

        update_keymember(member_fixture_not_keymember.member_id, ssh_key1)
        keymember1 = Member.objects.get(member_id=member_fixture_not_keymember.member_id)
        assert keymember1.memberspecials.is_keyholder is True
        assert keymember1.memberspecials.ssh_public_key == ssh_key1

        update_keymember(member_fixture_keymember.member_id, ssh_key2)
        keymember2 = Member.objects.get(member_id=member_fixture_keymember.member_id)
        assert keymember2.memberspecials.is_keyholder is True
        assert keymember2.memberspecials.ssh_public_key == ssh_key2
