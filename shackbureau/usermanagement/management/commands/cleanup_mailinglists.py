# coding=utf-8
from django.core.management import BaseCommand
from django.db.models import Q

from usermanagement.utils import (
    is_allowed_on_mitglieder_mailinglist,
    is_allowed_on_key_mailinglist,
    remove_from_mailinglist,
)


class Command(BaseCommand):

    help = "Cleanup mailinglist subscriptions"

    def handle(self, *args, **options):
        from usermanagement.models import Member
        from usermanagement.utils import is_on_mailinglist

        inactive_members = Member.objects.get_inactive_members()
        not_a_keyholder = Member.objects.filter(Q(is_active=False) | Q(memberspecials__is_keyholder=False))

        inactive_members_on_announce = [
            member for member in inactive_members
            if is_on_mailinglist('mitglieder-announce', member.email) and
            not is_allowed_on_mitglieder_mailinglist(member.email)
        ]
        if inactive_members_on_announce:
            print("\n### inactive members on mailinglist mitlgieder-announce")
            for member in inactive_members_on_announce:
                print("{} is inactive but on maillinglist mitlgieder-announce: {}".format(member, member.email))
                remove_from_mailinglist('mitglieder-announce', member.email)

        inactive_members_on_mitglieder = [
            member for member in inactive_members
            if is_on_mailinglist('mitglieder', member.email) and
            not is_allowed_on_mitglieder_mailinglist(member.email)
        ]
        if inactive_members_on_mitglieder:
            print("\n### inactive members on mailinglist mitlgieder")
            for member in inactive_members_on_mitglieder:
                print("{} is inactive but on mailinglist mitlgieder: {}".format(member, member.email))
                remove_from_mailinglist('mitglieder', member.email)

        not_a_keyholder_on_key = [
            member for member in not_a_keyholder
            if is_on_mailinglist('key', member.email) and
            not is_allowed_on_key_mailinglist(member.email)
        ]
        if not_a_keyholder_on_key:
            print("\n### not keyholders on mailinglist key")
            for member in not_a_keyholder_on_key:
                print("{} is not a keyholder but on mailinglist key: {}".format(member, member.email))
                remove_from_mailinglist('key', member.email)
