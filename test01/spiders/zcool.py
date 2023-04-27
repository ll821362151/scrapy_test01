import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
import re
import os
from test01.spiders.utils.constant import Constants


class ZcoolSpider(CrawlSpider):
    name = 'zcool'
    allowed_domains = ['zcool.com.cn']
    start_urls = ['https://www.zcool.com.cn/']
    index = 0

    rules = (
        Rule(LinkExtractor(allow='https://www.zcool.com.cn/work/(.*?)'), callback='parse1', follow=True),
    )

    # def start_requests(self):
    #     splah_args = {
    #         "lua_source": """
    #         function main(splash, args)
    #           assert(splash:go(args.url))
    #           assert(splash:wait(0.5))
    #           return {
    #             html = splash:html(),
    #             png = splash:png(),
    #             har = splash:har(),
    #           }
    #         end
    #         """
    #     }
    #     headers = {
    #         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
    #                       'Chrome/72.0.3626.109 Safari/537.36',
    #     }
    #     for url in self.start_urls:
    #         print('start_urls:'+url)
    #         yield SplashRequest(url=url, callback=self.parse_item,
    #                             headers=headers,
    #                             endpoint='render.json',
    #                             args={
    #                                 'har': 1,
    #                                 'html': 1,
    #                             })

    def parse_item(self, response):
        print(response.url)
        # a_url = response.xpath('//a/@href').getall()
        # for url in a_url:
        #     print(url)
        #
        # a_url = response.xpath('//img/@src').getall()
        # for url in a_url:
        #     print(url)
        # a_url = response.xpath('//div[@class="card-img"]/a/@href').getall()
        # print("".join(a_url))
        # for url in a_url:
        #     if re.match(self.res, url):
        #         yield SplashRequest(
        #             url,
        #             self.parse_content,
        #             endpoint='render.json',
        #             args={
        #                 'har': 1,
        #                 'html': 1,
        #             }
        #         )
        # le = LinkExtractor()
        # for link in le.extract_links(response):
        #     print(link.url)
        #     if re.match(self.res, link.url):
        #         yield SplashRequest(
        #             link.url,
        #             self.parse_content,
        #             endpoint='render.json',
        #             args={
        #                 'har': 1,
        #                 'html': 1,
        #             }
        #         )

    def parse1(self, response):
        img_url = response.xpath('//div[@class="photo-information-content"]/img/@src').getall()
        title = response.xpath('//title/text()').get()
        title = title.split('|')[0]
        path = Constants.FILE_PATH + 'zcool/' + title + "/"
        self.index = 0
        if not os.path.exists(path):
            os.makedirs(path)
        for url in img_url:
            if all(('http' in url, '.svg' not in url)):
                self.index += 1
                download_header = {
                    'Referer': 'https://www.dmzj.com/view/biaoren/42109.html#@page=1'
                }
                # img_name = page.split('/')
                pic = requests.get(url, timeout=10, headers=download_header)
                # img_path = path + "/" + img_name[7]
                img_path = path + str(self.index) + ".jpg"
                print(img_path)
                fp = open(img_path, 'wb')
                fp.write(pic.content)
                fp.close()

    def parse_content(self, response):
        img_url = response.xpath('//div[@class="photo-information-content"]/img/@src').getall()
        title = response.xpath('//title/text()').get()
        for url in img_url:
            if all(('http' in url, '.svg' not in url)):
                print(url)
        # for url in img_url:
        #     self.index += 1
        #     if all(('http' in url, '.svg' not in url)):
        #         print(url)
        #         pic = requests.get(url, timeout=10)
        #         dir = 'E:/pic/' + title + "-" + str(self.index) + ".jpg"
        #         fp = open(dir, 'wb')
        #         fp.write(pic.content)
        #         fp.close()
        #     else:
        #         print("不是url地址：" + url)
