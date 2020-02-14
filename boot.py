import cms4py
from app import routes
import config

routes.config(cms4py.create_server(config.DEFAULT_AIO_LIB)).start()
