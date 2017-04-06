from datetime import datetime, date

import arrow
import numpy as np
import pytz
from django.utils import timezone


class DateTimeOperations:
    @classmethod
    def datetime_to_timezone(cls, datetime_value, tz):
        if isinstance(datetime_value, datetime):
            if datetime_value.tzinfo is None:
                # timezone aware datetime object
                default_tz_datetime = arrow.get(datetime_value).to(tz=tz).datetime
            else:
                # naive datetime object
                default_tz_datetime = datetime_value.astimezone(tz=tz)
        elif isinstance(datetime_value, date):
            # date object only
            default_tz_datetime = arrow.get(datetime_value).replace(tzinfo=tz.zone).datetime
        else:
            default_tz_datetime = None

        return default_tz_datetime

    @classmethod
    def to_default_timezone(cls, datetime_value):
        """
        Converts a datetime or date object to the timezone specified in TIME_ZONE setting
        :param datetime_value: datetime object (timezone aware or not) or a date object
        :return: datetime object in default timezone
        """
        default_timezone_tz = timezone.get_default_timezone()
        return cls.datetime_to_timezone(datetime_value, default_timezone_tz)

    @classmethod
    def to_current_timezone(cls, datetime_value):
        """
        Converts a datetime or date object to the renderer timezone
        :param datetime_value: datetime object (timezone aware or not) or a date object
        :return: datetime object in renderer timezone
        """
        current_timezone_tz = timezone.get_current_timezone()
        return cls.datetime_to_timezone(datetime_value, current_timezone_tz)

    @classmethod
    def to_ist_timezone(cls, datetime_value):
        """
        Converts a datetime or date object to IST timezone
        :param datetime_value: datetime object (timezone aware or not) or a date object
        :return: datetime object in ist
        """
        ist_timezone_tz = pytz.timezone('Asia/Kolkata')
        return cls.datetime_to_timezone(datetime_value, ist_timezone_tz)

    @classmethod
    def ist_datetime(cls, *args, **kwargs):
        """
        get ist timestamp for passed in values
        """
        if len(args) == 0 and len(kwargs) == 0:
            # no arguments passed in -- return current timestamp in IST
            return arrow.now(tz=pytz.timezone('Asia/Kolkata')).datetime
        else:
            # arguments passed -- generate IST timestamp wrt arguments
            kwargs['tzinfo'] = kwargs.get('tzinfo', 'Asia/Kolkata')
            dtime = arrow.get(*args, **kwargs).datetime
            return cls.to_ist_timezone(dtime)

    @classmethod
    def ist_now(cls):
        """
        get current timestamp in ist format
        """
        return cls.ist_datetime()

    @classmethod
    def ist_now_arrow(cls):
        """
        get arrow object of current timestamp in ist format
        """
        return arrow.now(tz=pytz.timezone('Asia/Kolkata'))

    @classmethod
    def num_weekdays(cls, start, end):
        """
        returns number of days b/w start_date & end_date, excluding Sundays
        """
        days = np.busday_count(start.date(), end.date(), weekmask='1111110')
        return int(days)

    @classmethod
    def get_range_today(cls):
        """
        returns the start and end timestamps for current date
        """
        today = cls.ist_now_arrow()
        start, end = today.span('day')
        return start.datetime, end.datetime

    @classmethod
    def get_range_yesterday(cls):
        """
        returns the start and end timestamps for yesterday
        """
        yesterday = cls.ist_now_arrow().replace(days=-1)
        start, end = yesterday.span('day')
        return start.datetime, end.datetime

    @classmethod
    def get_range_current_week(cls):
        """
        returns the start and end timestamps for current week
        """
        today = cls.ist_now_arrow()
        start, end = today.span('week')
        return start.datetime, end.datetime

    @classmethod
    def get_range_last_week(cls):
        """
        returns the start and end timestamps for last week
        """
        today = cls.ist_now_arrow()
        start, end = today.replace(weeks=-1).span('week')
        return start.datetime, end.datetime

    @classmethod
    def get_range_current_month(cls):
        """
        returns the start and end timestamps for current month
        """
        today = cls.ist_now_arrow()
        start, end = today.span('month')
        return start.datetime, end.datetime

    @classmethod
    def get_range_last_month(cls):
        """
        returns the start and end timestamps for last month
        """
        today = cls.ist_now_arrow()
        start, end = today.replace(month=-1).span('month')
        return start.datetime, end.datetime

    @classmethod
    def get_range_calendar_year(cls):
        """
        returns the start and end timestamps for current calendar year
        """
        today = cls.ist_now_arrow()
        start, end = today.span('year')
        return start.datetime, end.datetime
