import datetime
import inspect
import os
import traceback

import config
from . import cms4py_config
from . import mime_types
from .http import http, response_tpls
from .cache_managers import PythonAstObjectCacheManager
from .exceptions.HttpException import HttpException
from .helpers import http_helper, aiofile


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
    file_path = f"{config.STATIC_FILES_ROOT}{scope['path']}"
    if await aiofile.exists(file_path) and await aiofile.isfile(file_path):
        mime_type = mime_types.get_mime_type(file_path)
        file_timestamp = datetime.datetime.utcfromtimestamp(
            await aiofile.getmtime(file_path)
        )
        file_timestamp_http_time_str = http_helper.datetime_to_http_time(file_timestamp)
        file_timestamp_http_time_bytes: bytes = file_timestamp_http_time_str.encode(
            config.GLOBAL_CHARSET
        )

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
            if if_modified_since_value_bytes == file_timestamp_http_time_bytes:
                # 发送 304 状态码
                await send_304(send, mime_type, file_timestamp_http_time_bytes)
                data_sent = True
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


async def handle_dynamic_request(scope, receive, send) -> bool:
    data_sent = False
    request_path: str = scope['path']
    tokens = request_path.split("/")
    tokens_len = len(tokens)
    controller_name = config.DEFAULT_CONTROLLER
    if tokens_len >= 2:
        controller_name = tokens[1] or config.DEFAULT_CONTROLLER
    action_name = config.DEFAULT_ACTION
    if tokens_len >= 3:
        action_name = tokens[2] or config.DEFAULT_ACTION
    controller_file = os.path.join(
        config.CONTROLLERS_ROOT, f"{controller_name}.py"
    )
    will_reload_callback = None
    if not cms4py_config.CONTROLLERS_HOT_LOAD_ENABLED:
        async def will_reload_callback(*args):
            return False

    controller_object = await PythonAstObjectCacheManager.get_instance().get_data(
        controller_file,
        will_reload_callback=will_reload_callback
    )
    if controller_object:
        if action_name in controller_object:
            try:
                req = http.Request(scope, receive)
                await req.parse_form()
                res = http.Response(req, send)
                await res._load_language_dict()
                action = controller_object[action_name]
                req._controller = controller_name
                req._action = action_name
                if inspect.isclass(action):
                    await action()(req, res)
                else:
                    await action(req, res)
                if not res.body_sent:
                    await res.end(b'')
            except Exception as e:
                if isinstance(e, HttpException):
                    await response_tpls.send(send, e.status_code, body=e.body)
                else:
                    traceback.print_exc()
                    await response_tpls.send(send, 500, body=b"Server error")

            data_sent = True
    return data_sent
