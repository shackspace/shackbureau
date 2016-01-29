# coding=utf-8
from django.core.management import BaseCommand

from usermanagement.models import Member, Membership
from django.db.models import Q

def get_member_without_membership_on_join_date():
    members = []
    for member in Member.objects.all():
        membership = Membership.objects.get_current_membership(member, member.join_date)
        if not membership:
            members.append(member)
    return members


class Command(BaseCommand):

    help = "Check consitence of data in usermanagement"

    def handle(self, *args, **options):
        # members = Member.objects
        for member in get_member_without_membership_on_join_date():
            print("{} has no active membership for {}".format(member, member.join_date))

        #check reduced means <20 and full >=20
        memberships = Membership.objects.filter((Q(membership_fee_monthly__lt=20) & Q(membership_type="full")) |
                                                (Q(membership_fee_monthly__gte=20) & Q(membership_type="reduced")))
        for membership in memberships:
            print("{} has in {} fee: {} but type: {}".format(membership.member,
                                                             membership.valid_from,
                                                             membership.membership_fee_monthly,
                                                             membership.membership_type))

        #inconsistent_is_active_leave_date
        members = Member.objects.filter(
            (Q(is_active=True) & (Q(leave_date__isnull=False) | Q(is_cancellation_confirmed=True))) |
            (Q(is_active=False) & Q(leave_date__isnull=True))
        )
        for member in members:
            print("{} has inconsitent leave state".format(member))
