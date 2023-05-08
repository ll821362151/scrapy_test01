import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from test01.items import BookInfoItem, ChapterInfoItem, ChapterContentItem


class GuwenSpider(CrawlSpider):
    name = 'guwen'
    allowed_domains = ['gushiwen.cn']
    start_urls = ['https://so.gushiwen.cn/guwen/']

    rules = (
        Rule(LinkExtractor(allow='.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        url = response.url
        if 'https://so.gushiwen.cn/guwen/bookv_' in url:
            title = response.xpath('//head/title/text()').get().replace("\n", '')
            title = title.split('_')
            content = response.xpath('//div[@class="left"]/div[@class="sons"]//div[@class="contson"]//text()').getall()
            item = ChapterContentItem()
            item['content'] = ''.join(content).replace("\n", '')
            item['info'] = title[0]
            return item
        elif 'https://so.gushiwen.cn/guwen/book_' in url:
            title = response.xpath('//div[@id="sonsyuanwen"]/div[@class="cont"]/h1//text()').getall()
            if title is None:
                return
            description = response.xpath('//div[@id="sonsyuanwen"]/div[@class="cont"]/p//text()').getall()
            item = BookInfoItem()
            item['book_name'] = "".join(title).replace("\n", '')
            item['description'] = ''.join(description).replace("\n", '')
            return item
