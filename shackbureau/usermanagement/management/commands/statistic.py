# coding=utf-8
from django.core.management import BaseCommand


class Command(BaseCommand):

    help = "Some statistic."

    # def add_arguments(self, parser):
    #     parser.add_argument('year', type=int)
    #     parser.add_argument('month', type=int)

    def handle(self, *args, **options):
        from usermanagement.utils import member_statistic

        # statistic = member_statistic(year=options['year'])
        statistic = member_statistic()

        statistic = [stat._replace(date=stat.date.isoformat()) for stat in statistic]

        for stat in statistic:
            # stat = stat._asdict()
            print(";".join([stat.date,
                            str(stat.members),
                            str(stat.full),
                            str(stat.reduced),
                            str(stat.sum),
                            ]))
        import json

        statistic = [stat._asdict() for stat in statistic]
        print(json.dumps(statistic, indent=2, sort_keys=True))
