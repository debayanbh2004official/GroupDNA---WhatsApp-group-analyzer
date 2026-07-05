from parser import parse_chat
from heatmap import activity_heatmap
from response_analysis import longest_silent_streak

from datetime import datetime

CARE_KEYWORDS = {

    "okay", "ok", "safe", "eat", "sleep",
    "take care", "please", "reminder",
    "drink water", "don't forget", "are you"

}

COMEDY_KEYWORDS = {

    "lol", "lmao", "haha", "rofl", "lmfao"

}

PROBLEM_SOLVER_KEYWORDS = {

    "try", "use", "install", "check",
    "restart", "update", "fix",
    "because", "instead", "replace",
    "change", "configure", "error",
    "issue", "solution", "problem",
    "debug"

}


def clean_words(text):

    punctuation = ".,!?;:'\"()[]{}<>-_/@#$%^&*=+`~|\\"

    words = []

    for word in text.lower().split():

        word = word.strip(punctuation)

        if word != "":

            words.append(word)

    return words


def initialise_scores(messages):

    scores = {}

    for message in messages:

        sender = message["sender"]

        if sender not in scores:

            scores[sender] = {}

    return scores




def detect_spammer(messages):

    spammer_scores = {}

    current_sender = messages[0]["sender"]

    current_burst = 1

    for message in messages:

        sender = message["sender"]

        if sender not in spammer_scores:

            spammer_scores[sender] = []

    for i in range(1, len(messages)):

        sender = messages[i]["sender"]

        previous_sender = messages[i - 1]["sender"]

        if sender == previous_sender:

            current_burst += 1

        else:

            spammer_scores[previous_sender].append(current_burst)

            current_burst = 1

    spammer_scores[messages[-1]["sender"]].append(current_burst)

    average_burst = {}

    for sender in spammer_scores:

        bursts = spammer_scores[sender]

        if len(bursts) == 0:

            average_burst[sender] = 0

        else:

            average_burst[sender] = sum(bursts) / len(bursts)

    return average_burst


def detect_group_mom(messages):

    caring_scores = {}

    total_messages = {}

    for message in messages:

        sender = message["sender"]

        if sender not in caring_scores:

            caring_scores[sender] = 0

            total_messages[sender] = 0

        total_messages[sender] += 1

        text = message["message"].lower()

        for keyword in CARE_KEYWORDS:

            if keyword in text:

                caring_scores[sender] += 1

                break

    percentages = {}

    for sender in caring_scores:

        if total_messages[sender] == 0:

            percentages[sender] = 0

        else:

            percentages[sender] = (

                caring_scores[sender]
                / total_messages[sender]

            ) * 100

    return percentages



def detect_night_owl(messages):

    night_messages = {}

    total_messages = {}

    for message in messages:

        sender = message["sender"]

        if sender not in night_messages:

            night_messages[sender] = 0

            total_messages[sender] = 0

        total_messages[sender] += 1

        if message["time"] == "":

            continue

        hour = int(message["time"].split(":")[0])

        if hour >= 23 or hour <= 4:

            night_messages[sender] += 1

    percentages = {}

    for sender in total_messages:

        if total_messages[sender] == 0:

            percentages[sender] = 0

        else:

            percentages[sender] = (

                night_messages[sender]

                / total_messages[sender]

            ) * 100

    return percentages


def detect_storyteller(messages):

    total_words = {}

    total_messages = {}

    for message in messages:

        sender = message["sender"]

        if sender not in total_words:

            total_words[sender] = 0

            total_messages[sender] = 0

        words = clean_words(message["message"])

        total_words[sender] += len(words)

        total_messages[sender] += 1

    average_words = {}

    for sender in total_words:

        if total_messages[sender] == 0:

            average_words[sender] = 0

        else:

            average_words[sender] = (

                total_words[sender]

                / total_messages[sender]

            )

    return average_words


def detect_drama_queen(messages):

    dramatic_messages = {}

    total_messages = {}

    for message in messages:

        sender = message["sender"]

        if sender not in dramatic_messages:

            dramatic_messages[sender] = 0

            total_messages[sender] = 0

        total_messages[sender] += 1

        text = message["message"]

        dramatic = False

        if len(text.strip()) >= 3:

            letters = ""

            for character in text:

                if character.isalpha():

                    letters += character

            if len(letters) > 0 and letters == letters.upper():

                dramatic = True

        if text.count("!") >= 2:

            dramatic = True

        if dramatic:

            dramatic_messages[sender] += 1

    percentages = {}

    for sender in dramatic_messages:

        if total_messages[sender] == 0:

            percentages[sender] = 0

        else:

            percentages[sender] = (

                dramatic_messages[sender]

                / total_messages[sender]

            ) * 100

    return percentages


def detect_ghost(messages):

    first_date = datetime.strptime(

        messages[0]["date"],

        "%d/%m/%y"

    ).date()

    last_date = datetime.strptime(

        messages[-1]["date"],

        "%d/%m/%y"

    ).date()

    total_days = (

        last_date - first_date

    ).days + 1

    silent_streaks = longest_silent_streak(messages)

    ghost_scores = {}

    for sender in silent_streaks:

        longest_streak = silent_streaks[sender][0]

        ghost_scores[sender] = (

            longest_streak

            / total_days

        ) * 100

    return ghost_scores



def detect_comedian(messages):

    comedy_scores = {}

    total_messages = {}

    for message in messages:

        sender = message["sender"]

        if sender not in comedy_scores:

            comedy_scores[sender] = 0

            total_messages[sender] = 0

        total_messages[sender] += 1

        words = clean_words(message["message"])

        for word in words:

            if word in COMEDY_KEYWORDS:

                comedy_scores[sender] += 1

                break

    percentages = {}

    for sender in comedy_scores:

        if total_messages[sender] == 0:

            percentages[sender] = 0

        else:

            percentages[sender] = (

                comedy_scores[sender]

                / total_messages[sender]

            ) * 100

    return percentages


def detect_question_master(messages):

    question_scores = {}

    total_messages = {}

    for message in messages:

        sender = message["sender"]

        if sender not in question_scores:

            question_scores[sender] = 0

            total_messages[sender] = 0

        total_messages[sender] += 1

        if message["message"].strip().endswith("?"):

            question_scores[sender] += 1

    percentages = {}

    for sender in question_scores:

        if total_messages[sender] == 0:

            percentages[sender] = 0

        else:

            percentages[sender] = (

                question_scores[sender]

                / total_messages[sender]

            ) * 100

    return percentages


def detect_problem_solver(messages):

    solver_scores = {}

    total_messages = {}

    for message in messages:

        sender = message["sender"]

        if sender not in solver_scores:

            solver_scores[sender] = 0

            total_messages[sender] = 0

        total_messages[sender] += 1

        words = clean_words(message["message"])

        for word in words:

            if word in PROBLEM_SOLVER_KEYWORDS:

                solver_scores[sender] += 1

                break

    percentages = {}

    for sender in solver_scores:

        if total_messages[sender] == 0:

            percentages[sender] = 0

        else:

            percentages[sender] = (

                solver_scores[sender]

                / total_messages[sender]

            ) * 100

    return percentages


def normalize_scores(archetype_scores):

    normalized_scores = {}

    for archetype in archetype_scores:

        normalized_scores[archetype] = {}

        maximum = max(archetype_scores[archetype].values())

        if maximum == 0:

            maximum = 1

        for sender in archetype_scores[archetype]:

            normalized_scores[archetype][sender] = (

                archetype_scores[archetype][sender]

                / maximum

            )

    return normalized_scores


def calculate_all_scores(messages):

    scores = {}

    scores["THE SPAMMER"] = detect_spammer(messages)

    scores["THE GROUP MOM"] = detect_group_mom(messages)

    scores["THE NIGHT OWL"] = detect_night_owl(messages)

    scores["THE STORYTELLER"] = detect_storyteller(messages)

    scores["THE DRAMA QUEEN"] = detect_drama_queen(messages)

    scores["THE GHOST"] = detect_ghost(messages)

    scores["THE COMEDIAN"] = detect_comedian(messages)

    scores["THE QUESTION MASTER"] = detect_question_master(messages)

    scores["THE PROBLEM SOLVER"] = detect_problem_solver(messages)

    return scores


'''def print_archetypes(assignments, raw_scores):

    print()

    print("=" * 70)

    print("PERSONALITY ARCHETYPES")

    print("=" * 70)

    print()

    ordered = sorted(assignments.items())

    for sender, archetype in ordered:

        value = raw_scores[archetype][sender]

        if archetype == "THE SPAMMER":

            metric = f"avg {value:.1f} msgs in a row"

        elif archetype == "THE GROUP MOM":

            metric = f"{value:.1f}% caring messages"

        elif archetype == "THE NIGHT OWL":

            metric = f"{value:.1f}% msgs after 11 PM"

        elif archetype == "THE STORYTELLER":

            metric = f"avg {value:.1f} words/msg"

        elif archetype == "THE DRAMA QUEEN":

            metric = f"{value:.1f}% dramatic msgs"

        elif archetype == "THE GHOST":

            metric = f"{value:.1f}% silent days"

        elif archetype == "THE COMEDIAN":

            metric = f"{value:.1f}% funny msgs"

        elif archetype == "THE QUESTION MASTER":

            metric = f"{value:.1f}% questions"

        elif archetype == "THE PROBLEM SOLVER":

            metric = f"{value:.1f}% solution msgs"

        else:

            metric = f"{value:.2f}"

        print(

            f"{sender:<10}"

            f"\u2192 "

            f"{archetype:<22}"

            f"({metric})"

        )
'''
def assign_archetypes(normalized_scores):

    participants = list(

        next(iter(normalized_scores.values())).keys()

    )

    preferences = {}

    for sender in participants:

        ranking = []

        for archetype in normalized_scores:

            score = normalized_scores[archetype][sender]

            ranking.append((archetype, score))

        ranking.sort(

            key=lambda item: item[1],

            reverse=True

        )

        preferences[sender] = ranking

    assignments = {}

    assigned_people = set()

    changed = True

    while changed:

        changed = False

        claims = {}

        for sender in participants:

            if sender in assigned_people:

                continue

            while len(preferences[sender]) > 0:

                archetype, score = preferences[sender][0]

                if archetype not in claims:

                    claims[archetype] = []

                claims[archetype].append(

                    (sender, score)

                )

                break

        for archetype in claims:

            candidates = claims[archetype]

            candidates.sort(

                key=lambda item: item[1],

                reverse=True

            )

            winner = candidates[0][0]

            assignments[winner] = archetype

            assigned_people.add(winner)

            changed = True

            for loser, score in candidates[1:]:

                preferences[loser].pop(0)

    return assignments


def print_archetypes(assignments, raw_scores):

    print()

    print("=" * 70)

    print("PERSONALITY ARCHETYPES")

    print("=" * 70)

    print()

    ordered = sorted(assignments.items())

    for sender, archetype in ordered:

        value = raw_scores[archetype][sender]

        if archetype == "THE SPAMMER":

            metric = f"avg {value:.1f} msgs in a row"

        elif archetype == "THE GROUP MOM":

            metric = f"{value:.1f}% caring messages"

        elif archetype == "THE NIGHT OWL":

            metric = f"{value:.1f}% msgs after 11 PM"

        elif archetype == "THE STORYTELLER":

            metric = f"avg {value:.1f} words/msg"

        elif archetype == "THE DRAMA QUEEN":

            metric = f"{value:.1f}% dramatic messages"

        elif archetype == "THE GHOST":

            metric = f"{value:.1f}% silent days"

        elif archetype == "THE COMEDIAN":

            metric = f"{value:.1f}% funny messages"

        elif archetype == "THE QUESTION MASTER":

            metric = f"{value:.1f}% questions"

        elif archetype == "THE PROBLEM SOLVER":

            metric = f"{value:.1f}% problem-solving messages"

        else:

            metric = f"{value:.2f}"

        print(f"{sender} \u2192 {archetype}    ({metric})")

if __name__ == "__main__":

    messages, parser_summary = parse_chat("hostel_bois.txt")

    raw_scores = calculate_all_scores(messages)

    normalized_scores = normalize_scores(raw_scores)

    assignments = assign_archetypes(normalized_scores)

    print_archetypes(assignments, raw_scores)