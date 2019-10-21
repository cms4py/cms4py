from pydal import DAL, Field
from cms4py.aiomysql_pydal import AsyncDAL


def define_table(db: AsyncDAL):
    db.define_table(
        "user_membership",
        Field('group', "reference user_group"),
        Field('user', "reference user")
    )
