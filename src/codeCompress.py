
import json

import minify_html
import rcssmin
import rjsmin
from mitmproxy.http import HTTPFlow

from .context import Context
from .exceptions import JobException
from .job import ConstantJob


class CodeCompressor(ConstantJob):
    def _compressHTML(self, content:str):
        return minify_html.minify(
            content, 
            minify_css=True,
            minify_js=True,
            minify_doctype=True,
            allow_noncompliant_unquoted_attribute_values=True,
            allow_optimal_entities=True,
            allow_removing_spaces_between_attributes=True,
        )

    def _compressCSS(self, content:str):
        return rcssmin.cssmin(content)

    def _compressJS(self, content:str):
        return rjsmin.jsmin(content)

    def _compressJSON(self, content:str):
        return json.dumps(
            json.loads(content),
            separators=(",", ":"),
            ensure_ascii=False
        )

    def run(self, flow:HTTPFlow, context:Context):
        if flow is None or flow.response is None:
            return

        contentType = (
            flow.response.headers.get("content-type")
            or flow.response.headers.get("Content-Type")
            or ""
        ).strip().lower()

        if not contentType:
            return

        if "text/html" in contentType:
            compressionMethod = self._compressHTML
        elif "text/css" in contentType:
            compressionMethod = self._compressCSS
        elif "javascript" in contentType or "ecmascript" in contentType:
            compressionMethod = self._compressJS
        elif "application/json" in contentType:
            compressionMethod = self._compressJSON
        else:
            return

        try:
            content = flow.response.get_text()
            sizeBefore = len(content)
            if content:
                compressed = compressionMethod(content)
                flow.response.text = compressed
                sizeAfter = len(compressed) if compressed else sizeBefore
                context.updateCompression(sizeBefore, sizeAfter, url=flow.request.pretty_url, content_type=contentType)
                return f"{sizeBefore} -> {sizeAfter} ({round((1 - sizeAfter/sizeBefore) * 100)}%)"

        except Exception as exc:
            raise JobException(f"Could not decode response for {contentType}: {exc}") from exc