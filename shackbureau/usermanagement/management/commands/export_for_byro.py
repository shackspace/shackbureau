# coding=utf-8
import json
from os import path

from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):

    help = "Export everything for byro!"

    def handle(self, *args, **options):
        from usermanagement.models import Member

        members_list = []
        for member in Member.objects.order_by("member_id"):
            member_dict = {
                'number': member.member_id,
                'name': member.name + ' ' + member.surname,
                'address': member.get_postal_address(),
                'email': member.email,
                # profile plugin
                'profile__nick': member.nickname,
                'profile__birth_date': str(member.date_of_birth or ''),
                'profile__phone_number': member.phone_number,
                # sepa plugin
                'sepa__iban': member.iban,
                'sepa__bic': member.bic,
                'sepa__institute': member.iban_institute,
                'sepa__issue_date': str(member.iban_issue_date or ''),
                'sepa__fullname': member.iban_fullname,
                'sepa__address': member.iban_address,
                'sepa__zip_code': member.iban_zip_code,
                'sepa__city': member.iban_city,
                'sepa__country': member.iban_country,
                'sepa__mandate_reference': member.get_mandate_reference(),
                'sepa__mandate_reason': member.get_mandate_reason(),
                # membership management
                'payment_type' : member.payment_type,
                'join_date': str(member.join_date or ''),
                'leave_date': str(member.leave_date or ''),
            }
            transactions = []
            for btrans in member.banktransactionlog_set.all():
                transactions.append({
                    'booking_date': str(btrans.booking_date),
                    'debitor_id': str(btrans.debitor_id),
                    'reference': btrans.reference,
                    'transaction_owner': btrans.transaction_owner,
                    'amount': str(btrans.amount),
                })
            member_dict['bank_transactions'] = transactions

            transactions = []
            for atrans in member.accounttransaction_set.all():
                transactions.append({
                    'amount': str(atrans.amount),
                    'booking_date': str(atrans.booking_date),
                    'due_date': str(atrans.due_date),
                    'booking_type': str(atrans.booking_type),
                    'payment_reference': str(atrans.payment_reference),
                    'transaction_type': str(atrans.transaction_type),
                })
            member_dict['account_transactions'] = transactions

            memberships = []
            for membership in member.membership_set.all():
                memberships.append({
                    "membership_start": str(membership.valid_from),
                    "membership_fee_monthly": str(membership.membership_fee_monthly),
                    "membership_type": membership.membership_type,
                    "membership_fee_interval": membership.membership_fee_interval
                })
            member_dict['memberships'] = memberships

            members_list.append(member_dict)
        with open(path.join(settings.EXPORT_ROOT, "shack2byro.json"), "w") as fp:
            json.dump(members_list, fp, sort_keys=True, indent=2)
