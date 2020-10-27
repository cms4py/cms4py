
from cms4py.handlers import lifespan_handler
from cms4py.handlers import error_pages
from cms4py.utils.log import Cms4pyLog
from cms4py.handlers import static_file_handler
from cms4py.handlers import dynamic_handler
from cms4py.socketio import sio_asgi_app


async def application(scope, receive, send):
    # 获取请求类型
    request_type = scope['type']

    # 如果是 http 类型的请求，则由该程序段处理
    if request_type == 'http':
        # 如果路径以 /socket.io 开始，则使用 socket.io app 进行处理
        if scope['path'].startswith("/socket.io"):
            return await sio_asgi_app(scope, receive, send)

        data_sent = await dynamic_handler.handle_dynamic_request(
            scope, receive, send
        )

        # 如果经过动态请求处理程序后未发送数据，则尝试使用静态文件请求
        # 处理程序处理
        if not data_sent:
            data_sent = await static_file_handler.handle_static_file_request(
                scope, send
            )

        # 如果静态文件处理程序未发送数据，则意味着文件找不到，此时应该
        # 向浏览器发送404页面
        if not data_sent:
            # 对于未被处理的请求，均向浏览器发回 404 错误
            await error_pages.send_404_error(scope, receive, send)
    # 如果是 websocket，则使用 socket.io app 处理
    elif request_type == 'websocket':
        return await sio_asgi_app(scope, receive, send)
    # 如果是生命周期类型的请求，则由该程序段处理
    elif request_type == 'lifespan':
        await lifespan_handler.handle_lifespan(scope, receive, send)
    else:
        Cms4pyLog.get_instance().warning("Unsupported ASGI type")
