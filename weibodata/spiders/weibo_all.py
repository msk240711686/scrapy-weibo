# -*- coding: utf-8 -*-
from  scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from urllib import parse
from weibodata.items import weib_allItem

import re
import time
from weibodata.settings import TABLE_NAME


class WeiboAllSpider(RedisSpider):
    name = 'weibo_all'
    allowed_domains = ['weibo.cn']
    redis_key = TABLE_NAME + ':start_urls'

    # 微博链接拼接时用到的字符串
    weibo_http = 'https://weibo.cn/'
    weibo_repost = 'repost/'
    weibo_comment = 'comment/'
    weibo_attitude = 'attitude/'

    def parse(self, response):
        weibo_ids = response.css('div.c::attr(id)').extract()
        # 循环当前页的 所有id 并提取出 转发数  评论数 点赞数
        for weibo_idm in weibo_ids:
            print(weibo_idm)
            weibo_id = re.search('M_(.*)', weibo_idm)
            weibo_id = weibo_id.group(1)

            # 微博内容
            content = response.css("#" + weibo_idm + " span.ctt::text").extract()
            content = ' '.join(content)
            # 发布时间
            publish_date = response.css("#" + weibo_idm + " span.ct::text").extract()[0]

            # 获取每条微博的所有数据的文本形式
            all_num_content = response.css("#" + weibo_idm + " div a::text").extract()
            all_num_content = ''.join(all_num_content)

            # 获取 赞 转发 评论 数（通过正则表达式）
            all_num = re.search('赞\[(\d+)\]转发\[(\d+)\]评论\[(\d+)\]', all_num_content)
            attitude_num = all_num.group(1)
            repost_num = all_num.group(2)
            comment_num = all_num.group(3)

            # 是否有视频
            video = re.search('秒拍视频', all_num_content)
            if video:
                video_num = '1'
            else:
                video_num = '0'

            # 是否有图片  有几张
            image = re.search('组图共(\d)张', all_num_content)
            if image:
                image_num = image.group(1)
            else:
                image_num = '0'

            weibo_url_repost = self.weibo_http + self.weibo_repost + weibo_id

            weib_all_Item = weib_allItem()
            weib_all_Item['weibo_id'] = weibo_id
            weib_all_Item['content'] = content
            weib_all_Item['publish_date'] = publish_date
            weib_all_Item['attitude_num'] = attitude_num
            weib_all_Item['repost_num'] = repost_num
            weib_all_Item['comment_num'] = comment_num
            weib_all_Item['video_num'] = video_num
            weib_all_Item['image_num'] = image_num
            weib_all_Item['weibo_url_repost'] = weibo_url_repost
            weib_all_Item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            yield weib_all_Item
