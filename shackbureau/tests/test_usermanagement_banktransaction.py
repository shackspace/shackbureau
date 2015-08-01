# coding=utf-8
import pytest


class TestbankTransactionUploadParser:

    # it's real data, biatch
    @pytest.mark.parametrize(('reference', 'expected', 'score'), [
        ('shack e.V. Mitgliedsbeitrag ID 666 Dauerauftrag:         54', 666, 1),
        ('Beitrag MItglied 724             ', 724, 6),
        ('Beitrag shack AAAA AAAAAAA 466 AAAAAAA AAAA           ', False, 99),
        ('Beitrag shack AAAAAAAAAAAAA AAA 91            ', False, 99),
        ('Beitrag             ', False, 99),
        ('ID 167 AAA AAA             ', 167, 3),
        ('ID 325 MITGLIEDSBEITRAG AAA AAA  AAAAAAA ZV0100189577183000111002           ', 325, 2),
        ('MITGLIEDSBEITRAG ID 123             ', 123, 1),
        ('MITGLIEDSBEITRAG ID 371 9802            ', 371, 1),
        ('MITGLIEDSBEITRAG ID 959 ZV0101183786226509001002            ', 959, 1),
        ('Mitgliedsbeitrag 241             ', 241, 5),
        ('Mitgliedsbeitrag AAAAAA AAA AAAA ID 19 Dauerauftrag            ', 19, 3),
        ('Mitgliedsbeitrag AAAAAAA AA AA            ', False, 99),
        ('Mitgliedsbeitrag ID 091             ', 91, 1),
        ('Mitgliedsbeitrag ID 116             ', 116, 1),
        ('Mitgliedsbeitrag             ', False, 99),
        ('MitgliedsbeitragAAAAAA AAAA A 126Monatlich            ', 126, 7),
        ('shack e.V. Mitgliedsbeitrag ID 007 Dauerauftrag:         82           ', 7, 1),
        ('shack e.V. Mitgliedsbeitrag ID 111 Dauerauftrag:         61           ', 111, 1),
        ('shack e.V. Mitgliedsbeitrag ID 172 AAAAAAA AAAAAA Dauerauftrag:         70          ', 172, 1),
        ('shack e.V. Mitgliedsbeitrag ID 492 Dauerauftrag:         23           ', 492, 1),
    ])
    def test_reference_parser(self, reference, expected, score):
        from usermanagement.utils import reference_parser
        assert reference_parser(reference) == (expected, score)
