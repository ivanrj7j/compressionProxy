from mitmproxy import ctx, http

from src import Adblock, Conductor, TelemetryTUI

# Suppress mitmproxy default stdout log messages
try:
    ctx.options.flow_detail = 0
    ctx.options.termlog_verbosity = "warn"
except Exception:
    pass

conductor = Conductor()
adblock = Adblock("adservers.txt")
tui = TelemetryTUI(conductor.context)
tui.start()



def request(flow: http.HTTPFlow):
    adblock.run(flow, conductor.context)
    tui.update()


def response(flow: http.HTTPFlow):
    conductor.run(flow)
    tui.update()


def done():
    tui.stop()
    print("\n\n🏎️ FINAL COMPRESSION & AD-BLOCK STATS:")
    print("Compression:", conductor.context.getCompressionInfo())
    print(conductor.context.getAdInfo())