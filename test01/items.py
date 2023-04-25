# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Test01Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    grade = scrapy.Field()
    info = scrapy.Field()
    img = scrapy.Field()
    pass


class MycwpijItem(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()


class CctvXmlbItem(scrapy.Item):
    title = scrapy.Field()
    source = scrapy.Field()
    publishTime = scrapy.Field()
    content = scrapy.Field()
