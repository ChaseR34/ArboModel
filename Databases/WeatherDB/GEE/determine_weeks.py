from datetime import date, datetime, timedelta

def get_week_start_end(date_str: str) -> list:
    weeks = list()

    stop_date = datetime.today()

    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    start_of_week = date_obj - timedelta(days=date_obj.weekday())

    while start_of_week < stop_date:
        end_of_week = start_of_week + timedelta(days=6)

        weeks.append((start_of_week.strftime("%Y-%m-%d"), end_of_week.strftime("%Y-%m-%d")))

        start_of_week = end_of_week + timedelta(days=1)
    return weeks

if __name__ == '__main__':
    weeks = get_week_start_end("2021-01-01")

    for a, b in weeks:
        print(a, b)