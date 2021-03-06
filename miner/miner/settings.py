# -*- coding: utf-8 -*-

# Scrapy settings for miner project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'miner'

SPIDER_MODULES = ['miner.spiders']
NEWSPIDER_MODULE = 'miner.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'miner (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    BOT_NAME+'.pipelines.BXJDailyPostDigestPipeline': 300,
    BOT_NAME+'.pipelines.BXJPostDigestDuplicatesPipeline': 301,
    BOT_NAME+'.pipelines.BXJPostDigestJsonWirterPipeline': 302,
    BOT_NAME+'.pipelines.BXJPostDigestMongoPipeline': 303,
}


MONGODB_URI = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "HupuMiner"

