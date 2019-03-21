# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.http.response.html import HtmlResponse
from ..items import MoviecommentItem


class DbcommitSpider(RedisCrawlSpider):
    name = 'dbcommit'
    allowed_domains = ['douban.com']
    # start_urls = ['https://movie.douban.com/subject/27624661/comments?start=0&limit=20']  本地Redis指定

    rules = (
        Rule(LinkExtractor(allow=r'start=\d+'), callback='parse_item', follow=False),
    )

    def parse_item(self, response:HtmlResponse):
        # i = {}
        # #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # #i['name'] = response.xpath('//div[@id="name"]').extract()
        # #i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i

        # //div[@class="comment-item"]//span[@class="short"]/text()
        pattern = '//div[@class="comment-item"]//span[@class="short"]/text()'
        comments = response.xpath(pattern).extract()
        for comment in comments:
            item = MoviecommentItem()
            item['comment'] = comment.strip()
            yield item

