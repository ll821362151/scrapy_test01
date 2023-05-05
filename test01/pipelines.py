# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time
import uuid
from datetime import datetime

import pymysql
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


class MySQLPipeline(object):

    def __init__(self, mysql_host, mysql_port, mysql_user, mysql_password, mysql_dbname):
        self.mysql_host = mysql_host
        self.mysql_port = mysql_port
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_dbname = mysql_dbname

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_port=crawler.settings.get('MYSQL_PORT'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
            mysql_dbname=crawler.settings.get('MYSQL_DBNAME')
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            password=self.mysql_password,
            db=self.mysql_dbname,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        # 执行SQL语句将数据存储到MySQL数据库中
        with self.conn.cursor() as cursor:
            author_name = item['author_name']
            if author_name is not None:
                select_author = 'select id from s_author where a_name=%s'
                cursor.execute(select_author, item['author_name'])
                author_result = cursor.fetchone()
                if author_result is None:
                    author_params = (
                        uuid.uuid4(), author_name, item['dynasty'], item['author_info'], datetime.now())
                    insert_author = 'insert into s_author(id,a_name,a_dynasty,a_remark,oper_time) values (%s,%s,%s,%s,%s)'
                    cursor.execute(insert_author, author_params)
            select_poem = 'select id from s_poem where title=%s'
            cursor.execute(select_poem, item['title'])
            poem_result = cursor.fetchone()
            if poem_result is None:
                insert_poem = 'insert into s_poem(id,author_name,title,content,oper_time) values (%s,%s,%s,%s,%s)'
                poem_params = (uuid.uuid4(), author_name, item['title'], item['content'], datetime.now())
                cursor.execute(insert_poem, poem_params)
                print(item['title'])
            self.conn.commit()
        return item
