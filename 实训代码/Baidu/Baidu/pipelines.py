# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class BaiduPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(spider.settings.get("MONGODB_HOST", 'mongodb://localhost:27017/'))
        self.db = self.client[spider.settings.get("MONGODB_DB_NAME", 'test')]
        self.sheet = self.db[spider.settings.get("MONGODB_SHEET_NAME", 'ly')]

    def process_item(self, item, spider):
        self.sheet.insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()

