# coding=utf-8
import pytest
from django.template.loader import get_template


@pytest.mark.django_db
class TestMemberEmails:

    def test_welcome_mail_transfer(self, member_fixture_transfer):
        mail_content = get_template('welcome_mail.txt').render({'member': member_fixture_transfer})
        assert mail_content.split('\n')[0] == 'Hallo {},'.format(member_fixture_transfer.name)
        assert 'überweise deinen Mitgliedsbeitrag' in mail_content
        assert 'shack e.V. Mitgliedsbeitrag ID {}'.format(member_fixture_transfer.member_id) in mail_content
        assert 'SEPA-Lastschriftmandat' not in mail_content

    def test_welcome_mail_sepa(self, member_fixture_sepa):
        mail_content = get_template('welcome_mail.txt').render({'member': member_fixture_sepa})
        assert mail_content.split('\n')[0] == 'Hallo {},'.format(member_fixture_sepa.name)
        assert 'überweise deinen Mitgliedsbeitrag' not in mail_content
        assert 'SEPA-Lastschriftmandat' in mail_content
        assert 'deine Mandatsreferenz lautet: ' + \
            'SHACKEVBEITRAGID{:04d}'.format(member_fixture_sepa.member_id) in mail_content

    def test_revoke_memberspecials_mail(self, member_fixture_keymember, member_fixture_memberspecials):
        ignore_fields = ["modified", 'signed_DSV', 'ssh_public_key', 'created',
                         'modified', 'created_by_id', 'id :', 'member_id']
        # test member_fixture_keymember
        specials = member_fixture_keymember.memberspecials.active_specials()
        content = get_template('revoke_memberspecials_mail.txt').render({'specials': specials,
                                                                         'member': member_fixture_keymember})
        assert "is_keyholder : True" in content
        assert "has_matomat_key" not in content
        assert "has_selgros_card" not in content

        # ignored fields
        for special in ignore_fields:
            assert special not in content

        # test member_fixture_memberspecials
        specials = member_fixture_memberspecials.memberspecials.active_specials()
        content = get_template('revoke_memberspecials_mail.txt') \
            .render({'specials': specials,
                     'member': member_fixture_memberspecials})
        for special in ["has_matomat_key : True",
                        "has_selgros_card : True",
                        "has_matomat_key : True",
                        "has_snackomat_key : True",
                        "has_laser_key : True",
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

    def test_payment_mail_sepa(self, membership_fixture_sepa, user_fixture):
        from usermanagement.views import payment_mail_content
        content = payment_mail_content(membership_fixture_sepa)

        import re
        assert re.search("Eintrittsdatum:\s+{}".format(membership_fixture_sepa.member.join_date.isoformat()), content)
        assert re.search("Mandatsdatum:\s+{}".format(membership_fixture_sepa.member.iban_issue_date.isoformat()),
                         content)
        assert re.search("Mandatsreferenz:\s+SHACKEVBEITRAGID{:04d}".format(membership_fixture_sepa.member.member_id),
                         content)
        assert re.search("Mandatsgrund:\s+shack e\.V\. Mitgliedsbeitrag ID {}"
                         .format(membership_fixture_sepa.member.member_id),
                         content)
        assert re.search("Kontoinhaber:\s+{}".format(membership_fixture_sepa.member.iban_fullname), content)
        assert re.search("Straße:\s+{}".format(membership_fixture_sepa.member.iban_address), content)
        assert re.search("Postleitzahl:\s+{}".format(membership_fixture_sepa.member.iban_zip_code), content)
        assert re.search("Ort:\s+{}".format(membership_fixture_sepa.member.iban_city), content)
        if membership_fixture_sepa.member.bic:
            assert re.search("BIC:\s+{}".format(membership_fixture_sepa.member.bic), content)
        assert re.search("IBAN:\s+{}".format(membership_fixture_sepa.member.iban), content)
        assert re.search("Mitgliedsbeitrag:\s+\d+", content)
        if membership_fixture_sepa.membership_fee_interval == 1:
            assert re.search("Interval:\s+monatlich", content)
        elif membership_fixture_sepa.membership_fee_interval == 12:
            assert re.search("Interval:\s+jährlich", content)
        else:
            assert re.search("Interval:\s+alle {} Monate".format(membership_fixture_sepa.membership_fee_interval),
                             content)
        assert re.search("Gültig ab:\s+{}".format(membership_fixture_sepa.valid_from.isoformat()), content)
        for ms in membership_fixture_sepa.member.membership_set.all():
            assert re.search("{}\s+-\s+{}".format(ms.valid_from.isoformat(), ms.membership_fee_monthly), content)
        assert "Diese Änderung wurde von {} veranlasst.".format(membership_fixture_sepa.created_by.username) in content
