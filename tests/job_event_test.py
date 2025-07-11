""" Unittests for job_event.py
"""
import unittest
from unittest.mock import patch
import sys
import os
from data_processing.job_event import (
    paste_jobs_command,
    filter_jobs,
    format_jobs_message,
    get_jobs,
)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
class TestJobEventFunctions(unittest.TestCase):
    """
    Tests for paste_jobs_command
    """
    def setUp(self):
        self.sample_jobs = [
            {
                "Type": "Internship",
                "Title": "Pizza Quality Assurance Intern",
                "Description": "Help us ensure our pizza reaches peak deliciousness. Must love cheese and have strong opinions about pineapple.",  # pylint: disable=C0301
                "Company": "Cheesy Dreams Inc",
                "Location": "Napoli, Italy",
                "whenDate": "Summer 2025",
                "pubDate": "2025-07-01",
                "link": "http://cheesydreams.com/apply",
                "entryDate": "2025-07-07",
            },
            {
                "Type": "Full-time",
                "Title": "Senior Cat Behavior Analyst",
                "Description": "Decode the mysterious ways of felines. Remote work encouraged (cats don't commute).",  # pylint: disable=C0301
                "Company": "Whiskers & Co",
                "Location": "Remote",
                "whenDate": "",
                "pubDate": "2025-06-28",
                "link": "http://whiskersco.com/careers",
                "entryDate": "2025-07-06",
            },
            {
                "Type": "Part-time",
                "Title": "Professional Bubble Wrap Popper",
                "Description": "Join our stress-relief team. Must have excellent finger dexterity and appreciation for satisfying sounds.",  # pylint: disable=C0301
                "Company": "Pop Culture Studios",
                "Location": "San Francisco, CA",
                "whenDate": "Fall 2025",
                "pubDate": "2025-07-05",
                "link": "http://popculture.com/jobs",
                "entryDate": "2025-07-05",
            },
            {
                "Type": "Co-op",
                "Title": "Unicorn Grooming Specialist",
                "Description": "Maintain the magical appearance of our unicorn fleet. Glitter allergy is a dealbreaker.",  # pylint: disable=C0301
                "Company": "Mythical Creatures Ltd",
                "Location": "Portland, OR",
                "whenDate": "Spring 2025",
                "pubDate": "2025-07-02",
                "link": "http://mythicalcreatures.com/apply",
                "entryDate": "2025-07-04",
            },
            {
                "Type": "Internship",
                "Title": "Cloud Whisperer Intern",
                "Description": "Interpret weather patterns and cloud formations. Must be comfortable working at high altitudes.",  # pylint: disable=C0301
                "Company": "Sky High Analytics",
                "Location": "Denver, CO",
                "whenDate": "Summer 2025",
                "pubDate": "2025-07-03",
                "link": "http://skyhigh.com/intern",
                "entryDate": "2025-07-03",
            },
        ]

    def test_paste_jobs_command_empty_args(self):
        """
        Test that no imputs in command line will return no filters
        """
        result = paste_jobs_command("")
        expected = {
            "role": None,
            "type": None,
            "season": None,
            "company": None,
            "location": None,
            "general_search": None,
        }
        self.assertEqual(result, expected)

    def test_paste_jobs_command_bracket_notation_full(self):
        """
        Test that inputs on command line return as filters
        """
        command = "-r tester -t internship -s summer -c cheese -l italy"
        result = paste_jobs_command(command)
        expected = {
            "role": "tester",
            "type": "internship",
            "season": "summer",
            "company": "cheese",
            "location": "italy",
            "general_search": None,
        }
        self.assertEqual(result, expected)

    def test_paste_jobs_command_flag_notation_all_flags(self):
        """
        Test for more flags to return as filters
        """
        command = "unicorn -r grooming -t internship -s spring -c mythical -l portland"
        result = paste_jobs_command(command)
        expected = {
            "role": "grooming",
            "type": "internship",
            "season": "spring",
            "company": "mythical",
            "location": "portland",
            "general_search": "unicorn",
        }
        self.assertEqual(result, expected)

    def test_paste_jobs_command_flag_notation_long_flags(self):
        """
        Test for longer flag names to return as filters
        """
        command = "cloud --role whisperer --type internship --season summer --company sky --location denver"  # pylint: disable=C0301
        result = paste_jobs_command(command)
        expected = {
            "role": "whisperer",
            "type": "internship",
            "season": "summer",
            "company": "sky",
            "location": "denver",
            "general_search": "cloud",
        }
        self.assertEqual(result, expected)

    def test_paste_jobs_command_flag_notation_general_search_only(self):
        """
        Test for no flags, just command line inputs to return as filters
        """
        command = "pizza quality assurance tester"
        result = paste_jobs_command(command)
        expected = {
            "role": None,
            "type": None,
            "season": None,
            "company": None,
            "location": None,
            "general_search": "pizza quality assurance tester",
        }
        self.assertEqual(result, expected)

    def test_paste_jobs_command_flag_notation_mixed_order(self):
        """
        Test for flags in unexpected order to return as filters
        """
        command = "-c whiskers cat -l remote -t full-time behavior"
        result = paste_jobs_command(command)
        expected = {
            "role": None,
            "type": "full-time",
            "season": None,
            "company": "whiskers",
            "location": "remote",
            "general_search": "cat behavior",
        }
        self.assertEqual(result, expected)

    def test_filter_jobs_no_filters(self):
        """
        Test that filter_jobs will return correct amount of jobs given no filters
        """
        filters = {}
        result = filter_jobs(self.sample_jobs, filters)
        self.assertEqual(len(result), 5)
        self.assertEqual(result, self.sample_jobs)

    def test_filter_jobs_general_search(self):
        """
        Test that general search terms will look through Title column of csv
        """
        filters = {"general_search": "pizza"}
        result = filter_jobs(self.sample_jobs, filters)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Title"], "Pizza Quality Assurance Intern")

    def test_filter_jobs_general_search_description(self):
        """
        Test that general search terms will look through Company column of csv
        """
        filters = {"general_search": "glitter"}
        result = filter_jobs(self.sample_jobs, filters)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Company"], "Mythical Creatures Ltd")

    def test_filter_jobs_role_filter(self):
        """
        Test that role filters resulting from flags in command line will
            look through Title column of csv
        """
        filters = {"role": "analyst"}
        result = filter_jobs(self.sample_jobs, filters)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Title"], "Senior Cat Behavior Analyst")

    def test_filter_jobs_type_filter(self):
        """
        Test that type filters resulting from flags in command line will
            look through Type column of csv and correctly return accurately
        """
        filters = {"type": "internship"}
        result = filter_jobs(self.sample_jobs, filters)
        self.assertEqual(len(result), 2)
        titles = [job["Title"] for job in result]
        self.assertIn("Pizza Quality Assurance Intern", titles)
        self.assertIn("Cloud Whisperer Intern", titles)

    def test_filter_jobs_season_filter(self):
        """
        Test that season filters resulting from flags in command line will
            look through Season column of csv
        """
        filters = {"season": "summer"}
        result = filter_jobs(self.sample_jobs, filters)
        self.assertEqual(len(result), 2)
        titles = [job["Title"] for job in result]
        self.assertIn("Pizza Quality Assurance Intern", titles)
        self.assertIn("Cloud Whisperer Intern", titles)

    def test_filter_jobs_company_filter(self):
        """
        Test that company filters resulting from flags in command line will
            look through Company column of csv
        """
        filters = {"company": "whiskers"}
        result = filter_jobs(self.sample_jobs, filters)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Company"], "Whiskers & Co")

    def test_filter_jobs_location_filter(self):
        """
        Test that location filters resulting from flags in command line will
            look through Location column of csv
        """
        filters = {"location": "remote"}
        result = filter_jobs(self.sample_jobs, filters)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Location"], "Remote")

    def test_filter_jobs_multiple_filters(self):
        """
        Test that multiple filters from flags in command line will 
            accurately look through respective columns of csv
        """
        filters = {"type": "Internship", "season": "summer"}
        result = filter_jobs(self.sample_jobs, filters)
        self.assertEqual(len(result), 2)
        for job in result:
            self.assertIn("Intern", job["Title"])

    def test_filter_jobs_complex_search(self):
        """
        Test that multiple filters from flags in command line will 
            accurately look through respective columns of csv
        """
        filters = {"role": "specialist", "location": "portland"}
        result = filter_jobs(self.sample_jobs, filters)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Title"], "Unicorn Grooming Specialist")

    def test_format_jobs_message_empty_list(self):
        """
        Test that given the input of no matching jobs, response will be printed
        """
        result = format_jobs_message([])
        self.assertEqual(result, "💼 No jobs found matching your criteria.")

    def test_format_jobs_message_single_job(self):
        """
        Test that given the input of a singular matching job, response will be printed
        """
        jobs = [self.sample_jobs[0]]
        result = format_jobs_message(jobs)
        self.assertIn("💼 **Found 1 job(s):**", result)
        self.assertIn("Pizza Quality Assurance Intern", result)
        self.assertIn("Cheesy Dreams Inc", result)
        self.assertIn("Napoli, Italy", result)
        self.assertIn("Summer 2025", result)
        self.assertIn("http://cheesydreams.com/apply", result)

    def test_format_jobs_message_multiple_jobs(self):
        """
        Test that given the input of multiple matching jobs, response will be printed
        """
        jobs = self.sample_jobs[:3]
        result = format_jobs_message(jobs)
        self.assertIn("💼 **Found 3 job(s):**", result)
        self.assertIn("Pizza Quality Assurance Intern", result)
        self.assertIn("Senior Cat Behavior Analyst", result)
        self.assertIn("Professional Bubble Wrap Popper", result)

    def test_format_jobs_message_with_filters(self):
        """
        Test that given filters in command line, response will print the filters
        """
        jobs = [self.sample_jobs[0]]
        filters = {"company": "cheesy", "type": "internship"}
        result = format_jobs_message(jobs, filters)
        self.assertIn("(Filters: company: cheesy, type: internship)", result)

    def test_format_jobs_message_with_general_search_filter(self):
        """
        Test that given general search terms in command line, response will print the filters
        """
        jobs = [self.sample_jobs[0]]
        filters = {"general_search": "pizza"}
        result = format_jobs_message(jobs, filters)

        self.assertIn("(Filters: search: pizza)", result)

    def test_format_jobs_message_limit_display(self):
        """
        Test that the message is limitted to 10 jobs per !job event
        """
        many_jobs = self.sample_jobs * 3     # 15 jobs
        result = format_jobs_message(many_jobs)
        self.assertIn("💼 **Found 15 job(s):**", result)
        self.assertIn("... and 5 more jobs", result)

class TestGetJobs(unittest.TestCase):
    """
    Tests for get_jobs function
    """
    def setUp(self):
        self.sample_jobs = [
            {
                "Type": "Internship",
                "Title": "Pizza Quality Assurance Intern",
                "Description": "Help us ensure our pizza reaches peak deliciousness.",
                "Company": "Cheesy Dreams Inc",
                "Location": "Napoli, Italy",
                "whenDate": "Summer 2025",
                "pubDate": "2025-07-01",
                "link": "http://cheesydreams.com/apply",
                "entryDate": "2025-07-07",
            },
            {
                "Type": "Full-time",
                "Title": "Senior Cat Behavior Analyst",
                "Description": "Decode the mysterious ways of felines.",
                "Company": "Whiskers & Co",
                "Location": "Remote",
                "whenDate": "",
                "pubDate": "2025-06-28",
                "link": "http://whiskersco.com/careers",
                "entryDate": "2025-07-06",
            },
            {
                "Type": "Part-time",
                "Title": "Professional Bubble Wrap Popper",
                "Description": "Join our stress-relief team.",
                "Company": "Pop Culture Studios",
                "Location": "San Francisco, CA",
                "whenDate": "Fall 2025",
                "pubDate": "2025-07-05",
                "link": "http://popculture.com/jobs",
                "entryDate": "2025-07-05",
            },
            {
                "Type": "Event",
                "Title": "Company Picnic",
                "Description": "Annual company gathering",
                "Company": "Fun Corp",
                "Location": "Park",
                "whenDate": "2025-08-01",
                "pubDate": "2025-07-01",
                "link": "http://funcorp.com/picnic",
                "entryDate": "2025-07-01",
            },
        ]

    @patch("data_collections.csv_updater.extract_entries_from_csv")
    def test_get_jobs_error_handling(self, mock_extract):
        """
        Test for error handling given not found csv file
        """
        mock_extract.side_effect = Exception("CSV file not found")
        result = get_jobs("error-handling.csv")
        self.assertEqual(result, [])

    @patch("data_collections.csv_updater.extract_entries_from_csv")
    def test_get_jobs_empty_csv(self, mock_extract):
        """
        Test for error handling given empty csv file
        """
        mock_extract.return_value = []
        result = get_jobs("empty.csv")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
