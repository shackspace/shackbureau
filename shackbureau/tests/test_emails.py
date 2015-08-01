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

    def test_welcome_mail_sepa(self, member_fixture_sepa):
        mail_content = get_template('welcome_mail.txt').render(Context(member_fixture_sepa.__dict__))
        assert mail_content.split('\n')[0] == 'Hallo {},'.format(member_fixture_sepa.name)
        assert not 'überweise deinen Mitgliedsbeitrag' in mail_content
        assert 'SEPA-Lastschriftmandat' in mail_content
        assert 'deine Mandatsreferenz lautet: ' + \
            'shack e.V. Mitgliedsbeitrag ID {}.'.format(member_fixture_sepa.member_id) in mail_content
