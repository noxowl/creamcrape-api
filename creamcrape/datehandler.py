"""
:mod: 'creamcrape.datehandler'

-------------------------------------------------------------------------------

Make datetime object for specific needs.
.. :moduleauthor: Mirai Kim <me@euc-kr.net>

"""
import pytz
import datetime
from flask import current_app


local_tz = pytz.timezone(current_app.config['TIMEZONE'])
utc = pytz.utc


def formatdt(dt):
    dtstr = dt.strftime('%Y-%m-%d %H:%M:%S.')+(
           "%0.3f" % (dt.microsecond/10**6 + 0.1))[2:]
    return datetime.datetime.strptime(dtstr, '%Y-%m-%d %H:%M:%S.%f')


def begin_of_day():
    utc_dt = utc.localize(datetime.datetime.utcnow())
    local_dt_origin = local_tz.normalize(utc_dt.astimezone(local_tz))
    local_dt = datetime.datetime(local_dt_origin.year, local_dt_origin.month, local_dt_origin.day, 00, 00, 00,
                                 tzinfo=local_dt_origin.tzinfo)
    bod = utc.normalize(local_dt.astimezone(utc))
    return formatdt(bod)


def end_of_day():
    utc_dt = utc.localize(datetime.datetime.utcnow())
    local_dt_origin = local_tz.normalize(utc_dt.astimezone(local_tz))
    local_dt = datetime.datetime(local_dt_origin.year, local_dt_origin.month, local_dt_origin.day, 23, 59, 59,
                                 tzinfo=local_dt_origin.tzinfo)
    eod = utc.normalize(local_dt.astimezone(utc))
    return formatdt(eod)


def begin_of_week():
    utc_dt = utc.localize(datetime.datetime.utcnow())
    local_dt_origin = local_tz.normalize(utc_dt.astimezone(local_tz))
    local_dt_begin_of_week = local_dt_origin + datetime.timedelta(days=0 - local_dt_origin.weekday())
    local_dt_origin = local_dt_begin_of_week
    local_dt = datetime.datetime(local_dt_origin.year, local_dt_origin.month, local_dt_origin.day, 00, 00, 00,
                                 tzinfo=local_dt_origin.tzinfo)
    eod = utc.normalize(local_dt.astimezone(utc))
    return formatdt(eod)


def end_of_week():
    utc_dt = utc.localize(datetime.datetime.utcnow())
    local_dt_origin = local_tz.normalize(utc_dt.astimezone(local_tz))
    local_dt_end_of_week = local_dt_origin + datetime.timedelta(days=6 - local_dt_origin.weekday())
    local_dt_origin = local_dt_end_of_week
    local_dt = datetime.datetime(local_dt_origin.year, local_dt_origin.month, local_dt_origin.day, 23, 59, 59,
                                 tzinfo=local_dt_origin.tzinfo)
    eod = utc.normalize(local_dt.astimezone(utc))
    return formatdt(eod)
