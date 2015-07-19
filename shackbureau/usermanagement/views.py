from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage


def send_welcome_email(email_address, context):
    content = get_template('welcome_mail.txt').render(Context(context))

    email = EmailMessage('Hello', content, 'FROM@shackspace.de',
                         [email_address])
    email.send()
