

default_template = OrderedDict([
    ("message", OrderedDict([
        ("formatted", FormattedMessageValue()),
        ("raw", MessageValue("msg")),
        ("args", MessageValue("args"))
    ])),

    ("exception", OrderedDict([
        ("type", ExceptionTypeValue()),
        ("message", ExceptionMessageValue()),
        ("traceback", ExceptionTracebackValue())
    ])),

    ("level", MessageValue("levelname")),
    ("time", TimeValue()),

    ("location", OrderedDict([
        ("file", MessageValue("pathname")),
        ("line", MessageValue("lineno")),
        ("function", MessageValue("funcname")
    ])),

    ("process", OrderedDict([
        ("process_id", MessageValue("process")),
        ("process_name", MessageValue("processName"))
    ])),

    ("thread", OrderedDict([
        ("id", MessageValue("thread")),
        ("name", MessageValue("threadName")),
    ]))
]]