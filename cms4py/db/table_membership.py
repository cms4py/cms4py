from pydal import DAL, Field


def define_table(db: DAL):
    db.define_table(
        "user_membership",
        Field('group', "reference user_group"),
        Field('user', "reference user")
    )
