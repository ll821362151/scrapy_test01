import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class XtextSpider(CrawlSpider):
    name = 'xtext'
    allowed_domains = ['ctext.org']
    start_urls = ['https://ctext.org/zhs']

    rules = (
        Rule(LinkExtractor(allow='https://ctext.org/.*/zhs'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        book_info = response.xpath('//div[@class="text"]//div[@class="etext noprint"]//text()').getall()
        if not book_info:
            return
        book_str = ''.join(book_info).split(' -> ')
        book_str[0] = book_str[0].replace('译文对照：[不显示] [英文翻译] ', '')
        print(book_str)
        book_name = response.xpath('//div[@class="text"]//div[@id="content3"]//td[@class="ctext"]//text()').getall()
        book_content = response.xpath('//div[@class="text"]//div[@id="content3"]//table[@border="0"]//td[@class="ctext"]//text()').getall()
        print(book_content)



# def process_category(categories, path):
#     # 如果没有子目录，则返回空字典
#     if not categories:
#         return {}
#
#     # 将每个子目录的名字和对应的子目录作为键值对添加到字典中
#     result = {}
#     for name, subcategories in categories.items():
#         result[name] = process_category(subcategories, path + [name])
#
#     return result
#
# categories = {
#     '先秦两汉': {
#         '史书': {
#             '汉书': {
#                 '传': {
#                     '循吏传': {}
#                 }
#             }
#         }
#     }
# }
#
# result = process_category(categories, [])
# print(result)
# {'先秦两汉': {'史书': {'汉书': {'传': {'循吏传': {}}}}}}
