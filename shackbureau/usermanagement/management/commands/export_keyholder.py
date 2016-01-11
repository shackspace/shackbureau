# coding=utf-8
from django.core.management import BaseCommand
from django.template import Context
from django.template.loader import get_template


class Command(BaseCommand):

    help = "Import keyholder from csv."

    def handle(self, *args, **options):
        from usermanagement.models import Member

        members = Member.objects.filter(memberspecials__is_keyholder=True)\
            .filter(is_active=True).order_by("member_id")

        for task in ["open", "close"]:
            context = {
                'task': task,
                'members': members,
            }
            content = get_template('portal_authorized_keys.txt')\
                .render(Context(context))

            with open("/tmp/authorized_keys." + task) as f:
                f.write(content)
