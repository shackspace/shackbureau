import csv


def import_old_shit(filename):
    with open(filename) as fp:
        reader = csv.reader(fp, delimiter=";", quotechar='"')
        headers = reader.__next__()
        for line in reader:
            print(dict(zip(headers, line)))
