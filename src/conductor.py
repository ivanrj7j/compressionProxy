from mitmproxy.http import HTTPFlow

from .codeCompress import CodeCompressor
from .exceptions import JobException
from .job import ConstantJob
from .logger import Logger


class Conductor:
    def __init__(self):
        self.logger = Logger()
        self.constantJobs:list[ConstantJob] = [
            CodeCompressor()
        ]

    def run(self, flow:HTTPFlow):
        self.logger.run(flow)

        for job in self.constantJobs:
            jobName = type(job).__name__
            try:
                status = job.run(flow)
                if status:
                    self.logger.logger.info(f"{jobName} | {status}")
            except JobException as e:
                self.logger.logger.error(f"{jobName} | {e}")