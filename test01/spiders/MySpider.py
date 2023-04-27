import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest


class MySpider(scrapy.Spider):
    name = 'with_splash'
    allowed_domains = ['beqege.com']
    start_urls = ['https://www.beqege.com/']

    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse)
        yield SplashRequest(url=self.start_urls[0], callback=self.parse_splash, args={'wait': 2})

    def parse(self, response):
        print('Request', response.url)

    def parse_splash(self, response):
        print(response.xpath("//div[@id='newscontent']//li/text()").getall())
        print('SplashRequest', response.text)
        pass
