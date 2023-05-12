import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from test01.items import PoetAuthorItem


class PoetryAuthorSpider(scrapy.Spider):
    name = 'poetry_author'
    allowed_domains = ['gushici.china.com']
    start_urls = ['https://gushici.china.com/']

    # rules = (
    # Rule(LinkExtractor(allow='.*://gushici.china.com/shiren/(0_0_\d+.html|\d+/)$'), callback='parse_item',
    #      follow=True),
    # )

    def start_requests(self):
        for i in range(13000, 30000):
            url = "https://gushici.china.com/shiren/{}/".format(i)
            yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        poet_url = re.compile(r'.*://gushici.china.com/shiren/\d+/$')
        current_url = response.url
        if poet_url.search(current_url):
            print(response.url)
        else:
            return
        poetry_remark = response.xpath('//div[@class="side-mod poetCard"]//div[@class="side-bd"]')
        if not poetry_remark:
            return
        item = PoetAuthorItem()
        item['a_name'] = poetry_remark.xpath('.//div[@class="info"]/h3/a/text()').get()
        dynasty = poetry_remark.xpath('.//div[@class="info"]/p/text()').get()
        if dynasty:
            dynasty = dynasty.split("：")[1]
        item['a_dynasty'] = dynasty
        remark = poetry_remark.xpath('.//div[@id="js-poetSum"]//p/text()').getall()
        if remark is None:
            item['a_remark'] = ''
            return
        remark_str = ''.join(remark)
        if len(remark_str) < 10:
            return
        item['a_remark'] = ''.join(remark)
        return item
