# coding=utf-8
from django.core.management import BaseCommand

from usermanagement.models import Member, Membership


class Command(BaseCommand):

    help = "Update fee_claims of members"

    def handle(self, *args, **options):
        for member in Member.objects.all():
            print(member)
            Membership.objects.fix_or_create_claims(member)
