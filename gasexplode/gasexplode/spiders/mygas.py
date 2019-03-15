# -*- coding: utf-8 -*-
import scrapy
from gasexplode.items import GasexplodeItem

import json

class MygasSpider(scrapy.Spider):
    name = 'mygas'
    year,month='2019','3'
    allowed_domains = ['gasexplode.mygas.cn']
    start_urls = ['http://gasexplode.mygas.cn/html/News.html?selectYear='+year+'&selectMonth='+month+'&contentType=99&count=31&offset=0']

    def parse(self, response):
        self.logger.debug(response.text)
        if json.get('articles'):
            for article in json.get('articles'):
                item=GasexplodeItem()
                item['title']=article.get('TITLE')
                item['time']=article.get('UPDATE_TIME')
                item['content']=article.get('CONTENT')
                yield item

