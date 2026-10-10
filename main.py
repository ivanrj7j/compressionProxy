from mitmproxy import http

from src import Conductor

conductor = Conductor()

def response(flow: http.HTTPFlow):
    conductor.run(flow) 