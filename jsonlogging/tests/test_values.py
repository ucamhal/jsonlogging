import logging
import unittest

from jsonlogging import values


class TestRecordValue(unittest.TestCase):
    def setUp(self):
        self.record_params = dict(
            name="testlogger",
            level=logging.DEBUG,
            pathname="/some/path.py",
            lineno=34,
            msg="This is a msg. %s",
            args=[123],
            func="some_func"
        )
        self.record = logging.makeLogRecord(self.record_params)

    def test_record_value_renders_expected_value(self):
        for (name, value) in self.record_params.items():
            record_value = values.RecordValue(name)
            self.assertEqual(value, record_value.render(self.record))


class TestDateRecordValue(unittest.TestCase):
    pass