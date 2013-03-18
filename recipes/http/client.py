#!/usr/bin/env python
import httplib
import urllib

def send_request(params, host, path, headers={}, method="GET", port=80):
    conn = httplib.HTTPConnection(host, port)
    conn.request(method, path, params, headers)
    res = conn.getresponse()
    ans = (res.status, res.getheaders(), res.read())
    conn.close()
    return ans


def local():
    params = urllib.urlencode({"url":2})
    ans = send_request(params, "www.baidu.com", "/")
    print ans[0]
    print ans[1]
    print ans[2]


if __name__ == "__main__":
    local()
