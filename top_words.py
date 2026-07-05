from parser import parse_chat


def top_words(messages):

    stop_words = {

        "i", "is", "the", "a", "an", "and", "or", "to", "of", "in",
        "on", "for", "at", "it", "this", "that", "was", "are", "am",
        "be", "been", "were", "you", "your", "me", "my", "we", "our",
        "us", "he", "she", "they", "them", "their", "as", "with",
        "from", "by", "if", "but", "so", "do", "did", "does", "have",
        "has", "had", "will", "would", "can", "could", "shall", "should"

    }

    punctuation = ".,!?;:'\"()[]{}<>-_/@#$%^&*=+`~|\\"

    word_count = {}

    for message in messages:

        if message["type"] == "deleted":

            continue

        if message["type"] == "media_only":

            continue

        text = message["message"].lower()

        words = text.split()

        for word in words:

            word = word.strip(punctuation)

            if word == "":

                continue

            if word in stop_words:

                continue

            if word not in word_count:

                word_count[word] = 1

            else:

                word_count[word] += 1

    sorted_words = sorted(

        word_count.items(),
        key=lambda item: item[1],
        reverse=True

    )

    return sorted_words[:10]


def print_top_words(top10):

    print()
    print("=" * 80)
    print("GROUPS FAVOURITE WORDS")
    print("=" * 80)
    print()

    maximum = top10[0][1]

    for word, count in top10:

        bar_length = int((count / maximum) * 30)

        bar = "\u2588" * bar_length
        
        print(f"{word:<20} {count:>5}  {bar}")
        print()



if __name__ == "__main__":

    messages, parser_summary = parse_chat("hostel_bois.txt")

    top10 = top_words(messages)

    print_top_words(top10)