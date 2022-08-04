import ipaddress

import proxy
from proxy.http.server import HttpWebServerPlugin
from proxy.http.server.reverse import ReverseProxy
from proxy.plugin.reverse_proxy import ReverseProxyPlugin

if __name__ == "__main__":
    hostname = ipaddress.IPv4Address("0.0.0.0")
    plugins = [HttpWebServerPlugin, ReverseProxy, ReverseProxyPlugin]
    proxy.main(hostname=hostname, port=8899, plugins=plugins)
