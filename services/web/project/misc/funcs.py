
import random
import string
from datetime import datetime, timedelta


def rand_string(length=30):
    rand_str = ''.join(random.choice(
        string.ascii_letters + string.digits) for _ in range(length))
    return(rand_str)


def rand_user_id():
    return("u_"+str(random.randint(1, 1e10)))

def dayWeekYearNr(date):
    # dayOfYear = date.timetuple().tm_yday
    # here: weekday = 0 for Monday, 6 for Sunday
    # test = date.strftime("%W")
    # print(test)
    weekNr = int(date.strftime("%W"))
    try:
        year = date.year()
    except Exception as e:
        year = date.year
    try:
        wday = date.weekday()
    except Exception as e:
        wday = date.weekday
    
    yearWeekDay = year * 10000 + weekNr*100 + wday
    return yearWeekDay


def calc_weekstart(date, week_start=0):
    # returns for a given date the date when the week started, defined by week_start.
    # week_start = 0 returns the Monday before the given date, 1 returns Tuesday before given date, ...
    
    try:
        wday = date.weekday()
    except Exception as e:
        wday = date.weekday
    try:
        year = date.year()
    except Exception as e:
        year = date.year
    try:
        month = date.month()
    except Exception as e:
        month = date.month
    try:
        day = date.day()
    except Exception as e:
        day = date.day
    offset_days = week_start - wday
    if offset_days > 0:  
        offset_days = offset_days-7

    weekstart_date = datetime(year, month,
                              day) + timedelta(days=offset_days)

    return(weekstart_date)
