# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from scrapy import signals
from logging import getLogger
from scrapy.http import HtmlResponse


class SeleniumLogin(object):
    def __init__(self, driver_path=None, timeout=None, account=None):
        self.account = account
        self.timeout = timeout
        self.driver_path = driver_path
        self.driver = webdriver.Chrome(self.driver_path)
        self.wait = WebDriverWait(self.driver, timeout)
        self.logger = getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(driver_path=crawler.settings.get("DRIVER_PATH"),
                   timeout=crawler.settings.get("SELENIUM_TIMEOUT"),
                   account=crawler.settings.get("ACCOUNT"))

    def __del__(self):
        self.driver.quit()

    def process_request(self, request, spider):
        meta = request.meta
        if meta.get("middlewares", None) == 'SeleniumLogin':
            try:
                self.driver.get(request.url)
                by_way = self.wait.until(lambda x: x.find_element_by_xpath('//*[@id="account"]/div[2]/div[2]/div/div['
                                                                           '1]/ul[1]/li[2]'))
                by_way.click()
                input_user_name = self.driver.find_element_by_id('username')
                input_user_name.send_keys(self.account.get('user', ''))
                input_user_password = self.driver.find_element_by_id('password')
                input_user_password.send_keys(self.account.get('password', ''))

                self.driver.find_element_by_xpath('//*[@id="account"]/div[2]/div[2]/div/div[2]/div[1]/div[4]').click()
                # 链接跳转
                self.wait.until(lambda x: x.current_url != request.url)
                # 深度复制cookie
                cookie = {}
                for i in self.driver.get_cookies():
                    cookie[i['name']] = i['value']
                # 添加cookie
                request.meta['cookie'] = cookie
                return HtmlResponse(url=request.url, status=200, request=request, body=self.driver.page_source,
                                    encoding='utf-8')
            except TimeoutException:
                return HtmlResponse(url=request.url, status=500, request=request)
            finally:
                self.driver.close()


class MoviecommentsSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MoviecommentsDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
