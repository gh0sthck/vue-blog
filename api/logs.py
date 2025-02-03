import logging


class BlogLogger:
    _FMT = "[{level}] {asctime} {filename}, {lineo} | {message}"
    _LOGGER_FORMATTER = logging.Formatter(fmt=_FMT, style="{", datefmt="%H:%M:%S")

    def __init__(self, name: str = "blog"):
        self._name = name
        self._logger = logging.getLogger(name=self._name)
        self._logger.setLevel(logging.DEBUG) 
        handler = logging.StreamHandler()
        handler.setFormatter(self._LOGGER_FORMATTER)
        self._logger.addHandler(handler)

    def get_logger(self):
        return self._logger

    def set_level(self, level):
        self._logger.setLevel(level)
        return self._logger
