
import scrapy
import logging

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class MySpider(CrawlSpider):
    name = 'test'
    # allowed_domains = ['people.com.cn/']
    # start_urls = ['http://www.people.com.cn/GB/59476/index.html']
    #
    # rules = (
    #     Rule(LinkExtractor(allow=''), callback='parse_content', follow=True),
    # )
    #
    # def parse_content(self, response):
    #     url = response.url
    #     print(url)
    #     index = response.meta['index']
    #     title = response.xpath(
    #         '/html/body/div[2]/div/div[1]/div[2]/text()').extract()[0].replace(' ', '')
    #     sourceStr = response.xpath('//div[@class="wzy_zzly"]/p').extract()[0]
    #     print(sourceStr)
    #     publish_time = sourceStr[sourceStr.rfind(u']')+1:sourceStr.find('</p>')].replace(u'', '').strip()
    #     self.log(publish_time)

    allowed_domains = ['people.com.cn']
    start_urls = ['http://www.people.com.cn/GB/59476/index.html']

    # rules = (
    #     Rule(LinkExtractor(allow='(.*?).people.com.cn/n1/\d{4}/\d{4}/(.*?)'),  callback='parse_item', follow=False),
    #     # Rule(LinkExtractor(allow='http://(.*?).people.com.cn/n1/(.*?)'), callback='parse_item', follow=False),
    # )

    # def make_requests_from_url(self, url):
    #     return Request(url, dont_filter=True, meta=start_urls)
    def parse(self, response):
        title = response.xpath('//li/a/text()').getall()
        print(title)

    # def parse_item(self, response):
    #     print(response.xpath('//title/text()').getall())
    #     # print(response.xpath('//td[@class="p6"]/li').getall())
    #     # print(response.text)
    #     # lis = response.xpath('//tbody//a/text()').getall()
    #     # print(lis)
    #     pass
