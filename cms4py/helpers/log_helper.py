import logging
import config


class Cms4pyLog:
    __instance = None

    @staticmethod
    def get_instance():
        if not Cms4pyLog.__instance:
            Cms4pyLog.__instance = Cms4pyLog()
        return Cms4pyLog.__instance

    def __init__(self) -> None:
        super().__init__()
        self._log = logging.getLogger(config.APP_NAME)

        log_handler = logging.StreamHandler()
        log_handler.setFormatter(
            logging.Formatter("[%(levelname)s %(name)s %(asctime)s %(pathname)s(%(lineno)s)] %(message)s"))

        if self._log.parent:
            self._log.parent.handlers = []
            self._log.parent.addHandler(log_handler)
        self._log.setLevel(config.LOG_LEVEL)
        self.info = self._log.info
        self.debug = self._log.debug
        self.warning = self._log.warning
