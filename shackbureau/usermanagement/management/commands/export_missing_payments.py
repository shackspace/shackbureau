import csv
import os
import sys
from contextlib import redirect_stdout

from django.core.management import BaseCommand


def safe_print(string):

    result = ''
    with redirect_stdout(open(os.devnull, 'w')):
      for letter in string:
        try:
            print(letter)
            result += letter
        except:
            result += '_'
    return result


class Command(BaseCommand):

    help = 'Export members with missing payments to CSV'

    def handle(self, *args, **options):
        result = []

        for member in Member.objects.all():
            result.append({
                'member': member,
                'balance': member.balance_set.order_by('-year').first()
            })

        filtered_result = [
            r for r in result
            if r['balance'] and (r['balance'].balance < -20 or r['balance'].accumulated_balance < -20)
        ]
        output = [
            {
                'member_id': r['member'].member_id,
                'nickname': safe_print(r['member'].nickname),
                'name': safe_print(r['member'].name) + ' ' + safe_print(r['member'].surname),
                'email': safe_print(r['member'].email),
                'is_active': r['member'].is_active,
                'leave_date':  r['member'].leave_date,
                'year': r['balance'].year,
                'balance': r['balance'].balance,
                'accumulated_balance': r['balance'].accumulated_balance
            }
            for r in filtered_result
        ]

        d = csv.DictWriter(sys.stdout, fieldnames=['member_id', 'nickname', 'name', 'email', 'is_active', 'leave_date', 'year', 'balance', 'accumulated_balance'])
        d.writeheader()

        for element in output:
            d.writerow(element)
