from parser import parse_chat

from analysis import group_overview

from activity_analysis import most_active_day_hour

from heatmap import (
    activity_heatmap,
    print_text_heatmap
)

from top_words import (
    top_words,
    print_top_words
)

from response_analysis import (
    average_response_time,
    longest_silent_streak,
    print_response_report
)

from archetype import (
    calculate_all_scores,
    normalize_scores,
    assign_archetypes,
    print_archetypes
)


def print_header():

    print("=" * 90)
    print(" " * 24 + "WHATSAPP GROUP ANALYTICS REPORT")
    print("=" * 90)
    print()


def print_footer():

    print()
    print("=" * 90)
    print("END OF REPORT")
    print("=" * 90)


if __name__ == "__main__":

    
    # Parser
    

    messages, parser_summary = parse_chat("hostel_bois.txt")

    print_header()

    
    # Group Overview
    

    group_overview(messages, parser_summary)

    print("\n")

   
    # Maximum Activity
    

    most_active_day_hour(messages)

    print("\n")

   
    # NumPy Heatmap
    

    heatmap, participants = activity_heatmap(messages)

    print_text_heatmap(heatmap, participants)

    print("\n")

    
    # Top Words
    

    top10 = top_words(messages)

    print_top_words(top10)

    print("\n")

    
    # Silent StreKS and Response Times
    

    average_times = average_response_time(messages)

    silent_streaks = longest_silent_streak(messages)

    print_response_report(
        average_times,
        silent_streaks
    )

    print("\n")

    
    # Personality Archetypes
    

    raw_scores = calculate_all_scores(messages)

    normalized_scores = normalize_scores(raw_scores)

    assignments = assign_archetypes(normalized_scores)

    print_archetypes(
        assignments,
        raw_scores
    )

    print_footer()