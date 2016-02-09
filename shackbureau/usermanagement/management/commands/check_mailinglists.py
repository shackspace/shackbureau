# coding=utf-8
from django.core.management import BaseCommand
from django.db.models import Q


class Command(BaseCommand):

    help = "Check mailinglist subscriptions"

    def handle(self, *args, **options):
        from usermanagement.models import Member
        from usermanagement.utils import is_on_mailinglist

        inactive_members = Member.objects.filter(is_active=False)
        active_members = Member.objects.filter(is_active=True)
        not_a_keyholder = Member.objects.filter(Q(is_active=False) | Q(memberspecials__is_keyholder=False))
        active_keyholder = Member.objects.filter(is_active=True, memberspecials__is_keyholder=True)

        inactive_members_on_announce = [member for member in inactive_members
                                        if is_on_mailinglist('mitglieder-announce', member.email)]
        if inactive_members_on_announce:
            print("\n### inactive members on mailinglist mitlgieder-announce")
            for member in inactive_members_on_announce:
                print("{} is inactive but on maillinglist mitlgieder-announce: {}".format(member, member.email))

        active_members_not_on_announce = [member for member in active_members
                                          if not is_on_mailinglist('mitglieder-announce', member.email)]
        if active_members_not_on_announce:
            print("\n### active members not on mailinglist mitlgieder-announce")
            for member in active_members_not_on_announce:
                print("{} is active but not on maillinglist mitlgieder-announce: {}".format(member, member.email))

        inactive_members_on_mitglieder = [member for member in inactive_members
                                          if is_on_mailinglist('mitglieder', member.email)]
        if inactive_members_on_mitglieder:
            print("\n### inactive members on mailinglist mitlgieder")
            for member in inactive_members_on_mitglieder:
                print("{} is inactive but on mailinglist mitlgieder: {}".format(member, member.email))

        not_a_keyholder_on_key = [member for member in not_a_keyholder
                                  if is_on_mailinglist('key', member.email)]
        if not_a_keyholder_on_key:
            print("\n### not keyholders on mailinglist key")
            for member in not_a_keyholder_on_key:
                print("{} is not a keyholder but on mailinglist key: {}".format(member, member.email))

        active_keyholder_not_on_key = [member for member in active_keyholder
                                       if not is_on_mailinglist('key', member.email)]
        if active_keyholder_not_on_key:
            print("\n### active keyholders not on mailinglist key")
            for member in active_keyholder_not_on_key:
                print("{} is a keyholder but not on mailinglist key: {}".format(member, member.email))
