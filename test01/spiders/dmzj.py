from contextlib import closing

import requests
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from scrapy_splash import SplashRequest
import os

class DmzjSpider(CrawlSpider):
    name = 'dmzj'
    allowed_domains = ['dmzj.com']
    start_urls = ['https://www.dmzj.com/info/chuanyuexiaoying.html']

    rules = (
        Rule(LinkExtractor(allow=''), callback='parse_item', follow=False),
    )

    res = 'https://www.dmzj.com/view/chuanyuexiaoying/(.*?)'
    title = ''


    def parse_item(self, response):
        # print(response.url)
        zj_list_url = response.xpath('//div[@class="tab-content tab-content-selected zj_list_con autoHeight"]/ul[@class="list_con_li autoHeight"]/li/a')
        if zj_list_url:
            for item in zj_list_url:
                url = item.xpath('@href').get()
                title = item.xpath('@title').get()
                if re.match(self.res, url):
                    next_page = url+"#@page=1"
                    print(title + '\t' + next_page+"\t")
                    add_params={}
                    add_params['title'] = title
                    yield SplashRequest(
                        next_page,
                        self.parse_content,
                        endpoint='render.json',
                        args={
                            'har': 1,
                            'html': 1,
                        },
                        cb_kwargs=add_params
                    )

    def parse_content(self, response, title):
        # print(title)
        pages = response.xpath('//select[@id="page_select"]/option/@value').getall()
        path = 'E:/漫画/穿越效应/' + title.split(' ')[0]
        is_exist = os.path.exists(path)
        index = 0
        if not is_exist:
            os.makedirs(path)
        for page in pages:
            index += 1
            download_header = {
                'Referer': 'https://www.dmzj.com/view/biaoren/42109.html#@page=1'
            }
            # img_name = page.split('/')
            pic = requests.get(page, timeout=10, headers=download_header)
            # img_path = path + "/" + img_name[7]
            img_path = path + "/" + str(index) + ".jpg"
            print(img_path)
            fp = open(img_path, 'wb')
            fp.write(pic.content)
            fp.close()

