from pydal import Field
from pydal.validators import IS_EMAIL, CRYPT, IS_NOT_EMPTY

from cms4py.aiomysql_pydal import AsyncDAL


def define_table(db: AsyncDAL):
    db.define_table(
        "member",
        Field(
            "login_name",
            label="Login name",
            unique=True,
            requires=[IS_NOT_EMPTY()]
        ),
        Field("nickname", label="Nickname", requires=IS_NOT_EMPTY()),
        Field(
            "email",
            label="Email",
            unique=True,
            requires=[IS_NOT_EMPTY(), IS_EMAIL()]
        ),
        Field(
            "phone",
            label="Phone",
            unique=True,
            requires=[IS_NOT_EMPTY()]
        ),
        Field("password", "password", label="Password", requires=CRYPT(), readable=False, writable=False),
        Field("openid", label="Open ID")
    )
    pass
