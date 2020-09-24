# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviecommentsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_name = scrapy.Field()
    is_see = scrapy.Field()
    comments_time = scrapy.Field()
    comments_num = scrapy.Field()
    comments = scrapy.Field()
    location = scrapy.Field()
    reg_time = scrapy.Field()
