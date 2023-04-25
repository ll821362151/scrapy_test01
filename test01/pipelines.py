# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

from test01.items import Test01Item, MycwpijItem


class Test01Pipeline:
    # 初始化的操作，这里我们做本地化直接写成文件，所以初始化文件对象
    def __init__(self):
        print('实例化DemoPipeline')
        # self.f = open('itcast_pipeline.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # if isinstance(item, Test01Item):
        #     content = json.dumps(dict(item), ensure_ascii=False)
        #     self.f.write(content+",")
        #     print(content)
        # elif isinstance(item, MycwpijItem):
        #     print(item['name'])
        #     print(item['title'])
        return item

    # 结束后做的操作，在这里我们要关闭文件
    def close_spider(self, spider):
        print('结束')
        # self.f.close()

