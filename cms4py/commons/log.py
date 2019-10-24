import logging
import config

logging.basicConfig(format="[%(levelname)s %(name)s %(asctime)s %(filename)s(%(lineno)s)] %(message)s")

log = logging.getLogger(config.APP_NAME)
log.setLevel(config.LOG_LEVEL)
