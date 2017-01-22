# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DoubanItem(Item):
    # define the fields for your item here like:
    movie_name = Field()
    comment = Field()
    star = Field()
    commenter = Field()
    comment_time = Field()

