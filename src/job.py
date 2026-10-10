from abc import ABC, abstractmethod

from mitmproxy.http import HTTPFlow

from .context import Context


class ConstantJob(ABC):
    @abstractmethod
    def run(self, flow:HTTPFlow, context:Context):
        pass