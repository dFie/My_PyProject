# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class DushspiderPipeline(object):
    def process_item(self, item, spider):   # 中间
        self.jsonfile.write(json.dumps(dict(item)) + ',\n')
        return item

    def open_spider(self, spider):  # 开始
        filename = 'f:/books.json'
        self.jsonfile = open(filename, 'w')
        self.jsonfile.write('[\n')

    def close_spider(self, spider): # 结束
        if self.jsonfile:
            self.jsonfile.write(']')
            self.jsonfile.close()
