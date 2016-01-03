# coding=utf-8
from django.core.management import BaseCommand


class Command(BaseCommand):

    help = "Import keyholder from csv."

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        from usermanagement.utils import update_keymember
        with open(options['filename']) as fp:
            for line in fp.readlines():
                member_id, ssh_key = line.strip().split(',')
                update_keymember(member_id, ssh_key)
