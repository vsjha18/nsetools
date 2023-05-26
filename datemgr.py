import datetime as dt
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from dateutil import rrule
from nsetools.errors import DateFormatError


def get_nearest_business_day(d):
    """ takes datetime object"""
    if d.isoweekday() == 7 or d.isoweekday() == 6:
        d = d - relativedelta(days=1)
        return get_nearest_business_day(d)

    # republic day
    elif d.month == 1 and d.day == 26:
        d = d - relativedelta(days=1)
        return get_nearest_business_day(d)
    # labour day
    elif d.month == 5 and d.day == 1:
        d = d - relativedelta(days=1)
        return get_nearest_business_day(d)
    # independece day
    elif d.month == 8 and d.day == 15:
        d = d - relativedelta(days=1)
        return get_nearest_business_day(d)
    # Gandhi Jayanti
    elif d.month == 10 and d.day == 2:
        d = d - relativedelta(days=1)
        return get_nearest_business_day(d)
    # chirstmas
    elif d.month == 12 and d.day == 25:
        d = d - relativedelta(days=1)
        return get_nearest_business_day(d)
    else:
        return d

def is_known_holiday(d):
    """accepts datetime/date object and returns boolean"""
    if type(d) == dt.datetime:
        d = d.date()
    elif type(d) != dt.date:
        raise DateFormatError("only date objects or datetime objects")
    else:
        # fine do nothing
        pass 

    # declare the list of holidays here.
    # republic day.
    if d.month  == 1 and d.day == 26:
        return True
    # labour day
    elif d.month == 5 and d.day == 1:
        d = d - relativedelta(days=1)
        return get_nearest_business_day(d)
    # independence day
    elif d.month == 8 and d.day == 15:
        return True
    # gandhi jayanti
    elif d.month == 10 and d.day == 2:
        return True
    # christmas
    elif d.month == 12 and d.day == 25:
        return True
    else:
        return False

def mkdate(d):
    """tries its best to return a valid date. it can accept pharse like today,
    yesterday, day before yesterday etc. 
    """
    # check if the it == a string
    return_date = ""
    if type(d) is str:
        if d == "today":
            return_date = dt.date.today()
        elif d == "yesterday":
            return_date = dt.date.today() - relativedelta(days=1)
        elif d == "day before yesterday":
            return_date = dt.date.today() - relativedelta(days=2)
        else:
            return_date = parse(d, dayfirst=True).date()
    elif type(d) == dt.datetime:
        return_date = d.date()
    elif type(d) == dt.date:
        return d
    else:
        raise DateFormatError("wrong date format %s" % str(d))
    # check if future date.
    return return_date

def usable_date(d):
    """accepts fuzzy format and returns most sensible date"""
    return get_nearest_business_day(mkdate(d))

def get_date_range(frm, to, skip_dates=[]):
    """accepts fuzzy format date and returns business adjusted date ranges"""
    # for x in rrule.rrule(rrule.DAILY, dtstart=s, until=dt.datetime.now(), byweekday=[0, 1, 2, 3, 4]): print(x)
    frm = usable_date(frm)
    to = usable_date(to)
    datelist = []
    for date in rrule.rrule(rrule.DAILY, dtstart=frm, until=to, byweekday=[0, 1, 2, 3, 4]):
        if not is_known_holiday(date):
            datelist.append(date.date())
    return datelist
