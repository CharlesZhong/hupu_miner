# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json
from scrapy.exceptions import DropItem
from scrapy import log
from datetime import datetime,timedelta

class MinerPipeline(object):
    def process_item(self, item, spider):
        return item


class BXJDailyPostDigestPipeline(object):

    def __init__(self):
        log.start(logfile=None, loglevel=log.DEBUG, logstdout=True)

    def process_item(self, item, spider):

        if not item['post_id']:
            raise DropItem("Miss post_id in %s" % item)

        if not item['create_date']:
            raise DropItem("Miss create_time in %s" % item)

        create_date = datetime.strptime(item["create_date"][0], "%Y-%m-%d")
        # delta = datetime.today() - create_date
        # if delta.days != 1:
        #     raise DropItem("Not Yesterday's data %s" % item)


        for key in item:
            item[key] = item[key][0].encode('utf8') if item[key] else ""
        for key in ['reply_count', 'browsing_count', 'light_count', 'post_page_count']:
            item[key] =  int(item[key]) if item[key] else 0
        return item

    def open_spider(self, spider):
        log.msg("Start BXJ Daily Item Pipeline...")

    def close_spider(self, spider):
        log.msg("End BXJ Daily Item Pipeline!")

class BXJPostDigestDuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['post_id'] in self.ids_seen:
            raise DropItem("Duplicate post_id found: %s" % item)
        else:
            self.ids_seen.add(item['post_id'])
            return item

class BXJPostDigestJsonWirterPipeline(object):

    def __init__(self):
        self.file = open('BXJ_Post.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

class BXJPostDigestMongoPipeline(object):


    def __init__(self, mongo_uri, mongo_db):
        self.colloction_name = 'post_digest'
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.colloction_name].insert(dict(item))
        return item