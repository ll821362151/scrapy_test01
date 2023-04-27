import os

import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from test01.spiders.utils.constant import Constants


class SiweiSpider(CrawlSpider):
    name = 'siwei'
    allowed_domains = ['sw.ateen.cn']
    start_urls = ['http://sw.ateen.cn/']

    rules = (
        Rule(LinkExtractor(allow=''), callback='parse_network', follow=True),
    )
    index = 0

    img_list = []

    def parse_item(self, response):
        print(response.url)
        pages = response.xpath('//img/@src').getall()

        path = Constants.FILE_PATH.join('siwei')
        print(path)
        is_exist = os.path.exists(path)
        if not is_exist:
            os.makedirs(path)
        for page in pages:
            if 'http://' not in page:
                page = 'http://sw.ateen.cn' + page
            print(page)
            if page not in self.img_list:
                self.img_list.append(page)
                self.index += 1
                download_header = {
                    'Referer': 'http://sw.ateen.cn/'
                }
                # img_name = page.split('/')
                pic = requests.get(page, timeout=10, headers=download_header)
                # img_path = path + "/" + img_name[7]
                img_path = path + "/" + str(self.index) + ".png"
                print(img_path)
                fp = open(img_path, 'wb')
                fp.write(pic.content)
                fp.close()

    def parse_network(self, response):
        path = Constants.FILE_PATH + ('siwei/html/')
        is_exist = os.path.exists(path)
        print(path)
        content = response.text
        if not is_exist:
            os.makedirs(path)
        title = response.url.split('http://sw.ateen.cn/')[1]
        if not title:
            title = response.url
        print(title)
        fp = open(path + title, 'w', encoding='utf-8')
        fp.write(content)
        fp.close()
