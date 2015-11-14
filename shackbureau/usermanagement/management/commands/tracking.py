# coding=utf-8
from django.core.management import BaseCommand


class Command(BaseCommand):

    help = "Imports the tracking file."

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        from usermanagement.models import MemberTrackingCode
        with open(options['filename']) as fp:
            for line in fp.readlines():
                dt, uuid_str = line.strip().split(',')
                try:
                    mtc = MemberTrackingCode.objects.filter(uuid=uuid_str).first()
                    if mtc:
                        mtc.validated = True
                        mtc.save()
                    else:
                        print("Not found: {}".format(uuid_str))
                except ValueError:
                    print("Error: invalid uuid: {}".format(uuid_str))
