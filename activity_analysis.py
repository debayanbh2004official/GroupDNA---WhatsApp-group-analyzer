from datetime import datetime

from parser import parse_chat


def format_date(date_string):

    date = datetime.strptime(date_string, "%d/%m/%y")

    return date.strftime("%d %B %Y")


def most_active_day_hour(messages):

    if len(messages) == 0:

        print("No messages found.")

        return

    day_count = {}

    hour_count = {}

    unique_days = set()

    for message in messages:

        date = message["date"]
        time = message["time"]

        unique_days.add(date)

        if date in day_count:

            day_count[date] += 1

        else:

            day_count[date] = 1

        if time != "":

            hour = time.split(":")[0]

            if hour in hour_count:

                hour_count[hour] += 1

            else:

                hour_count[hour] = 1

    if len(day_count) == 0:

        print("No valid dates found.")

        return

    if len(hour_count) == 0:

        print("No valid timestamps found.")

        return

    busiest_day = max(day_count, key=lambda day: day_count[day])

    busiest_day_messages = day_count[busiest_day]

    busiest_hour = max(hour_count, key=lambda hour: hour_count[hour])

    busiest_hour_messages = hour_count[busiest_hour]

    total_days = len(unique_days)

    average_messages = busiest_hour_messages / total_days

    print("=" * 60)
    print("                  MOST ACTIVE DAY AND HOUR")
    print("=" * 60)
    print()

    print(
        f"Busiest Day  : {format_date(busiest_day)} "
        f"({busiest_day_messages} messages)"
    )

    print(
        f"Busiest Hour : "
        f"{busiest_hour}:00 - "
        f"{int(busiest_hour) + 1:02d}:00 "
        f"(avg {average_messages:.1f} messages per day)"
    )


if __name__ == "__main__":

    messages, parser_summary = parse_chat("hostel_bois.txt")

    most_active_day_hour(messages)