#!/usr/bin/python
# -*- coding: utf-8 -*-

from calendar import (
    Calendar,
    day_abbr,
    month_name,
    monthrange,
)
from datetime import datetime
from locale import getdefaultlocale
import locale as _locale


class TimeEncoding:
    def __init__(self, locale):
        self.locale = locale

    def __enter__(self):
        self.oldlocale = _locale.getlocale(_locale.LC_TIME)
        _locale.setlocale(_locale.LC_TIME, self.locale)

    def __exit__(self, *args):
        _locale.setlocale(_locale.LC_TIME, self.oldlocale)


def get_month_names(locale=''):
    """Get month names.

    Keyword argument:
    locale -- locale timezone, if not set, the function will take the default
    locale of your system.
    """

    locale = locale + '.UTF-8' if locale else '%s.%s' % getdefaultlocale()

    try:
        with TimeEncoding(locale):
            result = [month.capitalize() for month in month_name if month]

        return result

    except Exception:
        return get_month_names_eng()


def get_month_names_eng():
    """In case if get_month_names() method has failed."""

    result = list(month_name)

    return result


def get_days_abbrs(locale=''):
    """ Return list with days abbreviations """

    locale = locale + '.UTF-8' if locale else '%s.%s' % getdefaultlocale()

    try:
        with TimeEncoding(locale):
            result = list(day_abbr)
    except Exception:
        result.list(day_abbr)

    return result


def calc_quarter(year, month):
    """Determines the current quarter."""

    previous_year = year
    previous_month = month - 1
    next_year = year
    next_month = month + 1

    if month == 1:
        previous_month = 12
        previous_year = year - 1
    elif month == 12:
        next_month = 1
        next_year = year + 1

    first_month = (previous_year, previous_month)
    second_month = (year, month)
    third_month = (next_year, next_month)

    return [first_month, second_month, third_month]


def _get_month(current_year, current_month):
    """
    Return list of month's weeks, which day
    is a turple (<month day number>, <weekday number>)
    """

    cal = Calendar()
    month = cal.monthdays2calendar(current_year, current_month)

    # Append to month's days a bool value to know if the day is in month
    for week_number, week in enumerate(month):
        for day in week:
            in_this_month = 1
            day_number, weekday_number = day

            if not day_number:
                in_this_month = 0

            day = (day_number, weekday_number, in_this_month)

            month[week_number][weekday_number] = day

    if len(month) == 4:
        return month

    quarter = calc_quarter(current_year, current_month)

    # Zeros in first week
    first_week_zeros = 0
    first_week = month[0]

    for day in first_week:
        in_this_month = day[-1]
        if not in_this_month:
            first_week_zeros += 1

    # Zeros in last week
    last_week_zeros = 0
    last_week = month[-1]

    for day in last_week:
        in_this_month = day[-1]
        if not in_this_month:
            last_week_zeros += 1

    if first_week_zeros:
        # Last day of prev month
        previous_month = quarter[0]
        _, n_days = monthrange(*previous_month)

        for i in range(first_week_zeros):
            weekday = n_days - (first_week_zeros - 1 - i)
            month[0][i] = (weekday, i, 0)

    if last_week_zeros:
        for i in range(last_week_zeros):
            month[-1][-last_week_zeros + i] = (
                i + 1,
                7 - last_week_zeros + i,
                0,
            )

    return month


def get_quarter(current_year, current_month):
    """ Get quarter where current_month is a middle month """

    result = []
    quarter = calc_quarter(current_year, current_month)

    for month in quarter:
        result.append(_get_month(*month))

    return result


def today_date_list():
    """ Return list with today date """

    return [datetime.now().day, datetime.now().month, datetime.now().year]


def today_date():
    """ Return today date dd.mm.yyyy like 28.02.2015 """

    return datetime.now().strftime("%d.%m.%Y")
