# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WeibodataPipeline(object):
    def process_item(self, item, spider):
        return item


import redis
class RedisPipeline(object):
    def __init__(self,redis_host,redis_password,redis_port,redis_db,table_name):
        self.host = redis_host
        self.password = redis_password
        self.port = redis_port
        self.db = redis_db
        self.table_name = table_name

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            redis_host=crawler.settings.get('REDIS_HOST'),
            redis_password=crawler.settings.get('REDIS_PWD'),
            redis_port=crawler.settings.get('REDIS_PORT'),
            redis_db=crawler.settings.get('REDIS_DB'),
            table_name=crawler.settings.get('TABLE_NAME'),
        )

    def open_spider(self,spider):
        self.client = redis.Redis(host=self.host,password=self.password,db=self.db,port=self.port)

    def process_item(self,item,spider):
        name = item.__class__.__name__
        if name == 'weib_allItem':
            weibo_url_repost = item['weibo_url_repost']
            key = self.table_name + ':weibo_urls'
            self.client.lpush(key,weibo_url_repost)
            return item

    def close_spider(self,spider):
        self.client.close()


import pymongo
class MongoPipeline(object):

    def __init__(self,mongo_uri,mongo_db,table_name,weibo_index,weibo_reposter_index,table_weibo_reposter,table_weibo_reposter_index):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.table_name = table_name
        self.weibo_index = weibo_index
        self.weibo_reposter_index = weibo_reposter_index
        self.table_weibo_reposter = table_weibo_reposter
        self.table_weibo_reposter_index = table_weibo_reposter_index

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            table_name=crawler.settings.get('TABLE_NAME'),
            table_weibo_reposter=crawler.settings.get('TABLE_WEIBO_REPOSTER'),
            weibo_index=crawler.settings.get('WEIBO_INDEX'),
            weibo_reposter_index=crawler.settings.get('WEIBO_REPOSTER_INDEX'),
            table_weibo_reposter_index=crawler.settings.get('TABLE_WEIBO_REPOSTER_INDEX')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def process_item(self,item,spider):
        name = item.__class__.__name__
        if name == 'weib_allItem':
            self.db[self.table_name].ensure_index(self.weibo_index,unique = True)
            self.db[self.table_name].insert(dict(item))
            return item
        elif name == 'weibo_repostItem':
            self.db[self.table_weibo_reposter].ensure_index(self.table_weibo_reposter_index, unique=True)
            # self.db[self.table_weibo_reposter].update(dict(item))
            self.db[self.table_weibo_reposter].insert(dict(item))
            return item

    def close_spider(self,spider):
        self.client.close()


import pymysql
from weibodata.settings import TABLE_NAME,TABLE_WEIBO_REPOSTER

class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1',user = 'root',passwd = '123',db = 'weibodata',charset = 'utf8')
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        name = item.__class__.__name__
        if name == 'weib_allItem':
            weibo_id = item['weibo_id']
            content = item['content']
            publish_date = item['publish_date']
            attitude_num = item['attitude_num']
            repost_num = item['repost_num']
            comment_num = item['comment_num']
            video_num = item['video_num']
            image_num = item['image_num']
            weibo_url_repost = item['weibo_url_repost']
            create_time = item['create_time']
            sql ="insert into "+TABLE_NAME+"(weibo_id,content,publish_date,attitude_num,repost_num,comment_num,video_num,image_num,weibo_url_repost,create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            # sql = """
            #         insert into rmrb(weibo_id,content,publish_date,attitude_num,repost_num,comment_num,video_num,image_num,weibo_url_repost,create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            #         """
            self.cursor.execute(sql,(weibo_id,content,publish_date,attitude_num,repost_num,comment_num,video_num,image_num,weibo_url_repost,create_time))
        elif name == 'weibo_repostItem':
            reposter_id_url = item['reposter_id_url']
            reposter_page = item['reposter_page']
            weibo_id = item['weibo_id']
            reposter_info = item['reposter_info']
            create_time = item['create_time']
            sql = "insert into "+TABLE_WEIBO_REPOSTER+"(weibo_id,reposter_id_url,reposter_page,reposter_info,create_time) VALUES (%s,%s,%s,%s,%s)"
            self.cursor.execute(sql, (weibo_id,reposter_id_url,reposter_page,reposter_info,create_time))
        return item

        def close_spider(self,spider):
            self.conn.close()
