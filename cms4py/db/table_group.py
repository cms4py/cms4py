from pydal import DAL, Field


def define_table(db: DAL):
    db.define_table(
        "user_group",
        Field('role'),
        Field('name'),
        Field('description'),
    )
    pass
