# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from urllib.request import urlopen
from urllib.request import ProxyHandler
from urllib.request import build_opener
from urllib.request import install_opener
import requests


class ProxyPipeline(object):

    # url = 'https://movie.douban.com/subject/26879060/comments?start=0&limit=20&sort=new_score&status=P'
    url = 'https://www.baidu.com'

    def process_item(self, item, spider):
        ip = item['ip']
        port = item['port']
        proxy = ip + ":" + port
        proxy_host = ProxyHandler({'http': 'http://' + proxy})
        opener = build_opener(proxy_host)
        install_opener(opener)

        response = urlopen(self.url)
        # proxies = {'http': proxy}
        # response = requests.get(self.url, proxies=proxies)
        if response.getcode() != 200:
            print('bad proxy', response.read().decode('utf-8'))
            pass
        else:
            print('good proxy' + response.read().decode('utf-8'))
        return item
