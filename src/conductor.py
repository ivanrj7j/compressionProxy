from mitmproxy.http import HTTPFlow

from .codeCompress import CodeCompressor
from .context import Context
from .exceptions import JobException
from .imageCompress import ImageCompressor
from .job import ConstantJob
from .logger import Logger


class Conductor:
    def __init__(self):
        self.logger = Logger()
        self.constantJobs:list[ConstantJob] = [
            CodeCompressor(),
            ImageCompressor()
        ]
        self.context = Context(self.logger)

    def run(self, flow:HTTPFlow):
        self.logger.run(flow)

        for job in self.constantJobs:
            jobName = type(job).__name__
            try:
                status = job.run(flow, self.context)
                if status:
                    self.logger.logger.info(f"{jobName} | {status}")
            except JobException as e:
                self.logger.logger.error(f"{jobName} | {e}")