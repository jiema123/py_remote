#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 'lijian' on 5/8/16

# coding: utf-8
'''
Accept:*/*
Accept-Encoding:gzip, deflate
Accept-Language:en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2
Connection:keep-alive
Content-Length:36
Content-Type:application/x-www-form-urlencoded
Host:vote.ecloud-zj.com
Origin:http://vote.ecloud-zj.com
Referer:http://vote.ecloud-zj.com/wx
User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36
X-Requested-With:XMLHttpRequest

url = 'http://vote.ecloud-zj.com/wx/voteSubmit'
cc:25
uid:aa0ab7ba226f46959af90ad46730bc13
'''
import urllib2
import urllib
import random
import time
import threading

class PersionVote(threading.Thread):

    def __init__(self, thread_name, proxies):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.use_proxy  = None
        self.proxies = proxies

        self.good_proxies = []
        self.bad_proxies = []

    def random_proxy(self):
        def random_pick(plist):
            return plist[random.randint(0, len(plist) - 1)]

        if self.proxies:
            return random_pick(self.proxies)
        else:
            return random_pick(self.good_proxies)

    def run(self):
        batch_size = 0
        for i in range(1, 10000):
            try:
                if batch_size > 50:
                    self.good_proxies.append(self.use_proxy)

                if self.use_proxy is None or batch_size > 30:
                    batch_size = 0
                    print '%s change proxy' % self.thread_name
                    self.use_proxy = self.random_proxy()

                if self.do_run(self.use_proxy):
                    print '%s, %sth vote success' % (self.thread_name, i)
                else:
                    print '%s, %sth vote fail' % (self.thread_name, i)

                batch_size += 1
                time.sleep(0.3)
            except urllib2.URLError, e:
                if self.use_proxy and self.use_proxy in self.proxies:
                    self.proxies.remove(self.use_proxy)
                    self.use_proxy = None
            except Exception as e:
                self.use_proxy = None
                print '%s %s' % (self.thread_name, e)

    def do_run(self, proxy_host):
        # proxy = "127.0.0.1:8888"
        proxy = urllib2.ProxyHandler({'http': proxy_host})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)

        #定义一个要提交的数据数组(字典)
        data = {}
        uid = ''.join(random.sample("abcdefghijlmnopqrstuvwxyz1234567890", 32)) +  ''.join(random.sample("abcdefghijlmnopqrstuvwxyz1234567890", 8))
        # print uid 2709973a27d285cfe02e59031a31438b61cf3e2c
        data['uid'] = uid #'xa0ab7ba226f46959af90ad46730bc13'

        #http://www.ecloud-zj.com/wx?code=031hmQDG0oCk962J79EG0mYRDG0hmQDe&state=STATE&isTest=1
        # data['uid'] =  "{&quot;errcode&quot;:40029,&quot;errmsg&quot;:&quot;invalid code, hints: [ req_id: _RYpHA0844n149 ]&quot;}"
        data['cc'] = '25'

        request = urllib2.Request('http://www.ecloud-zj.com/wx/Subget', urllib.urlencode(data))
        #Cookie:.AspNet.Session=a49d1c82-2870-f649-e8b0-1c069319e0af
        request.add_header('Cookie', '.AspNet.Session=76bd1827-fd87-260d-a507-c851b45382fd')
        request.add_header("Host", "www.ecloud-zj.com")
        request.add_header("Origin", "http://www.ecloud-zj.com")
        request.add_header("Referer", "http://www.ecloud-zj.com/wx?code=011L7htm0x52eg1tG2um0Bxetm0L7htK&state=STATE")
        request.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36")

        # url = 'http://www.ecloud-zj.com/wx/Subget'
        # post_data = urllib.urlencode(data)

        #提交，发送数据
        req = urllib2.urlopen(request)
        # req = urllib2.urlopen(url, post_data)

        #获取提交后返回的信息 http://www.ecloud-zj.com/wx/voteSubmwe
        content = req.read()
        if content == '1':
            return True
        else:
            return False

# import socks
# import socket
# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 8080)
# socket.socket = socks.socksocket

def load_proxy():
    ps = dict([(k[:-1], k[:-1]) for k in open('proxy').readlines() ])
    return ps.values()

def init_proxy():
    p = proxies.values()[random.randint(0, len(proxies) - 1)]
    proxy = urllib2.ProxyHandler({'http': p})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)

    return p

proxies = load_proxy()
import threading
urllib2.socket.setdefaulttimeout(10) #另一种方式
# inFile = open('proxy_candidate', 'r')
# outFile = open('available.txt', 'w')

all_thread = []
for i in range(1):
    start = i*60
    end = (i+1) * 100
    slice = proxies[start:end]

    t = PersionVote('thread_%s' % i, slice)
    all_thread.append(t)

for t in all_thread:
    t.start()

for t in all_thread:
    t.join()

# inFile.close()
# outFile.close()