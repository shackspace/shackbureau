# coding=utf-8
import pytest


@pytest.mark.django_db
class TestMemberEmails:

    def test_letter(self, letter_fixture):
        self.check_documents_creation(letter_fixture)

    def test_donationreceipt(self, donationreceipt_fixture):
        self.check_documents_creation(donationreceipt_fixture)

    def test_dataprotectionagreement(self, dataprotectionagreement_fixture):
        self.check_documents_creation(dataprotectionagreement_fixture)

    def check_documents_creation(self, document):
        from os import path
        from subprocess import getoutput
        assert document.data_file
        filename = document.data_file.file.name
        assert path.isfile(filename)
        root, ext = path.splitext(filename)
        assert ext == ".pdf"
        output = getoutput('file {}'.format(filename))
        assert output.split(':', 1)[1].strip() == "PDF document, version 1.5"
