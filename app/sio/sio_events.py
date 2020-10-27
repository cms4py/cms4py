

import time, asyncio
from cms4py.socketio import sio


async def echo_task(sid):
    for i in range(1, 6):
        # 向浏览器端发送消息
        await sio.emit(
            "echo",
            f"[{time.strftime('%X')}] Count: {i}",
            sid
        )
        # 等待1秒
        await asyncio.sleep(1)


@sio.event
async def connect(sid, environ):
    """
    连接成功
    """
    asyncio.create_task(echo_task(sid))
