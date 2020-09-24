# -*- coding: utf-8 -*-
import scrapy


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    # allowed_domains = ['movie.douban.com']
    login_url = 'https://www.douban.com/'
    login_post_url = "https://accounts.douban.com/j/mobile/login/basic"
    comments_url = 'https://movie.douban.com/subject/26266893/comments'

    def start_requests(self):
        yield scrapy.Request(url=self.login_url, callback=self.login_requests)

    def login_requests(self, response):
        form_data = {
            'ck': '',
            'name': '17338357023',
            'password': '110and119',
            'remember': 'false',
            'ticket': ''
        }

        yield scrapy.FormRequest(url=self.login_post_url, callback=self.verify_login, formdata=form_data)

    def verify_login(self, response):
        assert 'success' in response.text
        yield scrapy.Request(url=self.comments_url, callback=self.parse)

    def parse(self, response):
        pass


