# -*- coding:utf-8 -*-
import time
from datetime import datetime, timedelta

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from test01.items import CctvXmlbItem


class xwlbSpider(CrawlSpider):
    # 爬虫名称
    name = 'xmlb'
    # 允许域名
    allowed_domains = ['tv.cctv.com']
    # 开始URL
    start_urls = [
        'https://tv.cctv.com/lm/xwlb/index.shtml',
    ]

    rules = (
        Rule(LinkExtractor(allow='https://tv.cctv.com/lm/xwlb/index.shtml'),
             callback='parse_item',
             follow=False),
    )

    def parse_item(self, response):
        contents = response.xpath('//div[@class="con"]//ul[@id="content"]//a/text()').getall()
        contents = [s.replace(u'[视频]', '') for s in contents]
        item = CctvXmlbItem()
        now = datetime.now() - timedelta(days=1)
        date = str(now)[:10]
        item = CctvXmlbItem()
        item['publishTime'] = date + u" 19:00:00"
        date_arr = date.split('-')
        ymd = date_arr[0] + u'年' + date_arr[1] + u"月" + date_arr[2] + u"日"
        item['source'] = u'CCTV'
        item['title'] = ymd + u" 《新闻联播》主要内容"
        item['content'] = contents
        print(item)
        return item
