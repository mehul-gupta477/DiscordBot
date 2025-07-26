""""""

import os

from dotenv import load_dotenv

from .csv_updater import items_to_csv
from .events import getEvents
from .internships import getInternships
from .jobs import getJobs


def run_events_RSS(url, subType):
    if not url:
        raise ValueError(f"{subType}_RSS variable not set")
    data = getEvents(url, subType)
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

    url = None
    if task_type == "INFO_SESSION":
        url = os.getenv("INFO_SESSION_RSS")
        data = run_events_RSS(url, task_type)
    elif task_type == "WORKSHOP":
        url = os.getenv("WORKSHOP_RSS")
        data = run_events_RSS(url, task_type)
    elif task_type == "SPEAKER_PANEL":
        url = os.getenv("SPEAKER_PANEL_RSS")
        data = run_events_RSS(url, task_type)
    elif task_type == "OTHER":
        url = os.getenv("OTHER_RSS")
        data = run_events_RSS(url, task_type)
    elif task_type == "CAREER_FAIR":
        url = os.getenv("CAREER_FAIR")
        data = run_events_RSS(url, task_type)
    elif task_type == "JOBS":
        url = os.getenv("JOBS_RSS")
        data = run_jobs_RSS(url)
    elif task_type == "INTERNSHIPS":
        url = os.getenv("INTERNSHIPS_RSS")
        data = run_internships_RSS(url)
    else:
        raise ValueError(f"Unsupported TASK_TYPE: {task_type}")
    items_to_csv(data, "data_collections/runningCSV.csv")
