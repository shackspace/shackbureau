# coding=utf-8
from django.core.mail import EmailMessage
from django.core.management import BaseCommand
from django.db import transaction
from django.template import Context
from django.template.loader import get_template

from usermanagement.utils import get_shackbureau_user


class Command(BaseCommand):

    help = "Sends an email to all active members"

    def handle(self, *args, **options):
        from usermanagement.models import Member, MemberTrackingCode
        for member in Member.objects.filter(is_active=True):
            if not member.email:
                continue

            with transaction.atomic():
                uuid, created = MemberTrackingCode.objects.get_or_create(member=member,
                                                                         created_by=get_shackbureau_user())
                if uuid.validated:
                    continue

                # only send mail, when created
                # if not created:
                    # continue

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
