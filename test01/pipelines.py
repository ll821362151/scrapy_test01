import uuid
from datetime import datetime

import pymysql


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
        item_name = type(item).__name__
        switcher = {
            'PoemItem': self.handle_item_poem,
            'ChapterContentItem': self.handle_item_chapter_content,
            'BookInfoItem': self.handle_item_book_info
        }
        if item_name == 'PoemItem':
            return self.handle_item_poem(item)
        elif item_name == 'ChapterContentItem':
            return self.handle_item_chapter_content(item)
        elif item_name == 'BookInfoItem':
            return self.handle_item_book_info(item)

    def handle_item_poem(self, item):
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

    def handle_item_chapter_content(self, item):
        with self.conn.cursor() as cursor:
            content = item['content']
            title_info = item['info']
            titles = title_info.split('·')
            title_size = len(titles)
            book_name = titles[0]
            book_sql = 'select book_id,parent_id from book_info where book_name=%s'
            cursor.execute(book_sql, book_name)
            book_result = cursor.fetchone()
            if book_result is None:
                book_uuid = uuid.uuid4()
                insert_book = 'insert into book_info (book_id,book_name,update_time) values (%s,%s,%s)'
                insert_book_params = (book_uuid, book_name, datetime.now())
                cursor.execute(insert_book, insert_book_params)
            else:
                book_uuid = book_result['book_id']
            chapter_book_id = book_uuid
            if title_size == 3:
                book_uuid2 = uuid.uuid4()
                chapter_book_id = book_uuid2
                book_name2 = titles[1]
                print('book_name2:' + book_name2)
                book_sql = 'select book_id from book_info where book_name=%s and parent_name=%s'
                book_sql_params = (book_name2, book_name)
                cursor.execute(book_sql, book_sql_params)
                book_result = cursor.fetchone()
                if book_result is None:
                    insert_book = 'insert into book_info (book_id,parent_id,book_name,parent_name,update_time) values (%s,%s,%s,%s,%s)'
                    insert_book_params = (book_uuid2, book_uuid, book_name2, book_name, datetime.now())
                    cursor.execute(insert_book, insert_book_params)
            if title_size > 3:
                chapter_name = titles[1:-1]
            else:
                chapter_name = titles[-1]
            chapter_id = uuid.uuid4()
            chapter_sql = 'select chapter_id from chapter_info where chapter_name=%s'
            cursor.execute(chapter_sql, chapter_name)
            chapter_result = cursor.fetchone()
            if chapter_result is None:
                insert_chapter_info = 'insert into chapter_info(chapter_id,book_id,chapter_name,update_time) values (%s,%s,%s,%s)'
                insert_chapter_info_params = (chapter_id, chapter_book_id, chapter_name, datetime.now())
                cursor.execute(insert_chapter_info, insert_chapter_info_params)
                insert_chapter_content = 'insert into chapter_content(content_id,chapter_id,content) values (%s,%s,%s)'
                insert_chapter_content_params = (uuid.uuid4(), chapter_id, content)
                cursor.execute(insert_chapter_content, insert_chapter_content_params)
            self.conn.commit()
        return item

    def handle_item_book_info(self, item):
        with self.conn.cursor() as cursor:
            book_name = item['book_name']
            print('book_name:' + book_name)
            description = item['description']
            book_sql = 'select book_id from book_info where book_name=%s'
            cursor.execute(book_sql, book_name)
            book_result = cursor.fetchone()
            if book_result is None:
                insert_book = 'insert into book_info (book_id,book_name,description,update_time) values (%s,%s,%s,%s)'
                insert_book_params = (uuid.uuid4(), book_name, description, datetime.now())
                cursor.execute(insert_book, insert_book_params)
            else:
                update_book = 'update book_info set description=%s where book_name=%s'
                update_book_params = (description, book_name)
                cursor.execute(update_book, update_book_params)
            self.conn.commit()
        return item

    def handle_unknown_item_type(self, item):
        print('handle_unknown_item_type')
        return
