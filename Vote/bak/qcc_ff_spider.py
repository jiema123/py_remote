#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 'lijian' on 2/24/16


from spiders.browser import BaseBrowser
from spiders.company_info_dao import CompanyInfoDao, ParsedData

from scrapy.http import Request
from scrapy.http import HtmlResponse

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.unicodeutil import remove_punctuation


class QccFFSpider(BaseBrowser):

    def __init__(self, **kwargs):
        super(QccFFSpider, self).__init__()

        mysql_config = kwargs['mysql_config']
        start = kwargs.pop('start', 0)
        end = kwargs.pop('end', 100000)
        self.dao = CompanyInfoDao(mysql_config, start, end)
        self.dao.connect_mysql()

    def next_requests(self):
        result = []
        companys = self.dao.get_companys()
        for company in companys:
            ref_id = company['id']
            name = company['name']

            result.append(Request('http://qichacha.com/search?key=adfa&index=0', meta={'ref_id': ref_id, 'name': name}))

        return result

    def init_driver(self, driver):
        '''
        对driver进行初始化
        '''
        driver.get('http://qichacha.com/404')
        driver.add_cookie({'name': 'CNZZDATA1254842228', 'value':"1423021271-1456013503-|1456013503", 'path': '/' })
        driver.add_cookie({'name': 'PHPSESSID', 'value': 'csfa54g63pp96tul2jiblcd9c6', 'path': '/'})
        driver.add_cookie({'name': 'SERVERID', 'value': 'b7e4e7feacd29b9704e39cfdfe62aefc|1456018741|1456018083', 'path': '/'})
        driver.add_cookie({'name': 'pspt', 'value': '{"id":"792838","pswd":"8835d2c1351d221b4ab016fbf9e8253f","_code":"db73829e0ece255de0eab4947383b544"}', 'path': '/'})
        driver.add_cookie({'name': 'think_language', 'value': 'zh-cn', 'path': '/'})
        self.info('set qichacha cookies')

        driver.get('http://qichacha.com/search?key=adfa&index=0')
        return driver

    def crawl(self, driver, request):

        def element_exists(css_path):
            return len(driver.find_elements(By.CSS_SELECTOR, css_path)) != 0

        company_name = request.meta['name']
        ref_id = request.meta['ref_id']

        b = u'建行电话宝'
        if company_name.startswith(b):
            company_name = company_name.replace(b, '')

        # result = []
        # 输入框
        driver.implicitly_wait(1)
        driver.find_element(By.CSS_SELECTOR, 'div.input-group input.form-control').clear()
        driver.find_element(By.CSS_SELECTOR, 'div.input-group input.form-control').send_keys(company_name)
        # 搜索按钮
        driver.find_element(By.CSS_SELECTOR, 'span.input-group-btn button.btn').click()

        # 无结果
        if element_exists('div.noresult'):
            self.debug('%s, %s, nothing found', ref_id, company_name)
            yield HtmlResponse('', body='', request=request, status=401)
        else:
            items = driver.find_elements(By.CSS_SELECTOR, 'div.col-md-9 a.list-group-item')
            if items:
                self.debug('%s, %s, found %d result', ref_id, company_name, len(items))
                home_handle = driver.current_window_handle
                for i in range(len(items)):
                    try:
                        if i > 0:
                            driver.implicitly_wait(1)

                        # 点击链接
                        driver.find_elements(By.CSS_SELECTOR, 'div.col-md-9 a.list-group-item')[i].click()

                        # 切换到新tab页面
                        last_handle = driver.window_handles[-1]
                        driver.switch_to_window(last_handle)

                        try:
                            WebDriverWait(driver, 9).until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.panel.base_info")))
                        except TimeoutException:
                            self.debug('page load timeout')

                        #code to do something on new window  section.panel.base_info div.panel-body ul li
                        html = driver.page_source
                        url = driver.current_url.encode('utf8').strip()
                        yield HtmlResponse(url, body=html, request=request, encoding='utf-8')

                        #关闭当前窗口
                        driver.close()

                        switched = driver.switch_to_window(home_handle)
                    except Exception as e:
                        import traceback
                        traceback.print_stack()
                        self.error(e)

    def parse(self, response):

        def norm_value(text):
            return remove_punctuation(text).encode('utf8').strip()

        request = response.request
        ref_id = request.meta['ref_id']
        company_name = request.meta['name']

        if response.status == 401:
            self.debug('%s, %s, parsed 0 result', ref_id, company_name)
            self.dao.save_company_info(ref_id)
            return

        # response =HtmlResponse(url, body=page_source, encoding='utf-8', headers={})
        try:
            title_ele = response.css('span.text-big').xpath('.//text()').extract()
            if not title_ele or len(title_ele) == 0:
                self.debug('empty record')
                return

            struct_data = {
                '企业名称' : title_ele[0].encode('utf8')
            }

            for fs in response.css('section.panel.base_info div.panel-body ul li'):
                items = fs.xpath(".//text()").extract()

                name = norm_value(fs.xpath('label//text()').extract()[0])
                value = ''.join([norm_value(m) for m in items])[len(name):]
                struct_data[name] = value

            parsed_data = ParsedData(ref_id, response.url, response.body, struct_data)
            self.dao.save_company_info(ref_id, [parsed_data])
        except Exception as e:
            self.error(e)