from mitmproxy import http

from src import Conductor

conductor = Conductor()

def response(flow: http.HTTPFlow):
    conductor.run(flow) 

def done():
    print("\n\nStats:")
    print("Compression:", conductor.context.getCompressionInfo())