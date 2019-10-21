from pydal import DAL, Field
from cms4py.aiomysql_pydal import AsyncDAL


def define_table(db: AsyncDAL):
    db.define_table(
        "session",
        Field("session_id"),
        Field("session_content", "text")
    )
