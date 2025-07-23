"""
mainRSSRunner.py

This module provides functionality to run RSS event collection tasks and save the results to a CSV file.
It loads environment variables (RSS Feed URLS), determines the task type (from ENV variables), fetches event data from an RSS feed, and writes
the collected items to a CSV file.

Functions:
    run_events_RSS(url): Fetches event data from the provided RSS URL using the getEvents function.

Usage:
    Run this module as a script. It expects the following environment variables:
        - TASK_TYPE: Specifies the type of task to run (currently only "EVENTS" is supported).
        - EVENTS_RSS_URL: The URL of the RSS feed to fetch events from.

Raises:
    ValueError: If required environment variables are not set or if an unsupported TASK_TYPE is provided.

"""

import os

from dotenv import load_dotenv

from .csv_updater import items_to_csv
from .events import getEvents


def run_get_events(url, subType):
    if not url:
        raise ValueError(f"{subType}_RSS variable not set")
    data = getEvents(url, subType)
    return data


if __name__ == "__main__":
    load_dotenv()

    task_type = os.getenv("TASK_TYPE")
    if not task_type:
        raise ValueError("TASK_TYPE variable not set")

    if task_type == "INFO-SESSION":
        url = os.getenv("INFO_SESSION_RSS")
        data = run_get_events(url, task_type)
    elif task_type == "WORKSHOP":
        url = os.getenv("WORKSHOP_RSS")
        data = run_get_events(url, task_type)
    elif task_type == "SPEAKER-PANEL":
        url = os.getenv("SPEAKER-PANEL-RSS")
        data = run_get_events(url, task_type)
    else:
        raise ValueError(f"Unsupported TASK_TYPE: {task_type}")
    items_to_csv(data, "data_collections/runningCSV.csv")
