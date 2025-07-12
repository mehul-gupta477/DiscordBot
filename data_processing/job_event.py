"""Referenced from bot.py and filters and returns
jobs that match the inputted criteria.
"""

from typing import Any
from data_collections.csv_updater import (
    extract_entries_from_csv,
)


def paste_jobs_command(command_args: str) -> str:
    """
    Parses the jobs command arguments to extract search filters
        from flag notation

    Args:
        command_args (str): The arguments passed to the command,
                                as a string.

    Returns:
        str: string containing parsed parameters
    """
    params = ""
    if not command_args:
        return params
    args = command_args.split()
    for term in args:
        if term.startswith("-"):
            pass
        else:
            params += term + " "
    return params.strip()


def filter_jobs(
    jobs: list[dict[str, Any]], _filters: str
) -> list[dict[str, Any]]:
    """
    Filters jobs based on provided criteria

    Args:
        jobs (list): List of job dictionaries
        filters (dict): Dictionary of filter criteria

    Returns:
        list: Filtered list of jobs
    """
    if not _filters:
        return jobs
    filtered_jobs = []
    for current_job in jobs:
        include_job = False
        search_terms = _filters.split()
        searchable_fields = [
            current_job.get("Title", ""),
            current_job.get("Company", ""),
            current_job.get("Description", ""),
            current_job.get("Location", ""),
            current_job.get("whenDate", ""),
            current_job.get("pubDate", ""),
        ]
        for term in search_terms:
            for field in searchable_fields:
                if term.lower() in field.lower():
                    include_job = True
                    break
        if include_job:
            filtered_jobs.append(current_job)
    return filtered_jobs


def format_jobs_message(
    jobs: list[dict[str, Any]], _filters: str
) -> str:
    """
    Formats job results into a Discord message.

    Args:
        jobs (list): List of job dictionaries
        filters (dict, optional): Applied filters for context

    Returns:
        str: Formatted message string
    """
    if not jobs:
        return "💼 No jobs found matching your criteria."
    filter_text = f" (Filters: {_filters.strip()})" if _filters else ""
    message = f"💼 **Found {len(jobs)} job(s):{filter_text}**\n\n"
    limitted_jobs = jobs[:10]
    for current_job in limitted_jobs:
        title = current_job.get("Title", "Untitled Position")
        job_type = current_job.get("Type", "")
        company_name = current_job.get("Company", "")
        location = current_job.get("Location", "")
        description = current_job.get("Description", "")
        when_date = current_job.get("whenDate", "")
        pub_date = current_job.get("pubDate", "")
        link = current_job.get("link", "")

        job_text = f"**{title}**\n"
        job_text += f"📝 {job_type}\n"
        job_text += f"🏢 {company_name}\n"
        if location:
            job_text += f"📍 {location}\n"
        if when_date:
            job_text += f"📅 Start Date: {when_date}\n"
        if pub_date:
            job_text += f"📅 Posted: {pub_date}\n"
        if description:
            job_text += f"📝 {description}\n"
        if link:
            job_text += f"🔗 [Apply Here]({link})\n"
        message += job_text + "\n"
    if len(jobs) > 10:
        message += f"... and {len(jobs) - 10} more jobs. Use more specific filters to narrow results."  # noqa: E501
    return message


def get_jobs(csv_file_path: str) -> list[dict[str, Any]]:
    """
    Reads job data from CSV file and filters based on command parameters.

    Args:
        csv_file_path (str): Path to the CSV file containing job data

    Returns:
        list: List of job dictionaries matching the criteria
    """
    try:
        jobs = extract_entries_from_csv(csv_file_path)
    except RuntimeError:
        print("Error loading or filtering jobs from CSV")
        raise
    except OSError:
        print("CSV file not found or inaccessible")
        raise
    filtered_jobs = []
    for current_job in jobs:
        job_type = current_job.get("Type", "").lower()
        job_keywords = [
            "job",
            "internship",
            "intern",
        ]
        for specific_keyword in job_keywords:
            if specific_keyword in job_type:
                filtered_jobs.append(current_job)
                break
    return filtered_jobs
