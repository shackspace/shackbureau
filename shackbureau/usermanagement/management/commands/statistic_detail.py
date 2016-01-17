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
        parser.add_argument('month', type=int)

    def handle(self, *args, **options):
        from usermanagement.models import Member
        import datetime
        from usermanagement.models import Membership

        year = options['year']
        month = options['month']

        date = datetime.date(year, month, 1)
        members = Member.objects.get_active_members(date)

        mitglieder = len(members)
        erm = 0
        voll = 0
        summe = 0
        fees = dict()

        for member in members:
            membership = Membership.objects.get_current_membership(member, date)
            if membership.membership_type == 'full':
                voll += 1
            else:
                erm += 1

            fee = membership.membership_fee_monthly
            summe += fee
            if fee in fees:
                fees[fee] += 1
            else:
                fees[fee] = 1

        print("Mitglieder: {}".format(mitglieder))
        print("Ermäßigt: {}".format(erm))
        print("Voll: {}".format(voll))
        print("Summer: {}".format(summe))
        print("Beiträge:")
        for fee in fees:
            print("{}: {}".format(fee, fees[fee]))
