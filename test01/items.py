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


class AuthorItem(scrapy.Item):
    id = scrapy.Field()
    a_name = scrapy.Field()
    a_dynasty = scrapy.Field()
    a_deathtime = scrapy.Field()
    a_birthday = scrapy.Field()
    a_remark = scrapy.Field()
    oper_time = scrapy.Field()


class PoemItem(scrapy.Item):
    id = scrapy.Field()
    author_name = scrapy.Field()
    author_info = scrapy.Field()
    title = scrapy.Field()
    dynasty = scrapy.Field()
    content = scrapy.Field()
    translation_content = scrapy.Field()
    create_time = scrapy.Field()
    remark = scrapy.Field()
    oper_time = scrapy.Field()
