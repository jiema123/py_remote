#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 'lijian' on 5/7/16


'''
Request URL:http://vote.ecloud-zj.com/enterprises/Register
Request Method:POST
Status Code:302 Found
Remote Address:120.55.91.150:80

Headers
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding:gzip, deflate
Accept-Language:en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2
Cache-Control:no-cache
Connection:keep-alive
Content-Length:246
Content-Type:application/x-www-form-urlencoded
Cookie:.AspNet.Session=5da93942-5b7d-5bfd-6728-f4829af7eb71; VHmhdJ4h8LI=CfDJ8CP6XJf5PcpElNQC-Y-J2y7qDp9vwcsK_FlStHPunUUoYUbr5fb5vflMKoHpt9m2m4eJV4VQHJX0XzD1TKAEcaHA2Fq0ROM2-noBuXs824psuyaEkvzrM3x6yl8z4gn9uEA-eC0S61Een1M2y6Xm3AQ
Host:vote.ecloud-zj.com
Origin:http://vote.ecloud-zj.com
Pragma:no-cache
Referer:http://vote.ecloud-zj.com/enterprises/Register
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36
X-Wap-Profile:http://wap1.huawei.com/uaprof/HW_HUAWEI_P6-C00_1_20130425.xml

Form Data
name:我哈哈
codeCertificate:12345678
address:
enterpriseCustomCode:
email:demo@163.com
generalManager:王某某
managerTel:13878654567
ParentAID:914
ParentBID:915
Password:12345678
ConfirmPassword:12345678
'''
import urllib
import urllib2

def do_register(companyName, companyCode):
    #定义一个要提交的数据数组(字典)
    data = {}
    data['name'] = companyName
    data['codeCertificate'] = companyCode
    data['address'] = ''
    data['enterpriseCustomCode'] = ''
    data['email'] = 'test@163.com'
    data['generalManager'] = "王大锤"
    data['managerTel'] = '13267578970'

    data['ParentAID'] = 914
    data['ParentBID'] = 915

    data['Password'] = '12345678'
    data['ConfirmPassword'] = '12345678'

    #定义post的地址
    url = 'http://vote.ecloud-zj.com/enterprises/Register'
    post_data = urllib.urlencode(data)

    #提交，发送数据
    req = urllib2.urlopen(url, post_data)

    #获取提交后返回的信息  '<script type="text/javascript"> alert(\\'组织机构代码已经存在\\');javascript:history.go(-1);</script>'
    content = req.read()
    print content

do_register("山水海乐", "W15722321")