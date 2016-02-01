# coding=utf-8
from django.core.management import BaseCommand


class Command(BaseCommand):

    help = "Send monthly statistic to mailinglist"

    # def add_arguments(self, parser):
    #     parser.add_argument('year', type=int)
    #     parser.add_argument('month', type=int)

    def handle(self, *args, **options):
        from usermanagement.views import send_member_statistic_mail

        from datetime import date, timedelta

        statistic_date = date.today()
        statistic_date = statistic_date.replace(day=1)  # get the first day off current month
        statistic_date = statistic_date - timedelta(days=1)  # get a date in the last month

        send_member_statistic_mail(statistic_date.year, statistic_date.month)
