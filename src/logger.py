import datetime
import logging
import os

from mitmproxy.http import HTTPFlow

from .job import ConstantJob


class Logger(ConstantJob):
    def __init__(self):
        self.startTime = datetime.datetime.now()
        self.filename = f"logs/{self.startTime.strftime('%Y.%m.%d %H-%M-%S')}.log"
        os.makedirs("logs", exist_ok=True)

        self.logger = logging.getLogger("webOptimizer")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        fileHandler = logging.FileHandler(self.filename, encoding="utf-8")
        fileHandler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))

        self.logger.addHandler(fileHandler)

    def run(self, flow:HTTPFlow):
        contentType = flow.response.headers.get(
            "content-type", ""
        )
        bodySize = len(flow.response.raw_content or b"")
        self.logger.info(f"{flow.request.pretty_url} | {contentType} | {bodySize} bytes")