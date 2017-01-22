# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql
from .settings import MYSQL_DBNAME
from .settings import MYSQL_HOST
from .settings import MYSQL_PASSWORD
from .settings import MYSQL_USER

class WriteToMySqlPipeline(object):

    def __init__(self):
        self.file = open('review.json', 'w')
        self.db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME)
        self.cursor = self.db.cursor()

    # def open_spider(self, spider):
    #     self.file = open('items.jl', 'wb')
    #
    # def close_spider(self, spider):
    #     self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def write_myql(self, item):
        pass


