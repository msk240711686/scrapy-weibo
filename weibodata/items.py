# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeibodataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class weib_allItem(scrapy.Item):
    weibo_id = scrapy.Field()
    content = scrapy.Field()
    publish_date = scrapy.Field()
    attitude_num = scrapy.Field()
    repost_num = scrapy.Field()
    comment_num = scrapy.Field()
    video_num = scrapy.Field()
    image_num = scrapy.Field()
    weibo_url_repost = scrapy.Field()
    create_time = scrapy.Field()


class weibo_repostItem(scrapy.Item):
    reposter_id_url = scrapy.Field()
    reposter_info = scrapy.Field()
    reposter_page = scrapy.Field()
    weibo_id = scrapy.Field()
    create_time = scrapy.Field()

