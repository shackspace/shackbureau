# coding=utf-8

from django.core.management import BaseCommand

from districtcourt.models import DistrictcourtBalance, Debitor
from usermanagement.utils import get_shackbureau_user


class Command(BaseCommand):

    help = "Update balances of districtcourt debitors"

    def handle(self, *args, **options):
        shackbureau_user = get_shackbureau_user()
        for debitor in Debitor.objects.all():
            print(debitor)
            DistrictcourtBalance.objects.update_or_create(debitor=debitor,
                                                          defaults={'created_by': shackbureau_user})
