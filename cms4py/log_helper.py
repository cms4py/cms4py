import logging
import config

log = logging.getLogger(config.APP_NAME)

log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter("[%(levelname)s %(name)s %(asctime)s %(pathname)s(%(lineno)s)] %(message)s"))

if log.parent:
    log.parent.handlers = []
    log.parent.addHandler(log_handler)
log.setLevel(config.LOG_LEVEL)
