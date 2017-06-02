# coding=utf-8
from django.core.management import BaseCommand

from usermanagement.models import Balance, Member


class Command(BaseCommand):

    help = "Update balances of members"

    def handle(self, *args, **options):
        for member in Member.objects.all():
            try:
                print(member)
            except:
                print('Member ID ' + str(member.member_id))
            Balance.objects.fix_or_create_balances(member)
