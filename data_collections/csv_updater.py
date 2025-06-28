from getEvents import getEvents
import os
import pandas as pd
from dotenv import load_dotenv


def items_to_csv(data: list[dict], path_to_file: str):
    """
    Save items to a csv file
    """
    if data:
        try:
            if not os.path.isfile(path_to_file):
                raise ValueError("path_to_csv not found")
            data_frame = pd.DataFrame(data)
            data_frame.to_csv(path_to_file, index=False)
            print(f"Items Successfully saved to {path_to_file}")
        except Exception as e:
            raise RuntimeError(f"Failed to save data to CSV: {e}") from e

if __name__ == "__main__":
    load_dotenv("../.env")
    url = os.getenv("EVENTS_RSS_URL")
    data = getEvents(url)
    items_to_csv(data, "runningCSV.csv")
