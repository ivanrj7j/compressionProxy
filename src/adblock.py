from mitmproxy.http import HTTPFlow, Response

from .context import Context


class Adblock:
    def __init__(self, adserversPath:str):
        with open(adserversPath) as f:
            self.servers = {
                server.strip().lower()
                for server in f
                if server.strip() and not server.lstrip().startswith("#")
            }

    def run(self, flow:HTTPFlow, context:Context):
        if flow.request.pretty_host.strip().lower() in self.servers:
            flow.response = Response.make(204, b"")
            context.updateAdBlockCount(url=flow.request.pretty_url)
    