"""
Integration tests for the jsonlogging package.
"""

import json
import logging
import unittest
import StringIO

from mock import MagicMock

import jsonlogging


class TestJsonLogging(unittest.TestCase):
    def test_logged_messages_are_formatted_as_json(self):
        """
        Test a full run through the stack from a log call to a logging.Logger
        to JSON being written to a stream by a logging.Handler.
        """
        # Create our logging.Formatter implementation which produces JSON with
        # the default options.
        json_formatter = jsonlogging.get_json_formatter()

        # Configure logging
        stream = StringIO.StringIO()
        log_handler = logging.StreamHandler(stream=stream)
        log_handler.setFormatter(json_formatter)  # Use our JSON formatter
        log_handler.setLevel(logging.DEBUG)
        logger = logging.getLogger("test_jsonlogging")
        logger.propagate = False  # Make sure nobody else sees our test logs
        logger.setLevel(logging.DEBUG)
        logger.addHandler(log_handler)

        # Log something and verify that it pops out in our stream as JSON
        msg = "I'm running a test! The test is: %(test_name)s"
        args = {"test_name": "foobar"}
        logger.error(msg, args)

        stream_value = stream.getvalue()
        self.assert_valid_json(stream_value)
        message = json.loads(stream_value)

        self.assertEqual(logging.getLevelName(logging.ERROR),
                         message["level"])
        self.assertEqual("test_logged_messages_are_formatted_as_json",
                         message["location"]["function"])
        self.assertEqual(msg, message["message"]["raw"])
        self.assertEqual(args, message["message"]["args"])
        self.assertEqual(msg % args, message["message"]["formatted"])

    def assert_valid_json(self, string):
        try:
            json.loads(string)
        except Exception as e:
            raise AssertionError(
                "String was not valid JSON: {!r}, {}".format(string, e)
            )
