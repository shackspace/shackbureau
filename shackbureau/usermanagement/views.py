from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Membership
from .utils import member_statistic


def send_welcome_email(member):
    content = get_template('welcome_mail.txt').render({'member': member})

    return member.send_email(subject='Willkommen im shack e.V.',
                             body=content,
                             cc=['vorstand@shackspace.de'],
                             )


def payment_mail_content(membership):
    membership_fee = membership.membership_fee_monthly * membership.membership_fee_interval
    membership_interval = "alle {} Monate".format(membership.membership_fee_interval)
    if membership.membership_fee_interval == 1:
        membership_interval = "monatlich"
    if membership.membership_fee_interval == 12:
        membership_interval = "jährlich"

    all_memberships = Membership.objects.filter(member=membership.member).order_by("valid_from")
    all_memberships = list(all_memberships)
    if membership not in all_memberships:
        all_memberships.append(membership)
    all_memberships = sorted(all_memberships, key=lambda x: x.valid_from)

    context = {"member": membership.member,
               "membership": membership,
               "membership_fee": membership_fee,
               "membership_interval": membership_interval,
               "all_memberships": all_memberships}
    template = get_template('payment_mail.txt')

    return template.render(context)


def send_payment_email(membership):
    if membership.valid_from == membership.member.join_date:
        action = "New"
    else:
        action = "Update"
    content = payment_mail_content(membership)

    email = EmailMessage(subject='{} payment für {} {}'.format(action,
                                                               membership.member.name,
                                                               membership.member.surname),
                         body=content,
                         to=[settings.CASHMASTER_MAILADDR])
    ret = email.send()
    return ret


def send_cancellation_mail_to_cashmaster(member):
    content = get_template('payment_mail_on_cancellation.txt').render({'member': member})

    email = EmailMessage(subject='Payment cancelation für {} {}'.format(member.name,
                                                                        member.surname),
                         body=content,
                         to=[settings.CASHMASTER_MAILADDR])
    ret = email.send()
    return ret


def send_nagging_email(accounttransaction):
    member = accounttransaction.member
    content = get_template('nagging_mail.txt').render({'accounttransaction': accounttransaction,
                                                       'member': member})

    return member.send_email(email_type="nagging",
                             subject='Bitte Verwendungszweck anpassen',
                             body=content,
                             cc=['vorstand@shackspace.de'])


def send_revoke_memberspecials_mail(member):
    if not hasattr(member, "memberspecials"):
        return 0
    specials = member.memberspecials.active_specials()
    if not specials:
        return 0

    content = get_template('revoke_memberspecials_mail.txt').render({'specials': specials,
                                                                     'member': member})

    email = EmailMessage(subject='Revoke Memberspecials for {}'.format(member),
                         body=content,
                         to=['help@shackspace.de'])
    ret = email.send()
    return ret


def send_member_statistic_mail(year, month):
    statistic = member_statistic(year, month)

    content = get_template('member_statistic_mail.txt').render({'statistic': statistic})

    email = EmailMessage(subject='Mitglieder Statistik {:04d}-{:02d}'.format(year, month),
                         body=content,
                         to=['mitglieder@shackspace.de'])
    ret = email.send()
    return ret
