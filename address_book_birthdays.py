import calendar

from collections import defaultdict
from datetime import datetime, date


def _is_leap_birthday(birthday, current):
    current = current.date()
    calendar.setfirstweekday(calendar.MONDAY)
    is_leap_birthday_year = calendar.isleap(birthday.year)
    is_leap_current_year = calendar.isleap(current.year)
    if (
        is_leap_birthday_year
        and birthday == date(birthday.year, 2, 29)
        and not is_leap_current_year
    ):
        return True
    return False


def _format_greetings(greetings, current):
    formatted_greetings = "People who should be congratulated on their birthday: \n"
    if not greetings:
        return formatted_greetings.replace("\n", "None")
    current_weekday = current.weekday()
    weekdays_order_from_current = [(current_weekday + i) % 7 for i in range(7)]
    for weekday in weekdays_order_from_current:
        if weekday in greetings.keys():
            formatted_greetings += (
                f"{calendar.day_name[weekday]}: {', '.join(greetings[weekday])}\n"
            )
    return formatted_greetings


def get_birthdays_per_week(users):
    greetings = defaultdict(list)
    current = datetime.today()
    current_date = current.date()
    for user in users:
        birthday = datetime.strptime(user["birthday"], "%d.%m.%Y").date()
        if _is_leap_birthday(birthday, current):
            birthday_this_year = birthday.replace(
                year=current_date.year, month=3, day=1
            )
        else:
            birthday_this_year = birthday.replace(year=current_date.year)
        if birthday_this_year < current_date:
            birthday_this_year = birthday_this_year.replace(year=current_date.year + 1)
        delta_days = (birthday_this_year - current_date).days
        if delta_days < 7:
            name = user["name"]
            if birthday_this_year.weekday() in [calendar.SATURDAY, calendar.SUNDAY]:
                valid_saturday = (
                    birthday_this_year.weekday() == calendar.SATURDAY and delta_days < 5
                )
                valid_sunday = (
                    birthday_this_year.weekday() == calendar.SUNDAY and delta_days < 6
                )
                if valid_saturday or valid_sunday:
                    greetings[calendar.MONDAY].append(name)
            else:
                greetings[birthday_this_year.weekday()].append(name)
    return _format_greetings(greetings, current)


if __name__ == "__main__":
    from faker import Faker

    fake = Faker()
    test_data = [
        {"name": fake.name(), "birthday": fake.date_time().strftime("%d.%m.%Y")}
        for _ in range(500)
    ]
    print(get_birthdays_per_week(test_data))
