# coding=utf-8
from django.core.management import BaseCommand


class Command(BaseCommand):

    help = "Check existence of valid Memberships for each Member"

    # def add_arguments(self, parser):
    #     parser.add_argument('year', type=int)

    def handle(self, *args, **options):
        from usermanagement.models import Member, Membership
        # import datetime

        for member in Member.objects.all():
            membership = Membership.objects.get_current_membership(member, member.join_date)
            if not membership:
                print("{} has no active membership for {}".format(member, member.join_date))


        # for month in range(1, 13):
        #     date = datetime.date(year, month, 1)
        #     members = Member.objects.get_active_members(date)
        #
        #     mitglieder = len(members)
        #     erm = 0
        #     voll = 0
        #     summe = 0
        #
        #     for member in members:
        #         membership = Membership.objects.get_current_membership(member, date)
        #         if not membership:
        #             print("{} has no active membership for {}".format(member, date))
        #             continue
        #         if membership.membership_type == 'full':
        #             voll += 1
        #         else:
        #             erm += 1
        #
        #         summe += membership.membership_fee_monthly
        #
        #     statistic.append([month, mitglieder, erm, voll, summe])
        #
        # for stat in statistic:
        #     print(stat)
