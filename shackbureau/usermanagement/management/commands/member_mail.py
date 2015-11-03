# coding=utf-8
from django.core.management import BaseCommand
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.contrib.auth.models import User


class Command(BaseCommand):

    help = "Sends an email to all active members"

    def handle(self, *args, **options):
        from usermanagement.models import Member, MemberTrackingCode
        for member in Member.objects.filter(is_active=True):
            if not member.email:
                continue

            uuid = MemberTrackingCode.objects.create(member=member,
                                                     created_by=User.objects.get(username="admin"))
            context = {
                'uuid': uuid,
                'member': member,
            }
            content = get_template('active_member_mail.txt').render(Context(context))

            print(member.email)

            email = EmailMessage('Deine Mitgliedsdaten',
                                 content,
                                 'tt-vorstand@shackspace.de',
                                 [member.email])
            email.send()
