from collections import deque
from threading import Lock


class Context:
    def __init__(self, logger=None, updateEvery: int = 200, history_limit: int = 50):
        self.before: float = 0.0
        self.after: float = 0.0
        self.adsBlocked: int = 0
        self.totalRequests: int = 0
        self.compressedRequests: int = 0
        self._compressionMutex = Lock()
        self._adMutex = Lock()
        self._historyMutex = Lock()
        self.logger = logger

        self._updateCount = 0
        self.updateEvery = updateEvery
        self.recent_flows = deque(maxlen=history_limit)

    def getCompressionInfo(self) -> str:
        with self._compressionMutex:
            before_mb = round(self.before / (1024 * 1024), 3)
            after_mb = round(self.after / (1024 * 1024), 3)
            ratio = round((1 - self.after / self.before) * 100, 1) if self.before > 0 else 0.0
            return f"{before_mb}MB -> {after_mb}MB ({ratio}%)"

    def getAdInfo(self) -> str:
        with self._adMutex:
            return f"Blocked {self.adsBlocked} ads/trackers"

    def updateAdBlockCount(self, url: str = ""):
        with self._adMutex:
            self.adsBlocked += 1
            self.totalRequests += 1
        if url:
            self.add_flow_history(url, "AD / TRACKER", 0, 0, status="BLOCKED")

    def updateCompression(self, before: float, after: float, url: str = "", content_type: str = "") -> None:
        with self._compressionMutex:
            self.before += before
            self.after += after
            self.totalRequests += 1
            if before > after:
                self.compressedRequests += 1
            self._updateCount += 1

        if url:
            self.add_flow_history(url, content_type, before, after, status="COMPRESSED" if before > after else "PASSTHROUGH")

        if self.logger and self._updateCount % self.updateEvery == 0:
            message = f"Context | Compression | {self.getCompressionInfo()} | {self.getAdInfo()}"
            self.logger.logger.info(message)

    def add_flow_history(self, url: str, content_type: str, before: float, after: float, status: str = "OK"):
        with self._historyMutex:
            savings = round((1 - after / before) * 100, 1) if before > 0 and after < before else 0.0
            self.recent_flows.appendleft({
                "url": url,
                "type": content_type,
                "before": before,
                "after": after,
                "savings": savings,
                "status": status,
            })

    def get_stats(self) -> dict:
        with self._compressionMutex, self._adMutex:
            saved_bytes = max(0.0, self.before - self.after)
            savings_pct = round((saved_bytes / self.before) * 100, 1) if self.before > 0 else 0.0
            return {
                "before_bytes": self.before,
                "after_bytes": self.after,
                "saved_bytes": saved_bytes,
                "savings_pct": savings_pct,
                "ads_blocked": self.adsBlocked,
                "total_requests": self.totalRequests,
                "compressed_requests": self.compressedRequests,
            }

    def get_recent_flows(self) -> list:
        with self._historyMutex:
            return list(self.recent_flows)