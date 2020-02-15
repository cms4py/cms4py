import asyncio
import os

import config

from . import mime_types
from . import http
from . import file_helper
from .cache import cached_ast_objects


async def handle_static_file_request(scope, send) -> bool:
    """
    If the file exists and with it's content sent, then return True 
    """
    data_sent = False
    file_path = f"{config.STATIC_FILES_ROOT}{scope['path']}"
    file_content = None
    if await file_helper.file_exists(file_path) and await file_helper.isfile(file_path):
        file_content = await file_helper.read_file_async(file_path)
    if file_content:
        mime_type = mime_types.get_mime_type(file_path)
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', mime_type],
            ]
        })
        await send({
            'type': 'http.response.body',
            'body': file_content,
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
    controller_object = await cached_ast_objects.get_ast_object(controller_file)
    if controller_object:
        controller_global_scope = {}
        controller_local_scope = {}
        exec(controller_object, controller_global_scope, controller_local_scope)
        if action_name in controller_local_scope:
            req = http.Request(scope, receive)
            await controller_local_scope[action_name](req, http.Response(req, send))
            data_sent = True
    return data_sent
