from datetime import datetime, timedelta

from parser import parse_chat


def average_response_time(messages):

    response_times = {}

    for message in messages:

        sender = message["sender"]

        if sender not in response_times:

            response_times[sender] = []

    for i in range(len(messages) - 1):

        first = messages[i]

        second = messages[i + 1]

        if first["sender"] == second["sender"]:

            continue

        first_time = datetime.strptime(
            first["timestamp"],
            "%d/%m/%y, %H:%M"
        )

        second_time = datetime.strptime(
            second["timestamp"],
            "%d/%m/%y, %H:%M"
        )

        gap = (second_time - first_time).total_seconds()

        response_times[second["sender"]].append(gap)

    average_times = {}

    for sender in response_times:

        gaps = response_times[sender]

        if len(gaps) == 0:

            average_times[sender] = None

        else:

            average_times[sender] = sum(gaps) / len(gaps)

    return average_times


def longest_silent_streak(messages):

    participants = set()

    active_days = {}

    first_date = datetime.strptime(
        messages[0]["date"],
        "%d/%m/%y"
    ).date()

    last_date = datetime.strptime(
        messages[-1]["date"],
        "%d/%m/%y"
    ).date()

    for message in messages:

        sender = message["sender"]

        participants.add(sender)

        if sender not in active_days:

            active_days[sender] = set()

        current_date = datetime.strptime(
            message["date"],
            "%d/%m/%y"
        ).date()

        active_days[sender].add(current_date)

    silent_streaks = {}

    for sender in participants:

        current_day = first_date

        current_streak = 0

        longest_streak = 0

        streak_start = None

        longest_start = None

        longest_end = None

        while current_day <= last_date:

            if current_day not in active_days[sender]:

                if current_streak == 0:

                    streak_start = current_day

                current_streak += 1

            else:

                if current_streak > longest_streak:

                    longest_streak = current_streak

                    longest_start = streak_start

                    longest_end = current_day - timedelta(days=1)

                current_streak = 0

            current_day += timedelta(days=1)

        if current_streak > longest_streak:

            longest_streak = current_streak

            longest_start = streak_start

            longest_end = last_date

        silent_streaks[sender] = (

            longest_streak,
            longest_start,
            longest_end

        )

    return silent_streaks


def format_time(seconds):

    if seconds is None:

        return "No replies"

    minutes = seconds / 60

    if minutes < 60:

        return f"{minutes:.1f} minutes"

    hours = minutes / 60

    return f"{hours:.1f} hours"


def print_response_report(average_times, silent_streaks):

    print()

    print("=" * 70)

    print("RESPONSE PATTERNS")

    print("=" * 70)

    print()

    valid = {

        person: average_times[person]

        for person in average_times

        if average_times[person] is not None

    }

    fastest = min(valid.items(), key=lambda item: item[1])[0]

    slowest = max(valid.items(), key=lambda item: item[1])[0]


    print(

        f"Fastest Replier : "

        f"{fastest} "

        f"({format_time(valid[fastest])})"

    )

    print(

        f"Slowest Replier : "

        f"{slowest} "

        f"({format_time(valid[slowest])})"

    )

    print()

    print("LONGEST SILENT STREAKS")

    print()

    ordered = sorted(

        silent_streaks.items(),

        key=lambda x: x[1][0],

        reverse=True

    )

    for sender, streak in ordered:

        days = streak[0]

        start = streak[1]

        end = streak[2]

        if days == 0:

            print(f"{sender:<12}: 0 days")

        elif days == 1:

            print(

                f"{sender:<12}: "

                f"1 day "

                f"({start.strftime('%d %b %Y')})"

            )

        else:

            print(

                f"{sender:<12}: "

                f"{days} days "

                f"({start.strftime('%d %b %Y')} "

                f"to "

                f"{end.strftime('%d %b %Y')})"

            )


if __name__ == "__main__":

    messages, parser_summary = parse_chat("hostel_bois.txt")

    average_times = average_response_time(messages)

    silent_streaks = longest_silent_streak(messages)

    print_response_report(

        average_times,

        silent_streaks

    )