"""Unittests for event_command.py"""

import unittest
import tempfile
from unittest.mock import patch

from data_processing.event_command import (
    filter_events,
    format_event_message,
)

class TestEventCommand(unittest.TestCase):
    """
    Tests for event_command.py
    """

    def setUp(self):
        self.sample_events = [
            {
                "Title": "Git Workshop",
                "subType": "Workshop",
                "Company": "Group",
                "Description": "Learn Git basics",
                "Location": "Room 101",
                "whenDate": "2023-04-12",
                "pubDate": "2023-04-01",
                "link": "https://example.com/git-workshop",
            },
            {
                "Title": "LeetCode Challenge Night",
                "subType": "Challenge",
                "Company": "Coding Society",
                "Description": "Solve coding problems together",
                "Location": "Room 102",
                "whenDate": "2023-04-19",
                "pubDate": "2023-04-02",
                "link": "https://example.com/leetcode-challenge",
            },
            {
                "Title": "Final Meeting + Pizza",
                "subType": "Meeting",
                "Company": "Tech Club",
                "Description": "Wrap up the semester with pizza",
                "Location": "Room 103",
                "whenDate": "2023-04-26",
                "pubDate": "2023-04-03",
                "link": "https://example.com/final-meeting",
            },
        ]

    def test_filter_events_by_location(self):
        """
        Test that filter_events filters events by location.
        """
        filters = "Room 101"
        result = filter_events(self.sample_events, filters)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["Title"], "Git Workshop")
    
    def test_filter_events_multiple_criteria(self):
        """
        Test that filter_events filters events by multiple criteria.
        """
        filters = "Tech Club"
        result = filter_events(self.sample_events, filters)
        self.assertEqual(len(result), 1)
        for event in result:
            self.assertIn("Final Meeting + Pizza", event["Title"])
    def test_format_event_message(self):
        """
        Test that format_event_message formats the event message correctly.
        """
        filters = "Workshop"
        result = format_event_message(self.sample_events, filters)
        self.assertIn("**📅 Upcoming Events:**", result)
        self.assertIn("Git Workshop", result)
        self.assertIn("LeetCode Challenge Night", result)
        self.assertIn("Final Meeting + Pizza", result)
        self.assertIn("Total events found: 3 (Filters: Workshop)", result)
    