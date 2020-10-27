
import config, datetime
from cms4py.utils import aiofile
from cms4py.utils import http_helper

# mime_type 表，这里列出最常用的文件，后期继续完善
mime_type_map = {
    ".html": b"text/html",
    ".htm": b"text/html",
    ".js": b"text/javascript",
    ".css": b"text/css",
    ".jpg": b"image/jpeg",
    ".jpeg": b"image/jpeg",
    ".png": b"image/png",
    ".gif": b"image/gif",
}


def get_mime_type(file_path: str) -> bytes:
    """
    根据文件路径获取对应的 mime_type
    :param file_path: 文件路径
    :return: 对应的 mime_type
    """

    last_dot_index = file_path.rfind(".")
    # 设定 mime_type 默认值为 text/plain
    mime_type = b"text/plain"
    if last_dot_index > -1:
        # 取得文件后缀名
        file_type = file_path[last_dot_index:]
        if file_type in mime_type_map:
            # 根据后缀名取得 mime_type
            mime_type = mime_type_map[file_type]
    return mime_type


async def handle_static_file_request(scope, send) -> bool:
    """
    处理静态文件请求
    :param scope:
    :param send:
    :return: 如果文件存在并且已经发送了数据，返回 True，否则返回 False
    """

    # 因为对于静态文件的请求均为 GET 方式的请求，所以其它方式的
    # 静态文件请求可视为非法请求，直接忽略即可
    if scope['method'] != 'GET':
        return False

    data_sent = False

    # 根据请求路径和静态文件根路径组装成文件真实路径
    file_path = f"{config.STATIC_FILES_ROOT}{scope['path']}"

    # 如果指定路径存在并且是文件，则读取文件并向浏览器返回数据
    if await aiofile.exists(file_path) and await aiofile.isfile(file_path):
        # 获取文件的 mime_type
        mime_type = get_mime_type(file_path)

        # 获取文件的修改时间
        file_timestamp = datetime.datetime.utcfromtimestamp(
            await aiofile.getmtime(file_path)
        )
        # 将文件的修改时间转成 HTTP 协议标准的时间字符串
        file_timestamp_http_time_str = http_helper.datetime_to_http_time(
            file_timestamp
        )
        file_timestamp_http_time_bytes: bytes = file_timestamp_http_time_str.encode(
            config.GLOBAL_CHARSET
        )

        # 读取浏览器端发来的请求头信息中的 if-modified-since 字段
        headers = scope['headers']
        if_modified_since_value_bytes = b''
        if headers and len(headers):
            for h in headers:
                if len(h) >= 2:
                    hk = h[0]
                    hv = h[1]
                    if hk == b'if-modified-since':
                        if_modified_since_value_bytes = hv
                        break

        if if_modified_since_value_bytes:
            # 如果时间相同，意味着文件未改变，则向浏览器发送 304 状态码
            if if_modified_since_value_bytes == file_timestamp_http_time_bytes:
                # 发送 304 状态码
                await send({
                    'type': 'http.response.start',
                    'status': 304,
                    'headers': [
                        [b'content-type', mime_type],
                        [b'last-modified', file_timestamp_http_time_bytes]
                    ]
                })
                await send({
                    'type': 'http.response.body',
                    'body': b"",
                    'more_body': False
                })

                data_sent = True
        # 如果在前面的逻辑中没有发送数据，则意味着需要读取文件数据并发送给浏览器
        if not data_sent:
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [
                    [b'content-type', mime_type],
                    [b'last-modified', file_timestamp_http_time_bytes]
                ]
            })
            file_content = await aiofile.read_file(file_path)
            await send({
                'type': 'http.response.body',
                'body': file_content,
                'more_body': False
            })
            data_sent = True
    return data_sent
