import config
import os
import asyncio
from . import mime_types


def block_read_file(file_path) -> bytes:
    if os.path.exists(file_path) and os.path.isfile(file_path):
        f = open(file_path)
        file_content = f.read()
        f.close()
        return file_content.encode('utf-8') if isinstance(file_content, str) else file_content
    return None


async def handle_static_file_request(scope, send):
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
