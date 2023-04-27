from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest


class BeqegeSpider(CrawlSpider):
    name = 'beqege'
    allowed_domains = ['beqege.com']
    start_urls = ['https://www.beqege.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print('parse_item start')
        yield SplashRequest(response.url, self.parse_content, args={'wait': 0.5}, headers={
            'authority': 'www.beqege.com',
            'method': 'GET',
            'path': '/',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58'
        })


    def parse_content(self, response):
        print(response.text)
