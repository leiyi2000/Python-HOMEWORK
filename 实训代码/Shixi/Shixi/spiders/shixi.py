# -*- coding: utf-8 -*-
import scrapy
from Shixi.items import ShixiItem


class ShixiSpider(scrapy.Spider):
    name = 'shixi'
    # allowed_domains = ['shixi.com']
    start_urls = [f'https://www.shixi.com/search/index?page={i}' for i in range(1, 10)]
    domains = 'https://www.shixi.com'

    def parse(self, response):
        item = ShixiItem()
        for job in response.xpath('//*[@class="job-pannel-list"]'):
            # //*[@id="select-form"]/div[2]/div/div[5]
            item['date'] = job.xpath('.//*[@class="job-time"]/text()').extract_first().strip()
            item['company'] = job.xpath('.//*[@class="company-info-title"]/a/text()').extract_first().strip()
            item['job_name'] = job.xpath('.//*[@class="job-name"]/text()').extract_first().strip()
            dp_url = job.xpath('.//*[@class="job-name"]/@href').extract_first().strip()
            item['money'] = job.xpath('.//*[@class="company-info-des"]/text()').extract_first().strip().replace(" ", '')
            item['education'] = job.xpath('.//*[@class="job-educational"]/text()').extract_first().strip()
            # print(item)

            if dp_url:
                yield scrapy.Request(self.domains + dp_url, callback=self.parse_get_desc, meta={'item': item})

    def parse_get_desc(self, response):
        item = response.meta.get('item', {})
        item['desc'] = response.xpath('string(/html/body/div/div[3]/div[1]/div[3]/div[2])').get(). \
            strip().replace('\r', '\n')
        yield item
