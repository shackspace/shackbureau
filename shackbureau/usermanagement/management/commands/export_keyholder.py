# coding=utf-8
from django.db.models import Q
from django.conf import settings
from django.core.management import BaseCommand
from django.template.loader import get_template
from django.utils import timezone

from os import path


class Command(BaseCommand):

    help = "Import keyholder from csv."

    def handle(self, *args, **options):
        from usermanagement.models import Member

        members = Member.objects.filter(memberspecials__is_keyholder=True) \
                                .filter(Q(is_active=True) | Q(leave_date__gt=timezone.now()))\
                                .order_by("member_id")

        for task in ["open", "close"]:
            context = {
                'task': task,
                'members': members,
            }
            content = get_template('portal_authorized_keys.txt')\
                .render(context)

            with open(path.join(settings.EXPORT_ROOT, "authorized_keys." +
                                task), 'w') as f:
                f.write(content)
