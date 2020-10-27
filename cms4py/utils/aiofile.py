
import asyncio, os
from typing import Any


class AsyncFunWrapper:

    def __init__(self, blocked_fun) -> None:
        super().__init__()

        # 记录阻塞型 IO 函数，便于后续调用
        self._blocked_fun = blocked_fun

    def __call__(self, *args):
        """
        重载函数调用运算符，将阻塞型IO的调用过程异步化，并返回一个可
        等待对象（Awaitable）通过重载运算符实现包装逻辑的好处是不
        用一个一个去实现阻塞型IO的所有成员函数，从而大大节省了代码量
        """
        return asyncio.get_running_loop().run_in_executor(
            None,
            self._blocked_fun,
            *args
        )


class AIOWrapper:
    def __init__(self, blocked_file_io) -> None:
        super().__init__()
        # 在包装器对象中记录阻塞型IO对象外界通过包装器调用其成员
        # 函数时，事实上是分成两步进行：
        # 第一步，获取指定的成员，而该成员是一个可被调用的
        #        对象（Callable）
        # 第二步，对该成员进行调用
        self._blocked_file_io = blocked_file_io

    # 重载访问成员的运算符
    def __getattribute__(self, name: str) -> Any:
        """
        在外界通过包装器（AIOWrapper）访问成员操作时，创建一个异步
        函数包装器（AsyncFunWrapper），目的是将函数调用过程异步化
        """
        return AsyncFunWrapper(
            super().__getattribute__(
                "_blocked_file_io"
            ).__getattribute__(name)
        )


async def open_async(*args) -> AIOWrapper:
    """
    当外界调用该函数时，将返回一个包装器（AIOWrapper）对象，该包装器
    包装了一个阻塞型IO对象
    """
    return AIOWrapper(
        # 通过run_in_executor函数执行阻塞型IO的open函数，并转发外
        # 界传入的参数
        await asyncio.get_running_loop().run_in_executor(
            None, open, *args
        )
    )


async def read_file(file_path) -> bytes:
    """
    以二进制模式读取文件内容
    :param file_path:
    :return:
    """
    f = await open_async(file_path, "rb")
    content = await f.read()
    await f.close()
    return content


async def exists(file_path) -> bool:
    """
    判断指定的文件是否存在
    :param file_path:
    :return:
    """
    return await asyncio.get_running_loop().run_in_executor(
        None, os.path.exists, file_path
    )


async def isfile(file_path) -> bool:
    """
    判断指定的路径是否为文件
    :param file_path:
    :return:
    """
    return await asyncio.get_running_loop().run_in_executor(
        None, os.path.isfile, file_path
    )


async def getmtime(file_path):
    """
    获取指定路径的文件的修改时间
    :param file_path:
    :return:
    """
    return await asyncio.get_running_loop().run_in_executor(
        None, os.path.getmtime, file_path
    )
