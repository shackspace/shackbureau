from datetime import timedelta

def last_day_of_month(given_date):
    new_date = given_date.replace(day=28) + timedelta(days=5)
    new_date = new_date.replace(day=1) - timedelta(days=1)
    return new_date
