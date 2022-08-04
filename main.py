import ipaddress

import proxy
from proxy.http.server import HttpWebServerPlugin
from proxy.http.server.reverse import ReverseProxy

from sample.http_bin_reverse_proxy import HttpBinReverseProxyPlugin

if __name__ == "__main__":
    hostname = ipaddress.IPv4Address("0.0.0.0")
    plugins = [HttpWebServerPlugin, ReverseProxy, HttpBinReverseProxyPlugin]
    proxy.main(hostname=hostname, port=8899, plugins=plugins)
