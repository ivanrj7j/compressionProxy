from mitmproxy import http
import logging
import datetime
import os

startTime = datetime.datetime.now()

os.makedirs("logs", exist_ok=True)
filename = f"logs/{startTime.strftime("%Y.%m.%d %H-%M-%S")}.log"
print(filename)

logger = logging.getLogger("webOptimizer")
logger.setLevel(logging.INFO)
logger.propagate = False

fileHandler = logging.FileHandler(filename, encoding="utf-8")
fileHandler.setFormatter(logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
))

logger.addHandler(fileHandler)

def response(flow: http.HTTPFlow):
    contentType = flow.response.headers.get(
        "content-type", ""
    )
    bodySize = len(flow.response.raw_content or b"")

    print(
        f"{flow.request.pretty_url} | "
        f"{contentType} | {bodySize} bytes"
    )

    logger.info(f"{flow.request.pretty_url} | {contentType} | {bodySize} bytes")
