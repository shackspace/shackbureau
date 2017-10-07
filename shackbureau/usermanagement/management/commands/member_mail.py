# coding=utf-8
from django.core.management import BaseCommand
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage

from usermanagement.utils import get_shackbureau_user


class Command(BaseCommand):

    help = "Sends an email to all active members"

    def handle(self, *args, **options):
        from usermanagement.models import Member, MemberTrackingCode
        for member in Member.objects.filter(is_active=True):
            if not member.email:
                continue

            uuid, created = MemberTrackingCode.objects.get_or_create(member=member,
                                                                     created_by=get_shackbureau_user())
            if uuid.validated:
                continue

            context = {
                'uuid': uuid,
                'member': member,
            }
            content = get_template('active_member_mail.txt').render(Context(context))

            print(member.email)

            email = EmailMessage('Deine Mitgliedsdaten',
                                 content,
                                 'vorstand@shackspace.de',
                                 [member.email])
            email.send()
