#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 'lijian' on 5/9/16

import urllib
import urllib2
import cookielib

def get():
    pass

def request(url, data=None, headers={}, http_proxy= None, timeout=60, debug=False):
    # opener = urllib2.build_opener(proxy)
    # urllib2.install_opener(opener)
    encoded_data = urllib.urlencode(data) if data else None
    data = {1:1}
    # request = urllib2.Request('http://www.ecloud-zj.com/wx/Subget', urllib.urlencode(data))
    req = urllib2.Request(
        url,
        data = encoded_data,
        headers=headers)
    # opener.add_handler();
    response = urllib2.urlopen(req)
    print response.read()


def set_env(http_proxy= None, use_cookie=False, debug=False):
    handlers = []
    if debug:
        http_handler = urllib2.HTTPHandler(debuglevel=1)
        https_handler = urllib2.HTTPSHandler(debuglevel=1)
        handlers.append(http_handler, https_handler)

    if http_proxy:
        proxy_handler = urllib2.ProxyHandler({'http': http_proxy})
        handlers.append(proxy_handler)

    if use_cookie:
        cookie_handle = cookielib.CookieJar()
        handlers.append(cookie_handle)

    opener = urllib2.build_opener(*handlers)
    urllib2.install_opener(opener)


def set_socket_proxy(ip, port):
    import socks
    import socket
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
    socket.socket = socks.socksocket

# urllib2.urlopen("http://www.baidu.com")
request("http://www.baidu.com")