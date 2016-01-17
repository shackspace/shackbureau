# coding=utf-8
from django.core.management import BaseCommand
# from django.template import Context
# from django.template.loader import get_template
# from os import path
# from django.conf import settings


class Command(BaseCommand):

    help = "Some statistic."

    def add_arguments(self, parser):
        parser.add_argument('year', type=int)

    def handle(self, *args, **options):
        from usermanagement.models import Member
        import datetime
        from usermanagement.models import Membership

        statistic = [["Monat", "Mitglieder", "Ermäßigt", "Voll", "Summe"]]

        year = options['year']

        for month in range(1, 13):
            date = datetime.date(year, month, 1)
            members = Member.objects.get_active_members(date)

            mitglieder = len(members)
            erm = 0
            voll = 0
            summe = 0

            for member in members:
                membership = Membership.objects.get_current_membership(member, date)
                if membership.membership_type == 'full':
                    voll += 1
                else:
                    erm += 1

                summe += membership.membership_fee_monthly

            statistic.append([month, mitglieder, erm, voll, summe])

        for stat in statistic:
            print(stat)
