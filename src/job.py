from abc import ABC, abstractmethod

from mitmproxy.http import HTTPFlow


class ConstantJob(ABC):
    @abstractmethod
    def run(self, flow:HTTPFlow):
        pass