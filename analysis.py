from datetime import datetime

from parser import parse_chat


def format_date(date_string):

    date = datetime.strptime(date_string, "%d/%m/%y")

    return date.strftime("%d %B %Y")


def group_overview(messages, parser_summary):

    total_messages = parser_summary["total_messages"]

    participant_count = parser_summary["participant_count"]

    first_date = messages[0]["date"]

    last_date = messages[-1]["date"]

    first_date_object = datetime.strptime(first_date, "%d/%m/%y")

    last_date_object = datetime.strptime(last_date, "%d/%m/%y")

    total_days = (last_date_object - first_date_object).days + 1

    message_count = {}

    for message in messages:

        sender = message["sender"]

        if sender in message_count:

            message_count[sender] += 1

        else:

            message_count[sender] = 1

    sorted_people = sorted(

        message_count.items(),

        key=lambda person: person[1],

        reverse=True

    )

    print("=" * 60)
    print("GROUP OVERVIEW")
    print("=" * 60)

    print(f"Group            : Hostel Bois 4ever")

    print(
        f"Period           : {format_date(first_date)} to "
        f"{format_date(last_date)} ({total_days} days)"
    )

    print(f"Total Messages   : {total_messages}")

    print(f"Participants     : {participant_count}")

    print()

    print("MESSAGES PER PERSON")

    print()

    for sender, count in sorted_people:

        percentage = (count / total_messages) * 100

        print(f"{sender:<20} : {count:>5} ({percentage:5.1f}%)")


if __name__ == "__main__":

    messages, parser_summary = parse_chat("hostel_bois.txt")

    group_overview(messages, parser_summary)