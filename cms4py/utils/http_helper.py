
import re, datetime

months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]
month_str_to_num_map = {
    b"Jan": 1, b"Feb": 2, b"Mar": 3, b"Apr": 4, b"May": 5, b"Jun": 6,
    b"Jul": 7, b"Aug": 8, b"Sep": 9, b"Oct": 10, b"Nov": 11, b"Dec": 12
}
week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def format_time(tn) -> str:
    """
    在个位数前面补 0
    :param tn:
    :return:
    """
    return f'{tn}' if tn >= 10 else f"0{tn}"


def datetime_to_http_time(dt) -> str:
    """
    将 Python 的 datetime 转为 HTTP 协议标准的时间字符串
    :param dt:
    :return:
    """
    return f"{week_days[dt.weekday()]}, " \
           f"{format_time(dt.day)} {months[dt.month - 1]} {dt.year} " \
           f"{format_time(dt.hour)}:{format_time(dt.minute)}:{format_time(dt.second)} " \
           f"GMT"


def http_time_to_datetime(http_time: bytes):
    """
    将 HTTP 协议标准的时间字符串转成 Python 的 datetime，
    注意：时间字符串为 bytes 类型
    :param http_time:
    :return:
    """

    # 使用正则表达式匹配时间字符串，并截取其中的年月日时间信息
    result = re.match(
        b'\\w{3}, (\\d{2}) (\\w{3}) (\\d{4}) (\\d{2}):(\\d{2}):(\\d{2}) GMT',
        http_time
    )
    if result:
        # 根据年月日时间信息组装成一个 datetime
        day = int(result.group(1))
        month = month_str_to_num_map[result.group(2)]
        year = int(result.group(3))
        hour = int(result.group(4))
        minute = int(result.group(5))
        second = int(result.group(6))
        return datetime.datetime(
            year=year, month=month, day=day,
            hour=hour, minute=minute, second=second
        )
    return None
