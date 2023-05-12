import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from test01.items import PoetCategoryItem

'''诗人组合称呼'''


class PoetTitleSpider(scrapy.Spider):
    name = 'poet_title'
    allowed_domains = ['gushici.china.com/hecheng']
    start_urls = ['https://gushici.china.com/']

    # rules = (
    #     Rule(LinkExtractor(allow=r'.*://gushici.china.com/hecheng/.*html'), callback='parse_item', follow=True),
    # )

    def start_requests(self):
        for i in range(0, 1000):
            url = "https://gushici.china.com/hecheng/{}.html".format(i)
            yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        poet_category = response.xpath('//div[@class="group-row"]//div[@class="gr-value category"]//a/text()').getall()
        poets_name = response.xpath('//div[@class="mod corner"]//div[@class="poetGroup mt30"]/h3/text()').get()
        poets_remark = response.xpath('//div[@class="mod corner"]//div[@class="poetGroup mt30"]/p/text()').get()
        poets_remark = poets_remark.replace('…', '')
        poets_number = response.xpath('//div[@class="poetAllList mt30"]//div[@class="listItem item-1pic clearfix"]//'
                                      'h3[@class="tit"]/a/text()').getall()
        item = PoetCategoryItem()
        item['category_name'] = poet_category
        item['poets_name'] = poets_name
        item['poets_number'] = ','.join(poets_number)
        item['poets_remark'] = poets_remark
        print(item)
        return item
