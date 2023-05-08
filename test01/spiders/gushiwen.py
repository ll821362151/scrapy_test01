import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from test01.items import PoemItem


class GushiwenSpider(CrawlSpider):
    name = 'gushiwen'
    allowed_domains = ['gushiwen.cn']
    start_urls = ['https://www.gushiwen.cn/']

    rules = (
        Rule(LinkExtractor(allow='.*'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'https://so\.gushiwen\.cn/shiwenv.*\.aspx'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        current_url = response.url
        if "https://so.gushiwen.cn/shiwenv" not in current_url:
            return
        title = response.xpath('//div[@id="sonsyuanwen"]/div[@class="cont"]//h1/text()').get()
        if not title:
            return
        author_name = response.xpath(
            '//div[@id="sonsyuanwen"]/div[@class="cont"]//p[@class="source"]/a[1]/text()').get()
        dynasty = response.xpath(
            '//div[@id="sonsyuanwen"]/div[@class="cont"]//p[@class="source"]/a[2]/text()').get()
        if dynasty is not None:
            dynasty = dynasty[1:-1]
        content = response.xpath(
            '//div[@id="sonsyuanwen"]/div[@class="cont"]//div[@class="contson"]//text()').getall()
        author_info = response.xpath('//div[@class="sonspic"]/div[@class="cont"]//p[2]/text()').get()
        item = PoemItem()
        item['title'] = title
        item['author_name'] = author_name
        item['dynasty'] = dynasty
        item['author_info'] = author_info
        item['content'] = ''.join(content).replace("\n", '')
        print(item)
        return item
