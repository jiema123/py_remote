#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 'lijian' on 18/2/2016
import time
import threading
from selenium import webdriver
import logging


class BaseBrowser(threading.Thread):

    class Stats(object):

        def __init__(self):
            self.requests = 0
            self.responses = 0
            self.start_time = 0
            self.end_time = 0


        def tick(self, restart=False):
            if restart or not self.start_time:
                self.start_time = time.time()

            self.end_time = time.time()
            return self.end_time - self.start_time

        def reset(self):
            self.requests = 0
            self.responses = 0
            self.start_time = None
            self.end_time = None

        def used_time(self):
            return self.end_time - self.start_time if self.end_time else 0

    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.driver = None
        self.stats = None
        self.request_delay = 1

        self.logger = kwargs.get('logger', logging.getLogger('base'))
        self.driver_restart_threshhold = 5

        self.debug = self.logger.debug
        self.info = self.logger.info
        self.error = self.logger.error

    def run(self):
        '''
        请求的 4个阶段:
        1 生成request
        3 下载, (执行动作)
        4 parse
        5 save result or new reqeust
        '''
        self.initialize()
        self.do_run()
        self.finalize()

    def initialize(self):
        self.stats = BaseBrowser.Stats()
        self.stats.tick()

    def do_run(self):
        while 1:
            try:
                requests = self.next_requests()
                if not requests:
                    self.info('no more request, quit')
                    break

                driver = self.get_driver()
                for request in requests:
                    self.stats.requests += 1
                    for response in self.crawl(driver, request):
                        self.stats.responses += 1
                        self.parse(response)

                    # 每个请求间隔1s
                    driver.implicitly_wait(self.request_delay)
            except Exception as e:
                print e

    def next_requests(self):
        '''
        生成器: 返回下一批的请求
        '''
        pass

    def get_driver(self):
        '''
        初始化浏览器
        '''
        if not self.driver or self.stats.requests >= self.driver_restart_threshhold:
            if self.driver:
                self.driver.quit()

            self.driver = self.init_driver(webdriver.Firefox())
            self.info('init web driver')

        return self.driver

    def init_driver(self, driver):
        '''
        对driver进行初始化
        '''
        return driver

    def finalize(self):
        if self.driver:
            self.driver.quit()

        self.stats.tick()

    def crawl(self, driver, request):


        pass

    def parse(self, response):
        pass