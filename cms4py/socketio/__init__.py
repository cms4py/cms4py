
import socketio, os, config, importlib

sio = socketio.AsyncServer(async_mode='asgi')
sio_asgi_app = socketio.ASGIApp(sio)


async def load_sio_files():
    """
    加载 sio 文件
    :return:
    """
    sio_root = os.path.join(
        config.APP_DIR_NAME, config.SOCKET_IO_DIR_NAME
    )
    # 从 sio 文件目录中列出所有文件
    sio_files = os.listdir(sio_root)
    for f in sio_files:
        if f.endswith(".py"):
            # 去掉文件后缀名
            f_name = f[:-3]
            # 拼接成模块名
            module_name = "{}.{}.{}".format(
                config.APP_DIR_NAME,
                config.SOCKET_IO_DIR_NAME,
                f_name
            )
            # 导入模块
            importlib.import_module(module_name)
