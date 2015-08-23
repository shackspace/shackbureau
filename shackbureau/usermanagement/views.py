from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings


def send_welcome_email(email_address, context):
    content = get_template('welcome_mail.txt').render(Context(context))

    email = EmailMessage('Willkommen im shack e.V.', content, 'no-reply@vorstand.shack.space',
                         [email_address],
                         ['vorstand@shackspace.de'], reply_to=['vorstand@shackspace.de'])
    email.send()


def send_payment_email(context):
    content = get_template('payment_mail.txt').render(Context(context))

    email = EmailMessage('Payment für {} {}'.format(context.get('name'),
                                                    context.get('surname')),
                         content, 'no-reply@vorstand.shack.space',
                         [settings.CASHMASTER_MAILADDR])
    email.send()


def send_cancellation_mail_to_cashmaster(context):
    content = get_template('payment_mail_on_cancellation.txt').render(Context(context))

    email = EmailMessage('Payment für {} {}'.format(context.get('name'),
                                                    context.get('surname')),
                         content, 'no-reply@vorstand.shack.space',
                         [settings.CASHMASTER_MAILADDR])
    email.send()


def send_nagging_email(email_address, context):
    content = get_template('nagging_mail.txt').render(Context(context))

    email = EmailMessage('Nagging für {} {}'.format(context.get('name'),
                                                    context.get('surname')),
                         content, 'no-reply@vorstand.shack.space',
                         [email_address],
                         ['vorstand@shackspace.de'], reply_to=['vorstand@shackspace.de'])
    email.send()
