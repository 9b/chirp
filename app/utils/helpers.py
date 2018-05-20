"""Utility functions."""


def to_bool(value):
    """Take a value and convert it to a boolean type.

    :param value: string or int signifying a bool
    :type value: str
    :returns: converted string to a real bool
    """
    positive = ("yes", "y", "true",  "t", "1")
    if str(value).lower() in positive:
        return True
    negative = ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}")
    if str(value).lower() in negative:
        return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))


def now_time(str=True):
    """Get the current time and return it back to the app."""
    import datetime
    if str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return datetime.datetime.now()


def now_date(str=True):
    """Get the current date and return it back to the app."""
    import datetime
    if str:
        return datetime.date.datetime().strftime("%Y-%m-%d")
    return datetime.datetime.now()


def load_time(str_time):
    """Convert the date string to a real datetime."""
    import datetime
    return datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")


def load_date(str_time):
    """Convert the date string to a real datetime."""
    import datetime
    return datetime.datetime.strptime(str_time, "%Y-%m-%d")


def paranoid_clean(query_value):
    """Take a user query value and cleans.

    :param query_value: query value to clean up
    :type query_value: str
    :returns: string a clean value
    """
    if not query_value:
        return ''
    remove = ['{', '}', '<', '>', '"', "'", ";"]
    for item in remove:
        query_value = query_value.replace(item, '')
    query_value = query_value.rstrip().lstrip().strip()
    return query_value
