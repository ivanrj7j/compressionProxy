from mitmproxy import http

from src import Adblock, Conductor

conductor = Conductor()
adblock = Adblock("adservers.txt")

def request(flow:http.HTTPFlow):
    adblock.run(flow, conductor.context)

def response(flow: http.HTTPFlow):
    conductor.run(flow) 

def done():
    print("\n\nStats:")
    print("Compression:", conductor.context.getCompressionInfo())
    print(conductor.context.getAdInfo())