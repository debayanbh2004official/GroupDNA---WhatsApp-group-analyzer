import numpy as np

from parser import parse_chat


def activity_heatmap(messages):

    participants = []

    for message in messages:

        sender = message["sender"]

        if sender not in participants:

            participants.append(sender)

    participant_index = {}

    for i in range(len(participants)):

        participant_index[participants[i]] = i

    heatmap = np.zeros((len(participants), 24), dtype=int)

    for message in messages:

        sender = message["sender"]

        time = message["time"]

        if time == "":

            continue

        hour = int(time.split(":")[0])

        row = participant_index[sender]

        heatmap[row][hour] += 1

    return heatmap, participants

def print_ratio_matrix(heatmap, participants):

    print()
    print("=" * 130)
    print("NORMALIZED RATIO MATRIX")
    print("=" * 130)
    print()

    print(f"{'Participant / Time':<20}", end="")

    for hour in range(24):

        print(f"{hour:^7}", end="")

    print()

    print("-" * 190)

    for i in range(len(participants)):

        print(f"{participants[i]:<20}", end="")

        maximum = np.max(heatmap[i])

        if maximum == 0:

            maximum = 1

        for hour in range(24):

            ratio = heatmap[i][hour] / maximum

            print(f"{ratio:^7.2f}", end="")

        print()


def print_numeric_matrix(heatmap, participants):

    print()
    print("=" * 130)
    print("NUMERIC ACTIVITY MATRIX")
    print("=" * 130)
    print()

    print(f"{'Participant / Time':<20}", end="")

    for hour in range(24):

        print(f"{hour:^4}", end="")

    print()

    print("-" * 130)

    for i in range(len(participants)):

        print(f"{participants[i]:<20}", end="")

        for hour in range(24):

            print(f"{heatmap[i][hour]:^4}", end="")

        print()


def print_text_heatmap(heatmap, participants):

    print()
    print("=" * 130)
    print("TEXT ACTIVITY HEATMAP")
    print("=" * 130)
    print()

    print(f"{'Participant / Time':<20}", end="")

    for hour in range(24):

        print(f"{hour:^4}", end="")

    print()

    print("-" * 130)

    for i in range(len(participants)):

        print(f"{participants[i]:<20}", end="")

        maximum = np.max(heatmap[i])

        if maximum == 0:

            maximum = 1

        for hour in range(24):

            value = heatmap[i][hour]

            ratio = value / maximum

            if ratio <= 0.25:

                symbol = "\u00B7"     

            elif ratio <= 0.50:

                symbol = "\u2591"      

            elif ratio <= 0.75:

                symbol = "\u2592"      

            else:

                symbol = "\u2588"      

            print(f"{symbol:^4}", end="")

        print()


if __name__ == "__main__":

    messages, parser_summary = parse_chat("hostel_bois.txt")

    heatmap, participants = activity_heatmap(messages)

    print_numeric_matrix(heatmap, participants)

    print_ratio_matrix(heatmap, participants)

    print_text_heatmap(heatmap, participants)