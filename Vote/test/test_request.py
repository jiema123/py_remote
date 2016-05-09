#! /bin/python
# --coding: utf8 --

# http://docs.python-requests.org/zh_CN/latest/user/quickstart.html

import requests
# http://docs.python-requests.org/zh_CN/latest/user/advanced.html
r = requests.post("http://www.baidu.com")

# print r.text
# print r.cookies
# print r.cookies['BAIDUID']

# ssh root@121.40.197.43    Jin251314

def test_socket(USE_SOCKS_PROXY):
    if USE_SOCKS_PROXY:
        import requesocks as requests
    else:
        import requests

    session = requests.session()
    session.proxies = {'http': 'socks5://127.0.0.1:7070',
                       'https': 'socks5://127.0.0.1:9050'}
    resp = session.get('http://www.baidu.com')
    # resp = session.get('https://api.github.com', auth=('user', 'pass'))
    print(resp.status_code)
    print(resp.headers['content-type'])
    print(resp.text)

test_socket(True)