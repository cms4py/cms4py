

from .field import Field


class Table:
    """
    该对象用于封装pyDAL表达式
    """

    def __init__(self, pydal, pydal_cursor, pydal_table) -> None:
        """
        :param pydal: The pyDAL object
        :param pydal_connection: The PyDALConnection instance
        :param pydal_table:
        """
        super().__init__()
        self._pydal_table = pydal_table
        self._fields_map = {}
        self._pydal = pydal
        self._pydal_cursor = pydal_cursor

    @property
    def pydal_cursor(self):
        return self._pydal_cursor

    async def insert(self, **kwargs) -> int:
        sql = self._pydal_table._insert(**kwargs)
        await self.pydal_cursor.execute(sql)
        return self.pydal_cursor.rowcount

    async def update(self, query, **kwargs):
        return await self.pydal_cursor(query).update(**kwargs)

    async def delete(self, query):
        return await self.pydal_cursor(query).delete()

    async def update_or_insert(self, query, **kwargs):
        if await self.pydal_cursor(query).isempty():
            return await self.insert(**kwargs)
        else:
            return await self.update(query, **kwargs)

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __getattr__(self, item):
        pydal_field = self._pydal_table[item]
        if pydal_field in self._fields_map:
            async_field = self._fields_map[pydal_field]
        else:
            async_field = Field(self._pydal, self._pydal_cursor, pydal_field)
            self._fields_map[pydal_field] = async_field
        return async_field

    @property
    def ALL(self):
        return self._pydal_table.ALL

    async def by_id(self, record_id):
        return (await self._pydal_cursor(self.id == record_id).select()).first()
