# -*- coding: utf-8 -*-
from scrapy.selector import SelectorList

__author__ = 'Xin Zhong'
import scrapy
from miner.items import BXJItem


class BxjPostSpider(scrapy.Spider):
    name = "bxj_post_spider"
    allowed_urls = ["bbs.hupu.com/"]
    start_urls = ["http://bbs.hupu.com/bxj-postdate-" + str(idx) for idx in xrange(1, 100)]

    def parse(self, response):
        table = response.xpath('//table[@id="pl"]')
        for tr in table.xpath('.//tr'):

            node_title = tr.xpath('./td[@class="p_title"]')
            if node_title:
                item = BXJItem()
                common = node_title.xpath('./a[@id]/text()').extract()
                font = node_title.xpath('./a[@id]/font/text()').extract()
                b_font = node_title.xpath('./a[@id]/b/font/text()').extract()
                b = node_title.xpath('./a[@id]/b/text()').extract()

                item['title'] = common or font or b_font or b
                item['post_id'] = node_title.xpath('./a[@id]/@href').re(r'\w+')

                item['zone'] = node_title.xpath('./a[not(@id)]/@href').re(r'\w+')

                mulitpage_urls_list = node_title.xpath('./span[@class="multipage"]/a/@href').extract()
                item['post_page_count'] = [u'1'] if len(mulitpage_urls_list) == 0 else [unicode(len(mulitpage_urls_list) + 1)]

                item['light_count'] = node_title.xpath('./child::span/a/@title').re(r'\d+')

                node_author = tr.xpath('./td[@class="p_author"]')

                if node_author:
                    item['username'] = node_author.xpath('./a/text()').extract()
                    item['user_id'] = node_author.xpath('./a/@href').re(r'\w+')
                    item['create_date'] = node_author.xpath('./text()').extract()

                node_retime = tr.xpath('./td[@class="p_retime"]')
                if node_retime:
                    item['last_reply_time'] = node_retime.xpath('./a/text()').extract()
                    item['last_reply_url'] = node_retime.xpath('./a/@href').extract()
                    item['last_reply_username'] = node_retime.xpath('./text()').extract()

                node_re = tr.xpath('./td[@class="p_re"]')
                if node_re:
                    item['reply_count'] = node_re.xpath('./text()').re("^\d+")
                    item['browsing_count'] = node_re.xpath('./text()').re("\d+$")

                yield item
