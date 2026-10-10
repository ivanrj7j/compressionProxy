from io import BytesIO

from mitmproxy.http import HTTPFlow
from PIL import Image

from .context import Context
from .exceptions import JobException


class ImageCompressor:
    def _compressImage(self, content:bytes):        
        with Image.open(
            BytesIO(content)
        ) as image:
            if image.format not in {"JPEG", "PNG"}:
                return

            output = BytesIO()
            image.save(output, format="WEBP", quality=50)
            compressed = output.getvalue()

            if len(compressed) >= len(content):
                return

            return compressed

    def run(self, flow:HTTPFlow, context:Context):
        response = flow.response

        if response is None or response.status_code != 200 or response.raw_content is None:
            return

        contentType:str = response.headers.get("content-type", "").lower().strip()

        if not contentType.startswith("image/"):
            return

        content = response.content
        sizeBefore = len(content)
        sizeAfter = sizeBefore
        try:
            compressed = self._compressImage(content)
        except Exception as e:
            raise JobException(f"Could not compress image due to `{e}")

        if compressed is not None:
            sizeAfter = len(compressed)
            flow.response.content = compressed
            flow.response.headers["Content-Type"] = "image/webp"


            for header in ("ETag", "Content-MD5", "Content-Range"):
                flow.response.headers.pop(header, None)

            flow.response.headers.pop("Accept-Ranges", None)
            context.updateCompression(sizeBefore, sizeAfter, url=flow.request.pretty_url, content_type=contentType)

            return f"{sizeBefore} -> {sizeAfter} ({round((1 - sizeAfter/sizeBefore) * 100)}%)"

            