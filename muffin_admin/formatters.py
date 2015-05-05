""" Define formatters. """
import datetime as dt
from html import escape


def default_formatter(handler, item, value):
    """ Default formatter. """
    if hasattr(value, '__unicode__'):
        value = value.__unicode__()
    else:
        value = str(value)
    return escape(value)


def bool_formatter(handler, item, value):
    """ Boolean formatter. """
    glyph = 'ok' if value else 'minus'
    return '<span class="glyphicon glyphicon-%s"></span>' % glyph


def list_formatter(handler, item, value):
    """ Format list. """
    return u', '.join(str(v) for v in value)


def empty_formatter(handler, item, value):
    """ Format None. """
    return ''


def datetime_formatter(handler, item, value):
    """ Format Datetime. """
    return value.strftime('<span style="white-space: nowrap">%Y-%m-%d %H:%M</span>')


def date_formatter(handler, item, value):
    """ Format Date. """
    return value.strftime('%Y-%m-%d')


FORMATTERS = {
    type(None): empty_formatter,
    bool: bool_formatter,
    list: list_formatter,
    dt.datetime: datetime_formatter,
}


def format_value(handler, item, column):
    """ Format value. """
    value = getattr(item, column, None)
    formatter = FORMATTERS.get(type(value), default_formatter)
    return formatter(handler, item, value)
