from pydal import Field

from cms4py.aiomysql_pydal import AsyncDAL


def define_table(db: AsyncDAL):
    db.define_table(
        "cms4py_session",
        Field("session_id"),
        Field("session_content", "text")
    )
