# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem


class TutorialPipeline(object):
    # put all words in lowercase
    words_to_filter = ['politics', 'religion']

    def process_item(self, item, spider):
        print('@@@@@@@@', item)
        return item
        # for word in self.words_to_filter:
        #     if word in str(item['description']).lower():
        #         raise DropItem("Contains forbidden word: %s" % word)
        # else:
        #     print('***********', item)
        #     return item
