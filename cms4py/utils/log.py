
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
            # 设置自定义的日志格式，输出的日志包括行号这样的关键信息
            logging.Formatter(
                "[%(levelname)s %(name)s %(asctime)s %(pathname)s(%(lineno)s)] %(message)s"
            )
        )

        if self._log.parent:
            self._log.parent.handlers = []
            # 设置自定义的日志处理工具
            self._log.parent.addHandler(log_handler)

        # 设置日志的级别，该参数来自config.py文件中的配置，用于过滤不
        # 希望出现的日志
        self._log.setLevel(config.LOG_LEVEL)
        self.info = self._log.info
        self.debug = self._log.debug
        self.warning = self._log.warning
        self.error = self._log.error
