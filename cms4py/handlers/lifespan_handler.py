from cms4py.utils.log import Cms4pyLog
from cms4py.socketio import load_sio_files


async def handle_lifespan(scope, receive, send):
    while True:
        # 不断读取数据
        message = await receive()
        # 如果读取消息类型为 lifespan.startup，则进行初始化操作
        if message['type'] == 'lifespan.startup':
            await load_sio_files()
            # 在初始化完成后，向 asgi 环境发送启动完成消息
            await send({'type': 'lifespan.startup.complete'})
            Cms4pyLog.get_instance().info("Server started")
        # 如果读取消息类型为 lifespan.shutdown，则进行收尾工作
        elif message['type'] == 'lifespan.shutdown':
            # 在收尾工作结束后，向 asgi 环境发送收尾完成消息
            await send({'type': 'lifespan.shutdown.complete'})
            Cms4pyLog.get_instance().info("Server stopped")
            break
