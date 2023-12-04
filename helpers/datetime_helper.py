import datetime


def get_datetime_now_at8():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))


def utcnow():
    return datetime.datetime.utcnow()


def get_datetime_now():
    return utcnow()


def get_date_today_at8():
    now = get_datetime_now_at8()
    return datetime.date(now.year, now.month, now.day)


def translate_time_from_zone_0_to_8(t):
    return t + datetime.timedelta(hours=8)
