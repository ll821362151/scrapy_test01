import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from test01.items import PoemItem


class PoetryZhwSpider(CrawlSpider):
    name = 'poetry_zhw'
    allowed_domains = ['gushici.china.com']
    start_urls = ['https://gushici.china.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*://gushici.china.com/shici/0_0_.*.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        poetrys = response.xpath('//div[@class="poemAllList mt30"]/div[@class="listItem item-1pic clearfix"]')
        items = list()
        for poetry in poetrys:
            title = poetry.xpath('.//h3/a/text()').get()
            author = poetry.xpath('.//span/a/text()').get()
            dynasty = poetry.xpath('.//span[2]/text()').get()
            if dynasty is not None:
                dynasty = dynasty.split('：')[1]
            content = poetry.xpath('.//div[@class="sum"]/p/text()').getall()
            item = PoemItem()
            item['title'] = title
            item['author_name'] = author
            item['dynasty'] = dynasty
            item['author_info'] = ''
            item['content'] = ''.join(content).replace("\n", '')
            items.append(item)
        return items
