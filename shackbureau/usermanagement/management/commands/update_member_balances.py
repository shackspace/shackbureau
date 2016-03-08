# coding=utf-8
import datetime

from django.core.management import BaseCommand
from django.db.models import Min, Max, Q

from usermanagement.models import Balance, Member, AccountTransaction, Membership
from usermanagement.utils import get_shackbureau_user


class Command(BaseCommand):

    help = "Update balances of members"

    def handle(self, *args, **options):
        this_year = datetime.date.today().year
        shackbureau_user = get_shackbureau_user()
        for member in Member.objects.all():
            Membership.objects.fix_or_create_claims(member)
            transaction_dates = AccountTransaction.objects.filter(member=member)\
                                                          .aggregate(Max('due_date'), Min('due_date'))
            due_date_min = transaction_dates.get('due_date__min')
            due_date_max = transaction_dates.get('due_date__max')

            if not due_date_min and not due_date_max:
                Balance.objects.filter(member=member).delete()
                continue

            first_year = due_date_min.year
            last_year = min(due_date_max.year, this_year)

            Balance.objects.filter(member=member).filter(Q(year__lt=first_year) | Q(year__gt=last_year)).delete()
            print(member, first_year, last_year)
            for year in range(first_year, last_year + 1):
                Balance.objects.update_or_create(member=member,
                                                 year=year,
                                                 defaults={'created_by': shackbureau_user})
