""""""

import os

from dotenv import load_dotenv

from .csv_updater import items_to_csv
from .events import getEvents
from .internships import getInternships
from .jobs import getJobs


def run_events_RSS(url):
    if not url:
        raise ValueError("EVENTS_RSS_URL variable not set")
    data = getEvents(url)
    return data


def run_jobs_RSS(url):
    if not url:
        raise ValueError("JOBS_RSS variable not set")
    data = getJobs(url)
    return data


def run_internships_RSS(url):
    if not url:
        raise ValueError("INTERNSHIPS_RSS variable not set")
    data = getInternships(url)
    return data


if __name__ == "__main__":
    load_dotenv()

    task_type = os.getenv("TASK_TYPE")
    if not task_type:
        raise ValueError("TASK_TYPE variable not set")

    if task_type == "EVENTS":
        url = os.getenv("EVENTS_RSS_URL")
        data = run_events_RSS(url)
    elif task_type == "JOBS":
        url = os.getenv("JOBS_RSS")
        data = run_jobs_RSS(url)
    elif task_type == "INTERNSHIPS":
        url = os.getenv("INTERNSHIPS_RSS")
        data = run_internships_RSS(url)
    else:
        raise ValueError(f"Unsupported TASK_TYPE: {task_type}")
    items_to_csv(data, "data_collections/runningCSV.csv")
