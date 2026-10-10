from threading import Lock


class Context:
    def __init__(self, logger, updateEvery:int=200):
        self.before: float = 0.0
        self.after: float = 0.0
        self._mutex = Lock()
        self.logger = logger

        self._updateCount = 0
        self.updateEvery = updateEvery

    def getCompressionInfo(self):
        return f"{self.before} -> {self.after} ({round((1-self.after/self.before) * 100)}%)"

    def updateCompression(self, before: float, after: float) -> None:
        with self._mutex:
            self.before += before
            self.after += after
            self._updateCount += 1
            if self._updateCount % self.updateEvery == 0:
                message = f"Context | Compression | {self.getCompressionInfo()}"
                self.logger.logger.info(message)