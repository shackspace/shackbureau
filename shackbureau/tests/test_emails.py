# coding=utf-8
import pytest
from django.template import Context
from django.template.loader import get_template


@pytest.mark.django_db
class TestMemberEmails:

    def test_welcome_mail_transfer(self, member_fixture_transfer):
        mail_content = get_template('welcome_mail.txt').render(Context(member_fixture_transfer.__dict__))
        assert mail_content.split('\n')[0] == 'Hallo {},'.format(member_fixture_transfer.name)
        assert 'überweise deinen Mitgliedsbeitrag' in mail_content
        assert not 'SEPA-Lastschriftmandat' in mail_content

    def test_welcome_mail_sepa(self, member_fixture_sepa):
        mail_content = get_template('welcome_mail.txt').render(Context(member_fixture_sepa.__dict__))
        assert mail_content.split('\n')[0] == 'Hallo {},'.format(member_fixture_sepa.name)
        assert not 'überweise deinen Mitgliedsbeitrag' in mail_content
        assert 'SEPA-Lastschriftmandat' in mail_content
        assert 'deine Mandatsreferenz lautet: ' + \
            'SHACKEVBEITRAGID{}.'.format(member_fixture_sepa.member_id) in mail_content

    def test_revoke_memberspecials_mail(self, member_fixture_keymember, member_fixture_memberspecials):
        ignore_fields = ["modified", 'signed_DSV', 'ssh_public_key', 'created',
                         'modified', 'created_by_id', 'id :', 'member_id']
        #test member_fixture_keymember
        specials = member_fixture_keymember.memberspecials.active_specials()
        content = get_template('revoke_memberspecials_mail.txt').render(Context({'specials': specials,
                                                                                 'member': member_fixture_keymember}))
        assert "is_keyholder : True" in content
        assert "has_matomat_key" not in content
        assert "has_selgros_card" not in content

        # ignored fields
        for special in ignore_fields:
            assert special not in content

        # test member_fixture_memberspecials
        specials = member_fixture_memberspecials.memberspecials.active_specials()
        content = get_template('revoke_memberspecials_mail.txt').render(Context({'specials': specials,
                                                                                 'member': member_fixture_memberspecials}))
        for special in ["has_matomat_key : True",
                        "has_selgros_card : True",
                        "has_matomat_key : True",
                        "has_snackomat_key : True",
                        "has_metro_card : True",
                        "has_selgros_card : True",
                        "has_shack_iron_key : True",
                        "has_safe_key : True",
                        "has_loeffelhardt_account : True"]:
            assert special in content

        assert "is_keyholder" not in content

        # ignored fields
        for special in ignore_fields:
            assert special not in content
