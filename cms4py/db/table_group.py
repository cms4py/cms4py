from pydal import Field

from cms4py.aiomysql_pydal import AsyncDAL


def define_table(db: AsyncDAL):
    db.define_table(
        "auth_group",
        Field('role'),
        Field('description'),
    )
    pass
