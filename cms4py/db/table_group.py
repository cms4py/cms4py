from pydal import DAL, Field
from cms4py.aiomysql_pydal import AsyncDAL


def define_table(db: AsyncDAL):
    db.define_table(
        "user_group",
        Field('role'),
        Field('name'),
        Field('description'),
    )
    pass
