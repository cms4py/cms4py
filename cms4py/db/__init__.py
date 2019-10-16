from pydal import DAL
import config
from . import table_user
from . import table_session


def connect_db():
    db = DAL(
        config.DB_URI,
        config.DB_POOR_SIZE,
        config.DB_FOLDER,
        migrate=config.DB_MIGRATE,
        bigint_id=config.DB_USE_BIGINT_ID
    )
    table_user.define_table(db)
    table_session.define_table(db)
    return db
