from pydal import DAL, Field


def define_table(db: DAL):
    db.define_table(
        "session",
        Field("session_id"),
        Field("session_content", "text")
    )
