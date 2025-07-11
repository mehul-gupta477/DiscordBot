"""Referenced from bot.py and filters and returns
jobs that match the inputted criteria.
"""
from typing import list, dict, Any
from data_collections.csv_updater import extract_entries_from_csv  # pylint: disable=E0401

def paste_jobs_command(command_args: str) -> str:
    """
    Parses the jobs command arguments to extract search filters 
        from flag notation

    Args:
        command_args (str): The arguments string with format options:
                           Flag notation: "[flags] [search terms]"
                           Examples: "software -c google -l remote"
                                   "-c microsoft internship"
                                   "python -t internship -s summer"
    Returns:
        str: string containing parsed parameters
    """
    pasted_params = ""
    if not command_args.strip():
        return pasted_params
    current_input = command_args.split()
    for term in current_input:
        if term.startswith("-"):
            pass
        else:
            pasted_params += term + " "
    return pasted_params.strip()

def filter_jobs(all_jobs: list[dict[str, Any]],
                    current_filters: str) -> list[dict[str, Any]]:
    """
    Filters jobs based on provided criteria including general search and specific flags.

    Args:
        jobs (list): List of job dictionaries
        filters (dict): Dictionary of filter criteria

    Returns:
        list: Filtered list of jobs
    """
    if not current_filters:
        return all_jobs
    filtered_jobs = []
    for current_job in all_jobs:
        include_job = False
        search_terms = current_filters.split()
        searchable_fields = [
                current_job.get("Title", ""),
                current_job.get("Company", ""),
                current_job.get("Description", ""),
                current_job.get("Company", ""),
                current_job.get("Location", ""),
                current_job.get("whenDate", ""),
                current_job.get("pubDate", ""),
            ]
        for each_term in search_terms:
            for each_field in searchable_fields:
                if each_term.lower() in each_field.lower():
                    include_job = True
        if include_job:
            filtered_jobs.append(current_job)
        else:
            continue
    return filtered_jobs

def format_jobs_message(returned_jobs: list[dict[str, Any]],
                            current_filters: str) -> str:
    """
    Formats job results into a Discord message.

    Args:
        jobs (list): List of job dictionaries
        filters (dict, optional): Applied filters for context

    Returns:
        str: Formatted message string
    """
    if not returned_jobs:
        return "💼 No jobs found matching your criteria."
    filter_text = f" (Filters: {current_filters.strip()})" if current_filters else ""
    message = f"💼 **Found {len(returned_jobs)} job(s):{filter_text}**\n\n"
    display_jobs = returned_jobs[:10]
    running_count = 0
    for current_job in display_jobs:
        if running_count > 10:
            break
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
        running_count += 1
    if len(returned_jobs) > 10:
        message += f"... and {len(returned_jobs) - 10} more jobs. Use more specific filters to narrow results." # noqa: E501
    return message

def get_jobs(csv_file_path: str) -> list[dict[str, Any]]:
    """
    Reads job data from CSV file and filters based on command parameters.

    Args:
        csv_file_path (str): Path to the CSV file containing job data
        command_args (str): Command arguments for filtering 
                                (e.g., "software -c google -l remote") 

    Returns:
        list: List of job dictionaries matching the criteria
    """
    try:
        jobs = extract_entries_from_csv(csv_file_path)
    except RuntimeError:
        print("Error loading or filtering jobs from CSV")
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
            else:
                continue
    return filtered_jobs
