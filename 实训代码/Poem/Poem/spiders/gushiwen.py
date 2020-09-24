# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from Poem.items import PoemItem


class GushiwenSpider(scrapy.Spider):
    name = 'gushiwen'
    # allowed_domains = ['gushiwen.org']
    domains = ['so.gushiwen.org']
    start_urls = ['https://www.gushiwen.org/gushi/tangshi.aspx']

    def parse(self, response):
        pattern = '^https://so.gushiwen.org/shiwenv(.*?)'
        le = LinkExtractor(allow=pattern)
        links = le.extract_links(response)
        print(len(links))
        for i in links:
            yield scrapy.Request(i.url, callback=self.parse_content)

    def parse_content(self, response):
        item = PoemItem()
        # /html/body/div[2]/div[1]/div[2]/div[1]/h1
        item['author'] = response.xpath('/html/body/div[2]/div[1]/div[2]/div[1]/h1/text()').get()
        item['name'] = response.xpath('string(/html/body/div[2]/div[1]/div[2]/div[1]/p)').get()
        item['poem'] = response.xpath('string(//*[@class="contson"])').get().strip()
        yield item



