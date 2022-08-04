import re
from typing import List, Tuple, Union

from proxy.common.types import RePattern
from proxy.http import Url
from proxy.http.exception.base import HttpProtocolException
from proxy.http.parser import HttpParser
from proxy.http.server import ReverseProxyBasePlugin


class HttpBinReverseProxyPlugin(ReverseProxyBasePlugin):
    def routes(self) -> List[Union[str, Tuple[str, List[bytes]]]]:
        return [
            # A static route
            (
                r"/one$",
                [b"http://httpbin.org/get?id=1", b"https://httpbin.org/get?id=1"],
            ),
            # A dynamic route to catch requests on "/get/<int>""
            # See "handle_route" method below for what we do when
            # this pattern matches.
            r"/(.*)$",
        ]

    def handle_route(self, request: HttpParser, pattern: RePattern) -> Url:
        choice: Url = Url.from_bytes(b"https://httpbin.org")
        assert request.path
        result = re.search(pattern, request.path.decode())
        if not result or len(result.groups()) != 1:
            raise HttpProtocolException("Invalid request")
        assert choice.remainder is None
        choice.remainder = b"/"
        # NOTE: Internally, reverse proxy core replaces
        # original request.path with the choice.remainder value.
        # e.g. for this example, request.path will be "/get/1".
        # Core will automatically replace that with "/get?id=1"
        # before dispatching request to choice of upstream server.
        choice.remainder += f"{result.groups()[0]}".encode()
        print(choice)
        return choice
