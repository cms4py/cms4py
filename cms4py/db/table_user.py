from pydal import DAL, Field
from pydal.validators import IS_NOT_IN_DB, IS_EMAIL, CRYPT, IS_NOT_EMPTY


def define_table(db: DAL):
    db.define_table(
        "user",
        Field(
            "login_name",
            label="Login name",
            unique=True,
            requires=[IS_NOT_EMPTY(), IS_NOT_IN_DB(db, "user.login_name")]
        ),
        Field("nick_name", label="Nick name", requires=IS_NOT_EMPTY()),
        Field(
            "email",
            label="Email",
            unique=True,
            requires=[IS_NOT_EMPTY(), IS_EMAIL(), IS_NOT_IN_DB(db, "user.email")]
        ),
        Field("password", "password", label="Password", requires=CRYPT(), readable=False, writable=False),
        Field("openid", label="Open ID")
    )
    pass
