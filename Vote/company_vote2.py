#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from scrapy.http import HtmlResponse
import requests
import time
import logging
import logtool
import random


def chrome_header():
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
        # "Cache-Control": "max-age=0",
        # "Connection": "keep-alive",
        "Host": "www.ecloud-zj.com:88",
        # "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36"
    }


def extract_token(url, html):
    response = HtmlResponse(url, body=html, encoding='utf-8')
    response.xpath("//input[name=__RequestVerificationToken]")
    token = str(response.xpath("//input[@name='__RequestVerificationToken']/@value")[0].extract())
    return token


class Account(object):

    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd

    def __str__(self):
        return 'Account[%s, %s]' % (self.name, self.pwd)


class CompanyVoter(threading.Thread):

    def __init__(self, thread_name, accounts, proxies=None, timeout=15):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.accounts = accounts
        self.timeout = timeout
        self.proxies = proxies

        self.success_num = 0
        self.fail_num = 0

        self.logger = logtool.get_file_logger(thread_name)

    def log(self, message, level=logging.DEBUG):
        self.logger.log(level, '%s[success:%s, fail:%s] - %s' % (self.thread_name, self.success_num, self.fail_num, message))

    def random_proxy(self):
        if self.proxies:
            idx = random.randint(0, len(self.proxies) - 1)
            return { "http": self.proxies[idx]}
        else:
            return None

    def run(self):
        for account in self.accounts:
            try:
                session = requests.Session()
                proxy = self.random_proxy()
                if proxy:
                    session.proxies = proxy

                if self.do_login(session, account.name, account.pwd):
                    self.log("login success, %s" % (account, ))
                    if self.do_vote(session):
                        self.success_num += 1
                        self.log('vote success, %s' % account)
                    else:
                        self.fail_num += 1
                        self.log('vote fail, %s' % account)
                else:
                    self.fail_num += 1
                    self.log("login fail, %s" % (account, ), logging.WARN)

                time.sleep(0.3)
            except Exception as e:
                self.fail_num += 1
                self.log('vote fail, %s %s' % (account, e))

    def do_regist(self, account):
        pass

    def do_login(self, session, name, pwd):
        login_url = 'http://www.ecloud-zj.com:88/enterprises/Login'
        r = session.get(login_url, headers=chrome_header(), timeout=self.timeout)

        data = {}
        token = extract_token(login_url, r.text)
        '''
        UserName:8152538
        Password:4124bc0a
        __RequestVerificationToken:CfDJ8Dc7DjaiKOVFqagv25TofOK1BXJMS9q_y5PK_ikOmB9lhcoZRZtSlYVftokq2faBxvyyYPyLdOmL7sXbY1ZF5Xj6LOzwvG0sUV7d_08wbegyx_3ueQE4RMgGEeXMncn4Gk51KyHASJ5GrW55LGSTwFM
        '''
        data['UserName'] = name
        data['Password'] = pwd
        data['__RequestVerificationToken'] = token

        header = chrome_header()
        header['Referer'] = 'http://www.ecloud-zj.com:88/enterprises/Login'
        header['Origin'] = 'http://www.ecloud-zj.com:88'
        r = session.post(login_url, data=data, headers=header, timeout=self.timeout)
        if r.text.find('LogOff') > 0:
            return True
        else:
            return False

    def do_vote(self, session):
        main_url = 'http://www.ecloud-zj.com:88/web/main'
        '''
        Cookie:safedog-flow-item=1950407EF74F87B23A93D1B916A510E0;
        .AspNet.Session=22ce8fe7-e2d6-342b-df34-1677e86ca4ad;
        6v9ltmBQmuM=CfDJ8EihrEnGs4RHoN980lBwCGGjZpLtnQbPiqDzEiOc4cGh6AGC2dK0PPvWiX8uK9lJnCAS8YX_bVAQWS_SXxH5tgJa84FCeG45k6sV2Ls2Ck-VQJLraDkAflLHf8OkETueq3m-ErRVHyd42uHG-aQrHDg
        '''
        proxies = {}
        self.log('prepare to get main vote page')
        r = session.get(main_url, proxies=proxies, timeout=self.timeout)
        token = extract_token(main_url, r.text)

        vote_data = {
            'cc': 25,
            '__RequestVerificationToken': token
        }

        header = chrome_header()
        header['Host'] = 'www.ecloud-zj.com:88'
        header['Origin'] = 'http://www.ecloud-zj.com:88'
        header['Referer'] = 'http://www.ecloud-zj.com:88/web/main'

        self.log('prepare to vote')
        vote_url = 'http://www.ecloud-zj.com:88/web/voteSubmit'
        r = session.post(vote_url, data=vote_data, headers=header, proxies=proxies, timeout=self.timeout)
        fs = str(r.url).split('jscontent=')
        status = -1 if not fs or len(fs) < 2 else int(fs[1])
        self.log('status %s, %s' % (status, r.url))
        if status > 0:
            return True
        else:
            return False

# import socks
# import socket
# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 7070)
# socket.socket = socks.socksocket


def load_accounts(account_fname, skip=0):
    accounts = []
    i = 0

    out = open('account', 'w')
    for line in open(account_fname, "r").readlines():
        if not line or i < skip:  # or i < 4403:
            i += 1
            continue

        if i > 4403:
            break

        fs = line.split(',')
        name = fs[0]
        code = fs[1]
        pwd = fs[2]

        if pwd.endswith('\n'):
            pwd = pwd[:-1]

        accounts.append(Account(code, pwd))

    out.flush()
    out.close()
    return accounts


def load_proxies(fname):
    result = []
    for line in open(fname):

        result.append(line)
    return result


def main(voter_thread_num, account_fname, skip_account=0, proxy_fname=None):

    def slice_step(total, pieces):
        return total/pieces + (1 if total % pieces > 0 else 1)

    accounts = load_accounts(account_fname, skip_account)
    accounts_num = len(accounts)
    account_step = slice_step(accounts_num, voter_thread_num) #accounts_num/voter_thread_num + (1 if accounts_num % voter_thread_num > 0 else 0)

    proxies = load_proxies(proxy_fname) if proxy_fname else []
    proxies_num = len(proxies)
    proxy_step = slice_step(proxies_num, voter_thread_num)

    threads = []
    for i in xrange(0, voter_thread_num):
        start = i*account_step
        end = (i+1)*account_step
        accounts_slice = accounts[start:end]

        proxies_slice=None
        if proxies:
            proxies_slice = proxies[i*proxy_step][(i+1)*proxy_step]

        voter = CompanyVoter('thread_%s' % i, accounts_slice, proxies_slice)
        threads.append(voter)

        if end > accounts_num:
            break

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main(1, "conf/account", 13)