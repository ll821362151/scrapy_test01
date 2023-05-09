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


class BookInfoItem(scrapy.Item):
    book_id = scrapy.Field()
    parent_id = scrapy.Field()
    book_name = scrapy.Field()
    author = scrapy.Field()
    dynasty = scrapy.Field()
    description = scrapy.Field()
    update_time = scrapy.Field()


class ChapterContentItem(scrapy.Item):
    content_id = scrapy.Field()
    chapter_id = scrapy.Field()
    content = scrapy.Field()
    info = scrapy.Field()


class ChapterInfoItem(scrapy.Item):
    chapter_id = scrapy.Field()
    book_id = scrapy.Field()
    chapter_name = scrapy.Field()
    chapter_num = scrapy.Field()
    update_time = scrapy.Field()


class CtextBookItem(scrapy.Item):
    book_category_info = scrapy.Field()
    book_content = scrapy.Field()
    book_name = scrapy.Field()


class PoetAuthorItem(scrapy.Item):
    a_name = scrapy.Field()
    a_dynasty = scrapy.Field()
    a_remark = scrapy.Field()


class PoetCategoryItem(scrapy.Item):
    category_name = scrapy.Field()
    poets_name = scrapy.Field()
    poets_number = scrapy.Field()
    poets_remark = scrapy.Field()
