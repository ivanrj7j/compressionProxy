from threading import Lock


class Context:
    def __init__(self, logger, updateEvery:int=200):
        self.before: float = 0.0
        self.after: float = 0.0
        self.adsBlocked:int = 0
        self._compressionMutex = Lock()
        self._adMutex = Lock()
        self.logger = logger

        self._updateCount = 0
        self.updateEvery = updateEvery

    def getCompressionInfo(self):
        return f"{round(self.before/(2**20), 3)}MB -> {round(self.after/(2**20), 3)}MB ({round((1-self.after/self.before) * 100)}%)"

    def getAdInfo(self):
        return f"Blocked {self.adsBlocked} ads/trackers"

    def updateAdBlockCount(self):
        with self._adMutex:
            self.adsBlocked += 1

    def updateCompression(self, before: float, after: float) -> None:
        with self._compressionMutex:
            self.before += before
            self.after += after
            self._updateCount += 1
            if self._updateCount % self.updateEvery == 0:
                message = f"Context | Compression | {self.getCompressionInfo()} | {self.getAdInfo()}"
                self.logger.logger.info(message)