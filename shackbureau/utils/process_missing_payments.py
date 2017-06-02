import csv
import sys


def print_help():
    print('Failed to open the csv or template file.')
    print('Usage: print_missing_payments.py <path/to/export.csv> <path/to/mail_template>')


def main():
    template_path = sys.argv[-1]
    csv_path = sys.argv[-2]

    try:
        with open(template_path, 'r') as template_file:
            template_text = template_file.read()
        with open(csv_path) as csv_file:
            members = csv.DictReader(csv_file)
    except Exception as e:
        print(e)
        print_help()
        return


if __name__ == '__main__':
    main()
