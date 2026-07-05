
def is_new_message(line):

    if len(line) < 8:
        return False

    return (
        line[0].isdigit()
        and line[1].isdigit()
        and line[2] == "/"
        and line[3].isdigit()
        and line[4].isdigit()
        and line[5] == "/"
        and line[6].isdigit()
        and line[7].isdigit()
    )


def is_deleted_message(message):

    return message.strip() == "This message was deleted"


def is_media_message(message):

    return "<Media omitted>" in message


def has_media_caption(message):

    cleaned = message.replace("<Media omitted>", "").strip()

    return len(cleaned) > 0


def parse_chat(filename):

    messages = []

    system_count = 0
    media_count = 0
    deleted_count = 0
    malformed_count = 0

    participants = set()

    current_message = None

    file = open(filename, "r", encoding="utf-8")

    for line in file:

        line = line.rstrip("\n")

        if line.strip() == "":
            continue

        if not is_new_message(line):

            if current_message is not None:
                current_message["message"] += "\n" + line

            continue

        if current_message is not None:
            messages.append(current_message)

        parts = line.split(" - ", 1)

        if len(parts) != 2:

            malformed_count += 1
            current_message = None
            continue

        timestamp = parts[0]
        remaining = parts[1]

        sender_parts = remaining.split(": ", 1)

        if len(sender_parts) != 2:

            system_count += 1
            current_message = None
            continue

        sender = sender_parts[0].strip()
        message = sender_parts[1].strip()

        participants.add(sender)

        message_type = "normal"

        if is_deleted_message(message):

            deleted_count += 1
            message_type = "deleted"

        elif is_media_message(message):

            media_count += 1

            if has_media_caption(message):
                message_type = "media_with_caption"
            else:
                message_type = "media_only"

        date_time = timestamp.split(", ", 1)

        if len(date_time) == 2:
            date = date_time[0]
            time = date_time[1]
        else:
            date = timestamp
            time = ""

        current_message = {

            "timestamp": timestamp,
            "date": date,
            "time": time,
            "sender": sender,
            "message": message,
            "type": message_type

        }

    if current_message is not None:
        messages.append(current_message)

    file.close()

    parser_summary = {

        "total_messages": len(messages),
        "participants": participants,
        "participant_count": len(participants),
        "system_messages": system_count,
        "media_messages": media_count,
        "deleted_messages": deleted_count,
        "malformed_messages": malformed_count

    }

    return messages, parser_summary


if __name__ == "__main__":

    messages, parser_summary = parse_chat("hostel_bois.txt")

    print("-"*3,"| GROUP OVERVIEW |","-"*30)

    print("Successfully Parsed Chat\n")

    print("Total Messages      :", parser_summary["total_messages"])
    print("Participants        :", parser_summary["participant_count"])
    print("System Messages     :", parser_summary["system_messages"])
    print("Media Messages      :", parser_summary["media_messages"])
    print("Deleted Messages    :", parser_summary["deleted_messages"])
    print("Malformed Messages  :", parser_summary["malformed_messages"])

    print("\nFirst Five Parsed Messages:\n")

    for message in messages[:5]:
        print(message)
        print()

    print("\nLast Five Parsed Messages:\n")

    for message in messages[-5:]:
        print(message)
        print()