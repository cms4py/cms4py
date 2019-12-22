from pydal import Field

from cms4py.aiomysql_pydal import AsyncDAL


def define_table(db: AsyncDAL):
    db.define_table(
        "auth_membership",
        Field('group_id', "reference user_group"),
        Field('user_id', "reference user")
    )
