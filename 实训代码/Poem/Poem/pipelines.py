# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import jieba
from wordcloud import WordCloud


class PoemPipeline(object):
    def __init__(self):
        self.fp = None
        self.fonts_path = None
        self.wc = None
        self.pic_path = None

    def open_spider(self, spider):
        self.fp = open('data.csv', 'w+', encoding='utf-8')
        self.fonts_path = r'C:\Windows\Fonts\simhei.ttf'
        self.wc = WordCloud(font_path=self.fonts_path, width=800,
                            height=600, mode='RGB', background_color=None, collocations=False)
        self.pic_path = 'ciyun.png'

    def process_item(self, item, spider):
        row = '{author}|{name}|{poem}\n'.format_map(item)
        self.fp.writelines(row)
        return item

    def close_spider(self, spider):
        self.fp.flush()
        self.fp.seek(0, 0)
        text = self.fp.read()
        text = ' '.join(jieba.cut(text))
        self.wc.generate(text)
        self.wc.to_file(self.pic_path)

        self.fp.close()
