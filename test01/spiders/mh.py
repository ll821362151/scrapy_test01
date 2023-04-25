import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest


class MhSpider(CrawlSpider):
    name = 'mh'
    allowed_domains = ['05mh.com']
    start_urls = ['https://www.05mh.com/comic/105/']

    index = 0

    # rules = (
    #     Rule(LinkExtractor(allow=''), callback='parse_item', follow=False),
    # )

    def parse(self, response):
        le = LinkExtractor()
        for link in le.extract_links(response):
            yield SplashRequest(
                link.url,
                self.parse_link,
                endpoint='render.json',
                args={
                    'har': 1,
                    'html': 1,
                }
            )
        # print(response.url)

    def parse_link(self, response):
        self.index += 1
        print(str(self.index)+"\t\t\t"+response.url)
        img_url = response.xpath('//img[@class="bg"]/@src').get()
        # img_url = response.xpath('//img[@class="bg lazy"]/@data-original').get()
        print("图片地址："+img_url)
        if all(("https://www.05mh.com" not in img_url, 'space.gif' not in img_url)):
            img_url = "https://www.05mh.com"+img_url
            pic = requests.get(img_url, timeout=10)
            dir = 'E:/pic/' + str(self.index) + ".jpg"
            fp = open(dir, 'wb')
            fp.write(pic.content)
            fp.close()
