from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import member_statistic


def send_welcome_email(email_address, context):
    content = get_template('welcome_mail.txt').render(Context(context))

    email = EmailMessage('Willkommen im shack e.V.', content, 'vorstand@shackspace.de',
                         [email_address],
                         ['vorstand@shackspace.de'], reply_to=['vorstand@shackspace.de'])
    ret = email.send()
    return ret


def send_payment_email(membership):
    membership_fee = membership.membership_fee_monthly * membership.membership_fee_interval
    membership_interval = "alle {} Monate".format(membership.membership_fee_interval)
    if membership.membership_fee_interval == 1:
        membership_interval = "monatlich"
    if membership.membership_fee_interval == 12:
        membership_interval = "jährlich"

    if membership.valid_from == membership.member.join_date:
        action = "New"
    else:
        action = "Update"

    context = Context({"member": membership.member,
                       "membership": membership,
                       "membership_fee": membership_fee,
                       "membership_interval": membership_interval})
    if action.lower() == "new":
        template = get_template('payment_mail_new_member.txt')
    else:
        template = get_template('payment_mail_update_member.txt')

    content = template.render(context)

    email = EmailMessage('{} payment für {} {}'.format(action,
                                                        membership.member.name,
                                                        membership.member.surname),
                         content, 'vorstand@shackspace.de',
                         [settings.CASHMASTER_MAILADDR])
    ret = email.send()
    return ret


def send_cancellation_mail_to_cashmaster(context):
    content = get_template('payment_mail_on_cancellation.txt').render(Context(context))

    email = EmailMessage('Payment cancelation für {} {}'.format(context.get('name'),
                                                    context.get('surname')),
                         content, 'vorstand@shackspace.de',
                         [settings.CASHMASTER_MAILADDR])
    ret = email.send()
    return ret


def send_nagging_email(email_address, context):
    content = get_template('nagging_mail.txt').render(Context(context))

    email = EmailMessage('Nagging für {} {}'.format(context.get('name'),
                                                    context.get('surname')),
                         content, 'vorstand@shackspace.de',
                         [email_address],
                         ['vorstand@shackspace.de'], reply_to=['vorstand@shackspace.de'])
    ret = email.send()
    return ret


def send_revoke_memberspecials_mail(member):
    if not hasattr(member, "memberspecials"):
        return 0
    specials = member.memberspecials.active_specials()
    if not specials:
        return 0

    content = get_template('revoke_memberspecials_mail.txt').render(Context({'specials': specials,
                                                                             'member': member}))

    email = EmailMessage('Revoke Memberspecials for {}'.format(member),
                         content, 'vorstand@shackspace.de',
                         ['tt-vorstand@shackspace.de'],
                         [])
    ret = email.send()
    return ret


def send_member_statistic_mail(year, month):
    statistic = member_statistic(year, month)

    content = get_template('member_statistic_mail.txt').render(Context({'statistic': statistic}))

    email = EmailMessage('Mitglieder Statistik {}-{}'.format(year, month),
                         content, 'vorstand@shackspace.de',
                         ['mitglieder@shackspace.de'],
                         [])
    ret = email.send()
    return ret
