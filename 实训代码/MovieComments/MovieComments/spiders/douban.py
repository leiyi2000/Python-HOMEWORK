# -*- coding: utf-8 -*-
import scrapy
from MovieComments.items import MoviecommentsItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    login_url = 'https://accounts.douban.com/passport/login'
    comment_url = 'https://movie.douban.com/subject/26266893/comments'

    def __init__(self):
        super(DoubanSpider, self).__init__()
        self.cookie = None

    def start_requests(self):
        yield scrapy.Request(url=self.login_url, callback=self.login_parse,
                             meta={'middlewares': 'SeleniumLogin'})

    def login_parse(self, response):
        self.cookie = response.meta.get('cookie', '')
        yield scrapy.Request(url=self.comment_url, cookies=self.cookie, callback=self.parse)

    def parse(self, response):

        for i in response.xpath('//*[@class="comment"]'):
            item = MoviecommentsItem()
            dp_url = i.xpath('./h3/span[2]/a/@href').get()
            item['is_see'] = i.xpath('./h3/span[2]/span[1]/text()').get()
            item['user_name'] = i.xpath('./h3/span[2]/a/text()').get()
            item['comments_time'] = i.xpath('./h3/span[2]/span[last()]/@title').get()
            item['comments_num'] = i.xpath('./h3/span[1]/span/text()').get()
            item['comments'] = i.xpath('./p/span/text()').get()
            if dp_url:
                yield scrapy.Request(url=dp_url, cookies=self.cookie,
                                     callback=self.parse_space, meta={'item': item})
        # //*[@id="paginator"]/a
        next_page = response.xpath('//*[@id="paginator"]/a[last()]/@href').get()

        if next_page:
            yield scrapy.Request(url=self.comment_url + next_page, callback=self.parse, cookies=self.cookie)

    def parse_space(self, response):
        item = response.meta.get('item', {})
        item['location'] = response.xpath('//*[@id="profile"]/div/div[2]/div[1]/div/a/text()').get()
        item['reg_time'] = response.xpath('string(//*[@id="profile"]/div/div[2]/div[1]/div/div)').get()[-12:]

        yield item
