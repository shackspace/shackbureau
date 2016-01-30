from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings
from usermanagement.models import Membership, MemberSpecials


def send_welcome_email(email_address, context):
    content = get_template('welcome_mail.txt').render(Context(context))

    email = EmailMessage('Willkommen im shack e.V.', content, 'vorstand@shackspace.de',
                         [email_address],
                         ['vorstand@shackspace.de'], reply_to=['vorstand@shackspace.de'])
    email.send()


def send_payment_email(member):
    membership_fee = None
    membership_interval = None
    membership = Membership.objects.get_current_membership(member, member.join_date)
    if membership:
        membership_fee = membership.membership_fee_monthly * membership.membership_fee_interval
        membership_interval = "alle {} Monate".format(membership.membership_fee_interval)
        if membership.membership_fee_interval == 1:
            membership_interval = "monatlich"
        if membership.membership_fee_interval == 12:
            membership_interval = "jährlich"

    context = Context({"member": member,
                       "membership": membership,
                       "membership_fee": membership_fee,
                       "membership_interval": membership_interval})
    content = get_template('payment_mail.txt').render(context)

    email = EmailMessage('Payment für {} {}'.format(member.name,
                                                    member.surname),
                         content, 'vorstand@shackspace.de',
                         [settings.CASHMASTER_MAILADDR])
    email.send()


def send_cancellation_mail_to_cashmaster(context):
    content = get_template('payment_mail_on_cancellation.txt').render(Context(context))

    email = EmailMessage('Payment für {} {}'.format(context.get('name'),
                                                    context.get('surname')),
                         content, 'vorstand@shackspace.de',
                         [settings.CASHMASTER_MAILADDR])
    email.send()


def send_nagging_email(email_address, context):
    content = get_template('nagging_mail.txt').render(Context(context))

    email = EmailMessage('Nagging für {} {}'.format(context.get('name'),
                                                    context.get('surname')),
                         content, 'vorstand@shackspace.de',
                         [email_address],
                         ['vorstand@shackspace.de'], reply_to=['vorstand@shackspace.de'])
    email.send()


def send_revoke_memberspecials_mail(member):
    memberspecials = MemberSpecials.objects.filter(member=member).first()
    if not memberspecials:
        return
    specials = dict(memberspecials.__dict__)
    for key in [k for k in specials.keys() if k[0]=="_" ]:
        specials.pop(key)
    ignore_specials = set(['signed_DSV', 'ssh_public_key'])
    for key in set(['created', 'created_by_id', 'id', 'member_id', 'modified', 'ssh_public_key']).intersection(specials.keys()).union(ignore_specials):
        specials.pop(key)
    specials = [(k, v) for k, v in specials.items() if v]
    if not specials:
        return

    content = get_template('revoke_memberspecials_mail.txt').render(Context({'specials': specials,
                                                                             'member': member}))

    email = EmailMessage('Revoke Memberspecials for {}'.format(memberspecials.member),
                         content, 'vorstand@shackspace.de',
                         ['tt-vorstand@shackspace.de'],
                         [])
    email.send()
