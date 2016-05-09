#! /bin/python
# --coding: utf8 --

import requests
import threading


class ProxyChecker(threading.Thread):

    def __init__(self, thread_name, proxies):
        threading.Thread.__init__(self)

        self.thread_name = thread_name
        self.proxies = proxies

        self.good_proxies = []
        self.bad_proxies = []

    def run(self):
        for proxy_item in self.proxies:
            if self.do_check(proxy_item):
                self.good_proxies.append(proxy_item)
            else:
                self.bad_proxies.append(proxy_item)

    def do_check(self, proxy_item):
        try:
            proxies = {
                "http": proxy_item,
                # "http": "http://%s" % proxy_item,
            }
            r = requests.get("http://www.baidu.com", proxies=proxies, timeout=5)  # timeout 单位秒
            print r.status_code

            return r.status_code == 200
        except Exception as e:
            print e
            return False


def load_proxy_list(infile):
    result = []
    for line in open(infile).readlines():
        if not line:
            continue
        proxy_item = line[:-1]
        result.append(proxy_item)

    return result


def main(proxy_checker_num, infile, outfile):
    all_proxies = load_proxy_list(infile)
    total_proxy_num = len(all_proxies)
    step = total_proxy_num / proxy_checker_num + 1 if total_proxy_num % proxy_checker_num else 0

    threads = []
    for i in xrange(0, proxy_checker_num):
        start = i * step
        end = (i+1) * step

        if end > total_proxy_num:
            break

        slice = all_proxies[start:end]
        t = ProxyChecker("thread_%s" % i, slice)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    out = open(outfile, 'w')
    for t in threads:
        print t.good_proxies
        for item in t.good_proxies:
            out.write("http://%s\n" % item)
    out.flush()
    out.close()

if __name__ == '__main__':
    proxy_infile = 'good_proxy'
    proxy_outfile = 'good_proxy2'
    checker_num = 40
    main(checker_num, proxy_infile, proxy_outfile)