import asyncio
import os

import config

from . import mime_types
from . import http


def block_read_file(file_path) -> bytes:
    if os.path.exists(file_path) and os.path.isfile(file_path):
        f = open(file_path)
        file_content = f.read()
        f.close()
        return file_content.encode('utf-8') if isinstance(file_content, str) else file_content
    return None


async def handle_static_file_request(scope, send) -> bool:
    """
    If the file exists and with it's content sent, then return True 
    """
    data_sent = False
    file_path = f"{config.STATIC_FILES_ROOT}{scope['path']}"
    file_content = await asyncio.get_running_loop().run_in_executor(
        None, block_read_file, file_path
    )
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
    controller_name = tokens[1] if tokens_len >= 2 else 'default'
    action_name = tokens[2] if tokens_len >= 3 else "index"
    controller_file = os.path.join(
        config.CONTROLLERS_ROOT, f"{controller_name}.py"
    )
    current_loop = asyncio.get_running_loop()
    if await current_loop.run_in_executor(None, os.path.exists, controller_file) and \
            await current_loop.run_in_executor(None, os.path.isfile, controller_file):
        controller_file_content = await current_loop.run_in_executor(None, block_read_file, controller_file)
        controller_object = compile(
            controller_file_content,
            controller_file,
            "exec"
        )
        controller_global_scope = {}
        controller_local_scope = {}
        exec(controller_object, controller_global_scope, controller_local_scope)
        if action_name in controller_local_scope:
            await controller_local_scope[action_name](http.Request(scope, receive), http.Response(send))
            data_sent = True
    return data_sent
