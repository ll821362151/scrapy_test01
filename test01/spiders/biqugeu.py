import io
import os.path

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from test01.spiders.utils.constant import Constants


class BiqugeuSpider(CrawlSpider):
    name = 'biqugeu2'
    allowed_domains = ['biqugeu.net']
    start_urls = ['https://www.biqugeu.net']

    rules = (
        Rule(LinkExtractor(allow=''), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        book_name = response.xpath("//div[@class='book reader']/div[@class='path']/div[@class='p']/a[2]/text()").get()
        if not book_name:
            return
        file_path = Constants.FILE_PATH + 'biquge' + os.path.sep + book_name
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        chapter_name = response.xpath("//div[@class='book reader']/div[@class='content']/h1/text()").get()
        chapter_path = file_path + os.path.sep + chapter_name + '.txt'
        if not os.path.exists(chapter_path):
            print(chapter_path)
            with open(chapter_path, "w") as file:
                chapter_content = response.xpath(
                    "//div[@class='book reader']/div[@class='content']/div[@id='content']/text()").getall()
                content_str = ''.join(chapter_content).replace('\xa0', ' ')
                file.write(content_str)
