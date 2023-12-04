"""
Created on 2020/03/11
"""
from typing import Callable


async def send(send_func: Callable, status: int = 200, headers=None, body: bytes = b''):
    if headers is None:
        headers = [[b'content-type', "text/html"]]
    await send_func({
        'type': 'http.response.start',
        'status': status,
        'headers': headers
    })
    await send_func({
        'type': 'http.response.body',
        'body': body,
        'more_body': False
    })


async def send_304(send_func, mime_type: bytes, last_modified: bytes):
    """
    Args:
        send_func:
        mime_type:
        last_modified: http time string
    Returns:

    """
    await send(send_func, 304, [[b'content-type', mime_type], [b'last-modified', last_modified]])
