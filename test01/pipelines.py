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
        if item_name == 'PoemItem':
            return self.handle_item_poem(item)
        elif item_name == 'ChapterContentItem':
            return self.handle_item_chapter_content(item)
        elif item_name == 'BookInfoItem':
            return self.handle_item_book_info(item)
        elif item_name == 'CtextBookItem':
            return self.handle_ctext_item(item)
        elif item_name == 'AuthorItem':
            return self.handle_item_author(item)
        elif item_name == 'PoetCategoryItem':
            return self.handle_item_poet_category(item)

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
            select_poem = 'select id from s_poem where title=%s and author_name=%s'
            cursor.execute(select_poem, (item['title'], author_name))
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
            description = item['description']
            book_sql = 'select book_id from book_info where book_name=%s'
            cursor.execute(book_sql, book_name)
            book_result = cursor.fetchone()
            if book_result is None:
                insert_book = 'insert into book_info (book_id,book_name,description,update_time) values (%s,%s,%s,%s)'
                insert_book_params = (uuid.uuid4(), book_name, description, datetime.now())
                cursor.execute(insert_book, insert_book_params)
            else:
                update_book = 'update book_info set description=%s where book_name=%s and description='''
                update_book_params = (description, book_name)
                cursor.execute(update_book, update_book_params)
                print(book_name)
            self.conn.commit()
        return item

    def handle_unknown_item_type(self, item):
        print('handle_unknown_item_type')
        return

    def handle_ctext_item(self, item):
        book_info = item['book_category_info']
        if book_info is None:
            return
        book_info_len = len(book_info)
        if book_info_len < 3:
            return
        print(book_info)
        with self.conn.cursor() as cursor:
            category1_name = book_info[0]
            category2_name = book_info[1]
            category1_sql = 'select category_id from c_book_category where category_name=%s'
            cursor.execute(category1_sql, category1_name)
            categroy_result = cursor.fetchone()
            category1_id = uuid.uuid4()
            if categroy_result is None:
                insert_category1 = 'insert into c_book_category (category_id,category_name,oper_time) values (%s,%s,%s)'
                insert_category1_params = (category1_id, category1_name, datetime.now())
                cursor.execute(insert_category1, insert_category1_params)
            else:
                category1_id = categroy_result['category_id']
            print('category_id:' + category1_id)
            cursor.execute(category1_sql, category2_name)
            categroy_result = cursor.fetchone()
            category2_id = uuid.uuid4()
            if categroy_result is None:
                insert_category2 = 'insert into c_book_category (category_id,category_name,parent_name,parent_id,oper_time) values (%s,%s,%s,%s,%s)'
                insert_category2_params = (category2_id, category2_name, category1_name, category1_id, datetime.now())
                cursor.execute(insert_category2, insert_category2_params)
            else:
                category2_id = categroy_result['category_id']
            self.conn.commit()
        return item

    def handle_item_author(self, item):
        author_name = item['a_name']
        if not author_name:
            return
        with self.conn.cursor() as cursor:
            select_author = 'select id from s_author where a_name=%s'
            cursor.execute(select_author, author_name)
            author_result = cursor.fetchone()
            if author_result is None:
                author_params = (
                    uuid.uuid4(), author_name, item['a_dynasty'], item['a_remark'], datetime.now())
                insert_author = 'insert into s_author(id,a_name,a_dynasty,a_remark,oper_time) values (%s,%s,%s,%s,%s)'
                cursor.execute(insert_author, author_params)
            else:
                update_author = 'update s_author set a_remark=%s,oper_time=now() where a_name=%s and a_dynasty='''
                cursor.execute(update_author, (item['a_remark'], author_name))
            self.conn.commit()
        return item

    def handle_item_poet_category(self, item):
        poets_category = item['category_name']
        with self.conn.cursor() as cursor:
            for category in poets_category:
                select_sql = 'select id from s_poem_category where category_name=%s'
                cursor.execute(select_sql, category)
                result = cursor.fetchone()
                if result is None:
                    insert_category = 'insert into s_poem_category (category_name,oper_time) values (%s,now())'
                    cursor.execute(insert_category, category)
            poets_sql = 'select id from s_poets where poets_name=%s'
            poets_name = item['poets_name']
            cursor.execute(poets_sql, poets_name)
            result = cursor.fetchone()
            if result is None:
                poets_sql = 'insert into s_poets(poets_name,poets_number,poets_remark,oper_time) values (%s,%s,%s,%s)'
                poets_params = (poets_name, item['poets_number'], item['poets_remark'], datetime.now())
                cursor.execute(poets_sql, poets_params)
            self.conn.commit()
        return item
        pass
