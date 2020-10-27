

from cms4py.utils.log import Cms4pyLog
from app.db import Db


class ActionWithDb:

    async def execute(self, req, res):
        raise NotImplementedError()

    async def __call__(self, *args, **kwargs):
        # 获取数据管理器实例
        db_manager = await Db.get_instance()
        # 通过连接池建立一个连接
        conn = await db_manager.async_pydal.acquire()
        # 获取数据库对象用于操作数据库
        self.db = await conn.cursor()

        # 无论在execute中发生了什么错误，总要执行释放连接的操作
        err = None
        try:
            await self.execute(*args, **kwargs)
        except BaseException as e:
            err = e
            Cms4pyLog.get_instance().error(e)

        # 关闭数据库对象
        await self.db.close()
        # 释放连接
        await db_manager.async_pydal.release(conn)

        if err:
            # 如果在执行 execute 过程中发生了错误，将此错误抛给ASGI
            raise err
