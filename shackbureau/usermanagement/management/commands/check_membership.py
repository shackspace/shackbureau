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

        for membership in Membership.objects.all():
            if membership.membership_fee_monthly < 20 and membership.membership_type == "full"\
                    or membership.membership_fee_monthly >= 20 and not membership.membership_type == "full":
                print("{} has in {} fee: {} but type: {}".format(membership.member, membership.valid_from, membership.membership_fee_monthly, membership.membership_type))
