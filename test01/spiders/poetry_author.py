import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from test01.items import PoetAuthorItem

"""
zhw 古诗词作者信息
"""


class PoetryAuthorSpider(CrawlSpider):
    name = 'poetry_author'
    allowed_domains = ['gushici.china.com']
    start_urls = ['https://gushici.china.com/shiren/']

    rules = (
        Rule(LinkExtractor(allow=r'.*://gushici.china.com/shiren/.*/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
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
        item['a_remark'] = ''.join(remark)
        print(item)
        return item
