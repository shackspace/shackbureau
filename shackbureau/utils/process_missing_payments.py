import csv
import sys


def print_help():
    print('Failed to open the csv or template file.')
    print('Usage: print_missing_payments.py <path/to/export.csv> <path/to/mail_template>')


def print_member(member):
    flag = f' – ausgetreten am {member["leave_date"]}' if not member['is_active'] else ''
    if member['nickname']:
        print(f'{member["name"]} ({member["nickname"]}){flag}')
    else:
        print(f'{member["name"]} {flag}')
    print(f'Schuldet {member["accumulated_balance"]} €, davon {member["balance"]} € von {member["year"]}')
    print(f'Letzte Zahlungen: http://localhost:8000/admin/usermanagement/accounttransaction/?booking_type__exact=deposit&q={member["name"].replace(" ", "+")}')
    print(f'Balances: http://localhost:8000/admin/usermanagement/balance/?q={member["name"].replace(" ", "+")}')
    print()


def write_dict(data, fieldnames):
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    for element in data:
        writer.writerow(element)


def main():
    template_path = sys.argv[-1]
    csv_path = sys.argv[-2]

    try:
        with open(template_path, 'r') as template_file:
            template_text = template_file.read()
        with open(csv_path) as csv_file:
            reader = csv.DictReader(csv_file)
            members = [m for m in reader]
            for member in members:
                print_member(member)
                action = input('(m)ail, (s)kip, (d)elete from list, (w)rite list and quit, (q)uit: ')

                if action == 'q':
                    return
                elif action == 'w':
                    write_dict(members, reader.fieldnames)
                    return
                elif action == 'd':
                    del(member)
                elif action == 's':
                    continue
                elif action == 'm':
                    print(template_text.replace('{{ member_id }}', member['member_id']).replace('{{ amount }}', member['accumulated_balance']).replace('{{ email }}', member['email']))

                    delete = input('Delete this user from list? (y/n) ')
                    if delete == 'y':
                        del(member)

    except Exception as e:
        print(e)
        print_help()
        return


if __name__ == '__main__':
    main()
