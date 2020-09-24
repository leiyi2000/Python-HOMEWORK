# -*- coding: utf-8 -*-
import scrapy
from Baidu.items import BaiduItem


class BaiduspiderSpider(scrapy.Spider):
    name = 'baiduspider'
    #   allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def __init__(self):
        super(BaiduspiderSpider, self).__init__()

    def start_requests(self):
        for i in self.start_urls:
            yield scrapy.Request(url=i, callback=self.parse, meta={'keys': self.settings.get("KEYWORD", ''),
                                                                   'middlewares': 'SeleniumMiddleware'})

    def parse(self, response):
        item = BaiduItem()
        # 解析
        for i in response.xpath("//h3"):
            item['url'] = i.xpath('a/@href').get()
            print(item['url'])
            item['title'] = i.xpath('string(.)').get().strip()
            print(item['title'])

            yield item

        url = response.meta.get('next_url', '')

        if url:
            yield scrapy.Request(url, callback=self.parse, meta={'middlewares': 'SeleniumNext'})






