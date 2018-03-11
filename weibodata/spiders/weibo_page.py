# -*- coding: utf-8 -*-

import redis
from weibodata.settings import TABLE_NAME,PAGE

maxpage = PAGE
def get_weibo_page(maxpage):
    page_list = []
    for i in range(1,maxpage + 1):
        url = 'https://weibo.cn/{TABLE_NAME}?filter=1&page={page}'.format(TABLE_NAME=TABLE_NAME,page = str(i))
        redis_key = TABLE_NAME + ':start_urls'
        r.rpush(redis_key,url)

        # page_list.append(url)
    # r.set('rmrb:start_urls',page_list)

r = redis.Redis(host='localhost',port=6379)


if __name__ == '__main__':
    get_weibo_page(maxpage)
    # get_keys()