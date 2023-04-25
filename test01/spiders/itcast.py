# import logging
# import re
#
# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
#
# from test01.items import Test01Item
#
#
# class ItcastSpider(scrapy.Spider):
#     name = 'itcast'
#     allowed_domains = ['itcast.cn']
#     start_urls = ['http://www.itcast.cn/channel/teacher.shtml']
#     print("开始爬取新闻：" + str(tuple(start_urls)))
#
#     # rules = (
#     #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
#     # )
#
#     def parse(self, response):
#         print("开始啦")
#         print(response.body)
#         html = response.text
#         logging.info(html)
#         print(html)
#         reg = r'<img data-original="(.*?)">.*?<div class="li_txt">.*?<h3>(.*?)</h3>.*?<h4>(.*?)</h4>.*?<p>(.*?)</p>'
#         infos = re.findall(reg, html, re.S)
#         for img, name, grade, talk in infos:
#             item = Test01Item()
#             item['name'] = name
#             item['grade'] = grade
#             item['info'] = talk
#             item['img'] = self.allowed_domains[0] + img
#             logging.info(name+"--"+item['img'])
#             print(name+"--"+item['img'])
#             # 这里是用的yield 而不是return
#             yield item
