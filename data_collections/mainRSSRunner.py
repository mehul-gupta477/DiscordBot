""""""
from dotenv import load_dotenv
from getEvents import getEvents
from csv_updater import items_to_csv
import os


def run_events_RSS(url):
    if not url:
        raise ValueError("EVENTS_RSS_URL variable not set")
    data = getEvents(url)
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
        url = os.getenv("JOBS_RSS_URL")
        # Call different method like run_jobs_RSS
    items_to_csv(data, "data_collections/runningCSV.csv")

