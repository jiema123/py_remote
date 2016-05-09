#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 'lijian' on 5/7/16

"""
ssh -N -D 127.0.0.1:8080 scrapy@120.55.118.42

Request URL:http://vote.ecloud-zj.com/enterprises/Login
Request Method:GET
Status Code:200 OK
Remote Address:120.55.91.150:80

UserName:695722324
Password:12345678
__RequestVerificationToken:CfDJ8GtrgEe0yUNPgLvJx0u6e_5oa1VaQQlrIQkpGHA-Dq672kcW7nMuo9jxkzM6ivyG5c1nV0uBnO-dScH5y1EUGYyXBXWUsgKu5h0zg45iAPsMktajv9KgtG9XZOStGugCHSHF-Fn4z_4bcPCbA_GB
"""
import random
import urllib
import cookielib
import urllib2
import  logging

# 创建一个logger
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('vote.log')
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
# logger.addHandler(ch)

def do_register(companyName, companyCode, pwd, contact, email, phone, aid, bid):
    #定义一个要提交的数据数组(字典)

    req = urllib2.urlopen('http://vote.ecloud-zj.com/enterprises/Register')
    print req.read()

    data = {}
    data['name'] = companyName
    data['codeCertificate'] = companyCode
    data['address'] = ''
    data['enterpriseCustomCode'] = ''
    data['email'] = email
    data['generalManager'] = contact
    data['managerTel'] = phone

    data['ParentAID'] = aid #914
    data['ParentBID'] = bid #915

    data['Password'] = pwd
    data['ConfirmPassword'] = pwd

    #定义post的地址
    url = 'http://vote.ecloud-zj.com/enterprises/Register'
    post_data = urllib.urlencode(data)

    #提交，发送数据
    req = urllib2.urlopen(url, post_data)

    #获取提交后返回的信息'<script type="text/javascript"> alert(\\'组织机构代码已经存在\\');javascript:history.go(-1);</script>'
    html = req.read()
    # logger.debug(html)
    print html

def random_pwd():
    return ''.join(random.sample("abcdefghijlmnopqrstuvwxyz1234567890", 8))

def random_manger():
    return ','.join(random.choice(['张', '王', '赵', '钱']))

def random_phone():
    return ''.join([
        str(random.choice([138, 182, 133, 180, 188, 135, 155, 152])),
        ''.join(random.sample("1234567890", 8))]
    )

def do_login(UserName, Password):

    #定义一个要提交的数据数组(字典)
    data = {}
    data['UserName'] = UserName
    data['Password'] = Password

    #定义post的地址
    url = 'http://www.ecloud-zj.com:88/enterprises/Login'
    post_data = urllib.urlencode(data)

    # r = urllib2.urlopen('http://www.baidu.com')
    #提交，发送数据
    req = urllib2.urlopen(url, post_data)

    #获取提交后返回的信息  '<script type="text/javascript"> alert(\\'组织机构代码已经存在\\');javascript:history.go(-1);</script>'
    content = req.read()
    cs = ['%s=%s' % (c.name, c.value) for c in cj]
    cookie = '; '.join(cs)
    print cookie

    if not content.find('title="去投票"'):
        print '用户名或者密码错误', content
        return
    print content

    req = urllib2.urlopen('http://www.ecloud-zj.com:88/web/main?jscontent=1')
    html = req.read()

    vote_url ='http://vote.ecloud-zj.com:88/web/voteSubmit'
    from scrapy.http import HtmlResponse
    response = HtmlResponse(vote_url, body=html)

    response.xpath("//input[name=__RequestVerificationToken]")
    token = str(response.xpath("//input[@name='__RequestVerificationToken']/@value")[0].extract())
    # Selector(response=response).xpath('//span/text()').extract()

    '''
    safedog-flow-item=1950407EF74F87B23A93D1B916A510E0;
    .AspNet.Session=22ce8fe7-e2d6-342b-df34-1677e86ca4ad;
    6v9ltmBQmuM=CfDJ8Dc7DjaiKOVFqagv25TofOJk2lBifr_jVEttFNhx2QNy4aoZheEAyj8jNxAghbT3rP-Cg9D1P2onQzq5TfIji4zgQV-5_-z0NKyDs3RvoY_e3bqurjQAklP4Mgt_aTPRG8zQZ1Pkrm4VcQFf-mM5q8c
    '''
    data = {}
    data['cc'] = 25
    data['__RequestVerificationToken'] = token

    post_data = urllib.urlencode(data)
    req = urllib2.urlopen('http://vote.ecloud-zj.com/web/voteSubmit', post_data)
    content = req.read()
    if content and content.find('您已经为10个县市投票成功') > 0:
        logger.info(UserName + " vote success")
    else:
        logger.warn(UserName + "vote fail")

    print content

# 34179765-2
# 605201

# import socks
# import socket
# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 8080)
# socket.socket = socks.socksocket

# proxy = urllib2.ProxyHandler({'http': '127.0.0.1:8080'})
# opener = urllib2.build_opener(proxy)
# urllib2.install_opener(opener)


def load_names():
    result = []
    for line in open("conf/names"):
        line_names = line.split("#")
        result.extend(line_names)

    return result

def load_email():
    return open("conf/emails").readlines()

Cates = {
    91 : ['92', '129', '175', '195', '212'],
    1 :['2', '14', '22', '43', '54', '68', '78', '85'],
    221 : ['222', '228', '240', '248', '257', '270'],
    279 : ['280', '285', '289', '294', '299', '307', '320', '328'],
    339 : ['340', '358', '370', '385', '398', '403', '410', '416', '422'],
    451 : ['452', '464', '475', '492', '501', '506', '514', '518', '526'],
    533 : [534],
    538 : ['539', '554', '564', '586', '593'],
    607 : ['608', '617', '627', '633', '638', '645', '660', '670'],
    678 : ['679', '685', '705', '725', '733', '763', '768', '782', '784'],
    797 : ['798', '807', '814', '830', '837', '847'],
    855 : ['856'],
    866 : ['867', '873', '878', '886', '892', '906'],
    914 : ['915', '921', '930', '952', '962', '970', '978', '993'],
    1010 : ['1011', '1024', '1038', '1046', '1056', '1063'],
    1078 : ['1079', '1090', '1100', '1116', '1125', '1132', '1138', '1143'],
    }

def random_id():
    keys = Cates.keys()
    aid = keys[random.randint(0, len(keys)-1)]

    values = Cates[aid]
    bid = values[random.randint(0, len(values)-1)]

    return aid, bid

contacts = load_names()
emails = load_email()

i = 0
for line in open("conf/company.csv", "r").readlines():

    if not line or i < 500: # or i < 4403:
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
    email = emails[random.randint(0, len(emails)-1)][:-1]
    contact = contacts[random.randint(0, len(contacts)-1)]
    phone = random_phone()
    aid, bid = random_id()

    logger.info("Register %s, %s , code %s , pwd %s , contact %s , email %s , phone %s , aid %s , bid %s",
                i, name, code, pwd, contact, email, phone, aid, bid)
    i = i+1
    try:
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        # do_register(name, code, pwd, contact, email, phone, aid, bid)
        # do_login(code, pwd) 91330203MA28111B2 4124bc0a
        print code, pwd

        import time

        time.sleep(0.5)
    except Exception as e:
        raise e
        print e
        import traceback
        traceback.print_stack()


# do_login("34179765-2", "605201")