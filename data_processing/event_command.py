"""Referenced from bot.py and filters and returns
events that match the inputted criteria or
returns 5 upcoming events if no criteria is specified.
"""

from typing import Any

from data_processing.get_type_data import (
    get_type_data,
)


def filter_events(events: list[dict[str, Any]], _filters: str) -> list[dict[str, Any]]:
    """
    Filters events based on the provided arguments.

    Args:
        events (list[dict[str, Any]]): List of event dictionaries.
        _filters (str): Filter criteria as a string.

    Returns:
        list[dict[str, Any]]: Filtered list of events.
    """
    if not _filters:
        return events[:5]
    filtered_events = []
    for event in events:
        include_event = False
        confidence = 0
        search_terms = _filters.lower().split()
        searchable_fields = [
            event.get("Title", ""),
            event.get("subType", ""),
            event.get("Company", ""),
            event.get("Description", ""),
            event.get("Location", ""),
            event.get("whenDate", ""),
            event.get("pubDate", ""),
        ]
        for term in search_terms:
            for field in searchable_fields:
                if not field:
                    break
                if term in field.lower():
                    include_event = True
                    confidence += 1
                    break
        if include_event:
            event.update({"confidence": confidence})
            filtered_events.append(event)
    filtered_events.sort(key=lambda x: x["confidence"], reverse=True)
    return filtered_events


def format_event_message(events: list[dict[str, Any]], _filters: str) -> str:
    """
    Formats a message listing the events which follows Discord message
        conventions.

    Args:
        events (list[dict[str, Any]]): List of event dictionaries.
        _filters (str): Filter criteria as a string.

    Returns:
        str: Formatted message with event details.
    """
    if not events:
        return "No events found matching your criteria."
    filter_events = f" (Filters: {_filters.strip()})" if _filters else ""
    message = "**📅 Upcoming Events:**\n"
    limited_events = events[:5]
    for event in limited_events:
        title = event.get("Title", "Unknown Event")
        event_type = event.get("subType", "")
        company = event.get("Company", "")
        location = event.get("Location", "")
        when_date = event.get("whenDate", "")

        if (
            isinstance(location, str)
            and location.startswith("[")
            and location.endswith("]")
        ):
            location = location[1:-1]

        description = event.get("Description", "No description available.")
        round_description = (
            description[:80] + "..." if len(description) > 80 else description
        )
        link = event.get("link", "No link available.")

        event_text = f"**{title}**\n"
        if event_type:
            event_text += f"**Type:** {event_type}\n"
        if company:
            event_text += f"Company: {company}\n"
        if location:
            event_text += f"Location: {location}\n"
        if when_date:
            event_text += f"Date: {when_date}\n"
        event_text += f"Description: {round_description}\n"
        event_text += f"[More Info]({link})\n\n"
        message += event_text
    message += f"Total events found: {len(events)}{filter_events}"
    if len(events) > 5:
        message += "\n\nNote: Only the top 5 events are displayed based on relevance."
    return message


def get_events(csv_file_path: str) -> list[dict[str, Any]]:
    """
    Retrieves events from a CSV file and returns them as a list of dictionaries.

    Args:
        csv_file_path (str): Path to the CSV file containing event data.

    Returns:
        list[dict[str, Any]]: List of event dictionaries.
    """
    return get_type_data(csv_file_path, "Event")
