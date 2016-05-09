#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from scrapy.http import HtmlResponse
import requests


def chrome_header():
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
        # "Cache-Control": "max-age=0",
        # "Connection": "keep-alive",
        "Host" : "www.ecloud-zj.com:88",
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

    def __init__(self, thread_name, accounts, timeout=15):
        self.thread_name = thread_name
        self.accounts = accounts
        self.timeout = timeout

    def run(self):
        for account in self.accounts:
            try:
                session = requests.Session()
                if self.do_login(session, account.name, account.pwd):
                    print "login success, %s" % (account, )
                    if self.do_vote(session):
                        print self.thread_name, 'vote success, ', account
                    else:
                        print self.thread_name, 'vote fail, ', account
            except Exception as e:
                print self.thread_name, 'vote fail, ', account, e

    def do_regist(self, account):
        pass

    def do_login(self, session, name, pwd):
        login_url = 'http://www.ecloud-zj.com:88/enterprises/Login'
        r = session.get(login_url, headers=chrome_header(), timeout=self.timeout)

        data = {}
        token = extract_token(login_url, r.text)
        # print 'login token', token

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
        print 'get main vote page'
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

        print 'do vote'
        vote_url = 'http://www.ecloud-zj.com:88/web/voteSubmit'
        r = session.post(vote_url, data=vote_data, headers=header, proxies=proxies, timeout=self.timeout)
        fs = str(r.url).split('jscontent=')
        status = -1 if not fs or len(fs) < 2 else int(fs[1])
        if status > 0:
            return True
        else:
            return False

'''
def login(name, pwd):
    session = requests.Session()

    proxies = {
        # 'http': 'http://107.151.152.218:80'
    }

    login_url = 'http://www.ecloud-zj.com:88/enterprises/Login'
    r = session.get(login_url,  proxies=proxies, headers=chrome_header())

    data = {}
    token = extract_token(login_url, r.text)
    print 'login token', token

    data['UserName'] = name
    data['Password'] = pwd
    data['__RequestVerificationToken'] = token
    header = chrome_header()
    header['Referer'] = 'http://www.ecloud-zj.com:88/enterprises/Login'
    header['Origin'] = 'http://www.ecloud-zj.com:88'
    r = session.post(login_url, data=data, headers=header,  proxies=proxies)
    if r.text.find('LogOff') > 0:
        print "login %s, %s" % (name, pwd) #{'.ecloud-zj.com': {'/': {'safedog-flow-item': Cookie(version=0, name='safedog-flow-item', value='3B60491D035B1D82FE322C82115DE6BA', port=None, port_specified=False, domain='.ecloud-zj.com', domain_specified=True, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=1462809626, discard=False, comment=None, comment_url=None, rest={}, rfc2109=False)}}}

        main_url = 'http://www.ecloud-zj.com:88/web/main'

        print 'get main vote page'
        r = session.get(main_url,  proxies=proxies, timeout=10)
        token = extract_token(main_url, r.text)
        print 'main token', token

        vote_data = {
            'cc' : 25,
            '__RequestVerificationToken': token
        }

        header = chrome_header()
        header['Host'] = 'www.ecloud-zj.com:88'
        header['Origin'] = 'http://www.ecloud-zj.com:88'
        header['Referer'] = 'http://www.ecloud-zj.com:88/web/main'

        print 'do vote'
        vote_url = 'http://www.ecloud-zj.com:88/web/voteSubmit' # http://www.ecloud-zj.com:88/web/voteSubmit
        r = session.post(vote_url, data=vote_data, headers=header,  proxies=proxies, timeout=20)

        sucess_msg = '您已经为10个县市投票成功'
        # html = r.text.encode('utf8').find(sucess_msg)

        fs = str(r.url).split('jscontent=')
        status = -1 if not fs or len(fs) < 2 else int(fs[1])
        if status > 0:
            print 'vote success'
        else:
            print 'vote fail'
'''

# import socks
# import socket
# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 7070)
# socket.socket = socks.socksocket


def load_accounts():
    accounts = []
    i = 0
    for line in open("conf/company.csv", "r").readlines():

        if not line or i < 500:  # or i < 4403:
            i += 1
            continue

        if i > 4403:
            break

        fs = line.split(',')

        code = fs[1] if len(fs[1]) > 4 else fs[2]
        name = fs[0][1:-1]
        code = code[1:-2]

        # print line, name, code

        import hashlib
        m2 = hashlib.md5()
        m2.update("aa")
        pwd = m2.hexdigest()[:8]
        # email = emails[random.randint(0, len(emails) - 1)][:-1]
        # contact = contacts[random.randint(0, len(contacts) - 1)]
        # phone = random_phone()
        # aid, bid = random_id()
        accounts.append(Account(code, pwd))
    return accounts


def main(voter_thread_num):
    accounts = load_accounts()
    accounts_num = len(accounts)

    step = accounts_num/voter_thread_num + 1 if accounts_num % voter_thread_num > 0 else 0
    threads = []
    for i in xrange(0, voter_thread_num):
        start = i*step
        end = (i+1)*step

        accounts_slice = accounts[start:end]
        voter = CompanyVoter('thread_%s' % i, accounts_slice)
        threads.append(voter)

        if end > accounts_num:
            break

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main(10)