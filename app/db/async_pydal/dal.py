

from pydal import DAL as PY_DAL

import aiomysql
from aiomysql.pool import Pool
from .connection import PyDALConnection


class AsyncDAL:
    """
    该类将pyDAL封装为支持异步IO的模式，数据库驱动采用 aiomysql
    @see https://aiomysql.readthedocs.io/en/latest/pool.html
    """

    def __init__(self) -> None:
        super().__init__()
        self._pydal = None
        self._aiomysql_conn_pool = None

    @staticmethod
    async def create(
            host, user, password, db, port=3306,
            pool_max_size=10, echo=True
    ) -> "AsyncDAL":
        """
        该工厂方法用于支持以异步IO编程的方式创建 AsyncDAL 实例
        :param host: 数据库服务器主机
        :param user: 数据库登录用户名
        :param password: 数据库登录用户名对应的密码
        :param db: 数据库名
        :param port: 数据库服务器所在的端口号
        :param pool_max_size: 数据库连接池接受的最大连接数
        :param echo: 是否输出 SQL 语言，该功能可用于开发调试阶段
        :return:
        """
        return await AsyncDAL().async_init(
            host, user, password, db, port,
            pool_max_size, echo
        )

    async def async_init(
            self, host, user, password, db, port,
            pool_max_size, echo
    ) -> "AsyncDAL":
        """
        以异步方式初始化该实例，由于内置的 __init__ 函数无法通过
        异步IO的方式调用，所以写了个单独的支持以异步IO的方式调用的
        函数进行初始化
        """

        # 配置 pyDAL 连接，在不执行数据库指令的情况下pyDAL并不连接数据库
        self._pydal = PY_DAL(
            uri=f"mysql://{user}:{password}@{host}:{port}/{db}",
            migrate=False, migrate_enabled=False, bigint_id=True
        )

        # 配置 aiomysql 连接
        self._aiomysql_conn_pool = await aiomysql.create_pool(
            0, pool_max_size, echo, host=host, port=port, user=user,
            password=password, db=db
        )
        return self

    @property
    def aiomysql_conn_pool(self) -> Pool:
        """
        获取aiomysql连接池对象
        :return:
        """
        return self._aiomysql_conn_pool

    def close(self):
        """
        关闭连接池
        :return:
        """
        self.aiomysql_conn_pool.close()

    async def wait_closed(self):
        """
        等待连接池关闭
        :return:
        """
        await self.aiomysql_conn_pool.wait_closed()

    def terminate(self):
        """
        中止连接池
        :return:
        """
        self.aiomysql_conn_pool.terminate()

    async def acquire(self) -> PyDALConnection:
        """
        通过连接池获得一个连接上下文对象，并将其封装
        到PyDALConnection中
        :return:
        """
        return PyDALConnection(
            self._pydal,
            await self.aiomysql_conn_pool.acquire()
        )

    async def release(self, conn: PyDALConnection):
        """
        释放一个连接对象
        :param conn:
        :return:
        """
        await self.aiomysql_conn_pool.release(
            conn.aiomysql_conn
        )

    def define_table(self, tablename, *fields, **kwargs):
        """
        定义数据表
        """
        self._pydal.define_table(tablename, *fields, **kwargs)
