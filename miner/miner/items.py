# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BXJItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    post_id = scrapy.Field() # post_url ==  http://bbs.hupu.com/ + id + .html
    post_page_count = scrapy.Field() # amount of the post' pages

    title = scrapy.Field()

    user_id = scrapy.Field() # user_url == http://my.hupu.com/ + id
    username = scrapy.Field()

    zone = scrapy.Field()

    reply_count = scrapy.Field()  # amount of reply
    browsing_count = scrapy.Field() # amount of browsing
    light_count = scrapy.Field() # amount of light reply

    create_date = scrapy.Field()

    last_reply_username = scrapy.Field()
    last_reply_time = scrapy.Field()
    last_reply_url = scrapy.Field()


