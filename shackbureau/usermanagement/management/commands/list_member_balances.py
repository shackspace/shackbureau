# coding=utf-8
from django.core.management import BaseCommand

from usermanagement.models import Member, Balance


class Command(BaseCommand):

    help = "list balance of members"

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--inactive',
                            action='store_true',
                            dest='inactive',
                            default=False,
                            help='check on members with is_active == False')

    def handle(self, *args, **options):
        members = Member.objects.all()
        if options['inactive']:
            members = members.filter(is_active=False)

        for member in members:
            balance = Balance.objects.filter(member=member).order_by('year').last()
            if not balance:
                print("{member:50} ### has no balance".format(member=str(member)))
                continue
            print("{member:50} {year} {balance:8.2f}".format(member=str(member),
                                                             year=balance.year,
                                                             balance=balance.accumulated_balance))
