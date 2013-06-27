from collections import OrderedDict
import json
import logging
import unittest

from mock import MagicMock, sentinel

from jsonlogging import values
from jsonlogging import recordadapter
from jsonlogging import formatters


class TestJsonFormatter(unittest.TestCase):
    def test_format_returns_result_of_encoder_encode(self):
        """
        Verify that JsonFormatter's format() method returns the
        value returned from the constructor's json_encoder param's
        encode() method. i.e. delegates to the encoder for output, so
        the JSON produced is under the control of the encoder.
        """
        template = values.OrderedObjectValue([])
        empty_adapter = recordadapter.ValueRecordAdapter(template)
        record = logging.makeLogRecord({})

        # Create a mock encoder to pass in as the JSON encoder
        mock_encoder = MagicMock()
        mock_encoder.encode.return_value = sentinel.encode_result

        # Format the record
        formatter = formatters.JsonFormatter(mock_encoder, empty_adapter)
        actual_result = formatter.format(record)

        # Assert that our mock encoder's encode method was called once
        mock_encoder.encode.assert_called_once_with(None)
        # ... and that the method returned the exact object returned by
        # our encoder's encode method.
        self.assertIs(sentinel.encode_result, actual_result)

    def test_adapters_to_json_return_val_is_encoded(self):
        """
        Verify that the return val of the adapter is passed to the encoder's
        encode method.
        """
        mock_adapter = MagicMock()
        mock_adapter.to_json.return_value = sentinel.adapter_result
        mock_encoder = MagicMock()

        formatter = formatters.JsonFormatter(mock_encoder, mock_adapter)

        # Action
        formatter.format(sentinel.log_record)
        # Assertion
        mock_adapter.to_json.assert_called_once_with(sentinel.log_record)
        mock_encoder.encode.assert_called_once_with(sentinel.adapter_result)
