# coding=utf-8
from django.core.management import BaseCommand
from django.template import Context
from django.template.loader import get_template
from os import path
from django.conf import settings


class Command(BaseCommand):

    help = "Import keyholder from csv."

    def handle(self, *args, **options):
        from usermanagement.models import Member
        # MemberTrackingCode

        members = Member.objects.filter(membertrackingcode__validated=False)
        context = {'lb': '{',
                   'rb': '}',
                   'members': members}
        content = get_template('bulkmail.txt').render(Context(context))
        # print(content)

        with open(path.join(settings.MEDIA_ROOT, "bulkmail.tex"), 'w') as f:
            f.write(content)
