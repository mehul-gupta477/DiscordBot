"""Referenced from bot.py and filters and returns
jobs that match the inputted criteria.
"""
from typing import List, Dict, Any
from data_collections.csv_updater import extract_entries_from_csv

def paste_jobs_command(command_args: str) -> Dict[str, Any]:
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
        dict: Dictionary containing parsed parameters
    """
    pasted_params = {
        "role": None,
        "type": None,
        "season": None,
        "company": None,
        "location": None,
        "general_search": None,
    }
    if not command_args.strip():
        return pasted_params
    full_inputs = command_args.split()
    i = 0
    general_search_terms = []
    while i < len(full_inputs):
        current_input = full_inputs[i]
        if current_input.startswith("-"):
            if current_input in ["-r", "--role"]:
                pasted_params["role"] = full_inputs[i + 1]
                i += 2
            elif current_input in ["-t", "--type"]:
                pasted_params["type"] = full_inputs[i + 1]
                i += 2
            elif current_input in ["-s", "--season"]:
                pasted_params["season"] = full_inputs[i + 1]
                i += 2
            elif current_input in ["-c", "--company"]:
                pasted_params["company"] = full_inputs[i + 1]
                i += 2
            elif current_input in ["-l", "--location"]:
                pasted_params["location"] = full_inputs[i + 1]
                i += 2
            else:   # skip unknown flags
                i += 1
        else:
            general_search_terms.append(current_input)      # input is a general search term
            i += 1
    pasted_params["general_search"] = " ".join(general_search_terms)
    return pasted_params

def filter_jobs(all_jobs: List[Dict[str, Any]],
                    filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Filters jobs based on provided criteria including general search and specific flags.

    Args:
        jobs (list): List of job dictionaries
        filters (dict): Dictionary of filter criteria

    Returns:
        list: Filtered list of jobs
    """
    filtered_jobs = []
    for current_job in all_jobs:
        include_job = False
        searchable_fields = [
                current_job.get("Title", ""),
                current_job.get("Company", ""),
                current_job.get("Description", ""),
                current_job.get("Company", ""),
                current_job.get("Location", ""),
                current_job.get("whenDate", ""),
                current_job.get("pubDate", ""),
            ]
        if filters.get("general_search"):
            general_search = filters["general_search"].lower()
            for each_field in searchable_fields:
                if general_search in each_field.lower():
                    include_job = True
                else:
                    continue
        if include_job:
            filtered_jobs.append(current_job)
        else:
            continue
    return filtered_jobs

def format_jobs_message(returned_jobs: List[Dict[str, Any]],
                            filters: Dict[str, Any] = None) -> str:
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
    filter_desc = []
    if filters:
        for key, value in filters.items():
            if key == "general_search":
                filter_desc.append(f"search: {value}")
            else:
                filter_desc.append(f"{key}: {value}")
    filter_text = f" (Filters:{', '.join(filter_desc)})"
    message = f"💼 **Found {len(returned_jobs)} job(s):{filter_text}:**\n\n"
    display_jobs = returned_jobs[:10]

    for current_job in display_jobs:
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
            job_text += f"📅 {when_date}\n"
        if pub_date:
            job_text += f"📅 Posted: {pub_date}\n"
        if description:
            job_text += f"📝 {description}\n"
        if link:
            job_text += f"🔗 [Apply Here]({link})\n"
        message += job_text + "\n"
    if len(display_jobs) > 10:
        message += f"... and {len(display_jobs) - 10} more jobs. Use more specific filters to narrow results." # pylint: disable=C0301
    return message

def get_jobs(csv_file_path: str,
                command_args: str = "") -> List[Dict[str, Any]]:
    """
    Reads job data from CSV file and filters based on command parameters.

    Args:
        csv_file_path (str): Path to the CSV file containing job data
        command_args (str): Command arguments for filtering (e.g., "software -c google -l remote")

    Returns:
        list: List of job dictionaries matching the criteria
    """
    try:
        jobs = extract_entries_from_csv(csv_file_path)
    except OSError as e:
        print(f" Error loading or filtering jobs from CSV: {e}")
        return []
    filtered_jobs = []
    for current_job in jobs:
        job_type = current_job.get("Type", "").lower()
        title = current_job.get("Title", "").lower()
        job_keywords = [
            "job",
            "internship",
            "intern", 
        ]
        for specific_keyword in job_keywords:
            if specific_keyword in job_type or title:
                filtered_jobs.append(current_job)
            else:
                continue
    jobs = filtered_jobs
    if command_args.strip():
        filters = paste_jobs_command(command_args)
        jobs = filter_jobs(jobs, filters)
    return jobs
