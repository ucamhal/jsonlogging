jsonlogging
=========

`jsonlogging` provides structured log output from the `logging` module in JSON format.

Here's a pretty-printed example (output is normally compacted to a single line):

    {
        "message": {
            "formatted": "I'm running a test! The test is: foobar",
            "raw": "I'm running a test! The test is: %(test_name)s",
            "args": {
                "test_name": "foobar"
            }
        },
        "level": "ERROR",
        "time": "2013-06-26T17:50:16.598734",
        "location": {
            "file": "/Users/hwtb2/Documents/workspace/jsonlogging/jsonlogging/tests/test_jsonlogging.py",
            "line": 33,
            "function": "test_logged_messages_are_formatted_as_json"
        },
        "process": {
            "process_id": 83265,
            "process_name": "MainProcess"
        },
        "thread": {
            "id": 140735166720352,
            "name": "MainThread"
        }
    }

The structure of the JSON log is defined by a template, allowing complete control over the structure and content of the logged information.

Extending the template to insert custom values is as easy as writing a simple class with a `render(log_record)` method which returns the JSON value to log (e.g. a string, dict, list etc).

Quick Start
-----------

To output your logs as JSON you need to change your `logging.Handler`'s formatter from the default to the formatter implementation provided by `jsonlogging`. To do this you use the `logging.Handler.setFormatter()` method.

A JSON log formatter with sensible defaults is provided for convenience. An instance can be obtained by calling `jsonlogging.get_json_formatter()` with no arguments.


Interactive session example
---------------------------

    (jsonlogging)hwtb2@pebble:~/Documents/workspace/jsonlogging> python
    Python 2.7.2 (v2.7.2:8527427914a2, Jun 11 2011, 15:22:34)
    [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import logging, jsonlogging
    >>> logging.basicConfig()
    >>> logger = logging.getLogger()
    >>> logger.handlers[0].setFormatter(jsonlogging.get_json_formatter())

Let's log a simple message. The log output is going to stdout so it'll show up right after each logging call:

    >>> logger.error("oh noes!: %(thing)s", {"thing": "oops"})
    {"message":{"formatted":"oh noes!: oops","raw":"oh noes!: %(thing)s","args":{"thing":"oops"}},"level":"ERROR","time":"2013-06-27T11:01:57.286882","location":{"file":"<stdin>","line":1,"function":"<module>"},"process":{"process_id":93526,"process_name":"MainProcess"},"thread":{"id":140735166720352,"name":"MainThread"}}

We can log exceptions as well:

    >>> try:
    ...   1 / 0
    ... except ZeroDivisionError:
    ...   logger.exception("Maths fail")
    ...
    {"message":{"formatted":"Maths fail","raw":"Maths fail","args":[]},"exception":{"type":"exceptions.ZeroDivisionError","message":"integer division or modulo by zero","traceback":[{"file":"<stdin>","line":2,"function":"<module>"}]},"level":"ERROR","time":"2013-06-27T11:02:42.768527","location":{"file":"<stdin>","line":4,"function":"<module>"},"process":{"process_id":93526,"process_name":"MainProcess"},"thread":{"id":140735166720352,"name":"MainThread"}}

Let's make the logs a bit easier to read by configuring the JSON output to be pretty-printed:

    >>> import json
    >>> logger.handlers[0].setFormatter(jsonlogging.get_json_formatter(json_encoder=json.JSONEncoder(indent=2)))
    >>> logger.error("oh noes!: %(thing)s", {"thing": "oops"})
    {
      "message": {
        "formatted": "oh noes!: oops",
        "raw": "oh noes!: %(thing)s",
        "args": {
          "thing": "oops"
        }
      },
      "level": "ERROR",
      "time": "2013-06-27T11:04:21.834753",
      "location": {
        "file": "<stdin>",
        "line": 1,
        "function": "<module>"
      },
      "process": {
        "process_id": 93526,
        "process_name": "MainProcess"
      },
      "thread": {
        "id": 140735166720352,
        "name": "MainThread"
      }
    }
    >>> try:
    ...   1 / 0
    ... except ZeroDivisionError:
    ...   logger.exception("Maths fail")
    ...
    {
      "message": {
        "formatted": "Maths fail",
        "raw": "Maths fail",
        "args": []
      },
      "exception": {
        "type": "exceptions.ZeroDivisionError",
        "message": "integer division or modulo by zero",
        "traceback": [
          {
            "file": "<stdin>",
            "line": 2,
            "function": "<module>"
          }
        ]
      },
      "level": "ERROR",
      "time": "2013-06-27T11:04:57.020030",
      "location": {
        "file": "<stdin>",
        "line": 4,
        "function": "<module>"
      },
      "process": {
        "process_id": 93526,
        "process_name": "MainProcess"
      },
      "thread": {
        "id": 140735166720352,
        "name": "MainThread"
      }
    }

Tests
-----

To run the unit tests you can use `nosetests`. e.g.:

    (jsonlogging)hwtb2@pebble:~/Documents/workspace/jsonlogging> python `which nosetests` --with-coverage --cover-html --cover-package jsonlogging
    ....................
    Name                        Stmts   Miss  Cover   Missing
    ---------------------------------------------------------
    jsonlogging                    12      0   100%
    jsonlogging.formatters         11      0   100%
    jsonlogging.recordadapter       5      0   100%
    jsonlogging.values             55      0   100%
    ---------------------------------------------------------
    TOTAL                          83      0   100%
    ----------------------------------------------------------------------
    Ran 20 tests in 0.122s

    OK

(The `which nosetests` is needed because I'm using a virtualenvironment and `nosetests` doesn't pick up virtualenv packages if run normally.)