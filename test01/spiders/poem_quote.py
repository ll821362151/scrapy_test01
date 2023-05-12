import scrapy

from test01.items import PoemQuoteCategoryItem, PoemQuoteItem


class PoemQuoteSpider(scrapy.Spider):
    name = 'poem_quote'
    allowed_domains = ['gushicimingju.com']
    start_urls = ['https://www.gushicimingju.com']

    # rules = (
    #     Rule(LinkExtractor(allow=r'.*'), callback='parse_item', follow=True),
    # )

    def start_requests(self):
        yield scrapy.Request(method='POST', url='https://www.gushicimingju.com/shiju/', callback=self.parse_item)

    def parse_item(self, response):
        poem_quote = response.xpath(
            '//div[@class="main-content gushi-info"]//ul[@class="content-left left-4-col"]//a/text()').getall()
        items = list()
        for quote in poem_quote:
            item = PoemQuoteCategoryItem()
            item['category_name'] = quote
            items.append(item)
        return items
        # poem_quote_url = response.xpath(
        #     '//div[@class="main-content gushi-info"]//ul[@class="content-left left-4-col"]//a/@href').getall()
        # for url in poem_quote_url:
        #     current_url = 'https://www.gushicimingju.com' + url
        #     yield scrapy.Request(url=current_url, callback=self.parse_poem_quote)

    def parse_poem_quote(self, response):
        quotes = response.xpath(
            '//div[@class="main-content gushi-info"]//div[@class="good-mingju main-data mingju-list"]')
        items = list()
        for item in quotes:
            quote = PoemQuoteItem()
            quote['poem_quote'] = item.xpath('.//span[2]//a/text()').get()
            quote['poet_name'] = item.xpath('.//span[4]//a/text()').get()
            quote['poem_title'] = item.xpath('.//span[5]/a/text()').get()
            items.append(quote)
        return items
