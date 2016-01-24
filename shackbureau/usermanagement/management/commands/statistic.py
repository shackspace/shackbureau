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
        # import json
        import decimal

        def decimal_default(obj):
            if isinstance(obj, decimal.Decimal):
                return float(obj)
            raise TypeError

        statistic_json = []
        for stat in statistic:
            fees = dict((str(key), value) for (key, value) in stat.fees.items())
            stat_dict = stat._asdict()
            stat_dict["fees"] = fees
            statistic_json.append(stat_dict)
        print(json.dumps(statistic_json, indent=2, sort_keys=True, skipkeys=True, default=decimal_default))
