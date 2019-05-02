# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from ..items import RoisItem
from scrapy.selector import Selector
import re

class RosiSpider(scrapy.Spider):
    name = 'rosi'
    allowed_domains = ['http://www.meiyuanguan.com/']
    start_urls = ['http://www.meiyuanguan.com/']

    all_url = set(start_urls)
    def start_requests(self):
        # url = self.parse0
        # # print(url)
        # self.all_url.add()
        # while self.start_urls.__len__():
        for i in range(1,230):
            url = "http://www.meiyuanguan.com/meinv/" + str(i)+".html"
            self.all_url.add(url)
        for u in self.all_url:
            yield scrapy.Request(
                u,
                callback=self.parse,
                errback=self.errback,
                dont_filter=True
            )

    # / html / body / div / div[4] / div[1] / a[16]
    # def parse0(self,response):
    #     selector = Selector(response)
    #     url = selector.xpath('/html/body/div/div[4]/div[1]/a[16]/@href').extract_first()
    #     print('------------------------')
    #     print(url)
    #     print('------------------------')

    def parse(self,response):
        yield self.parse_item(response)
        print('--------------------------')
        print(response.css('p::attr(href)').extract())
        print('--------------------------')

        for a in response.css('p::attr(href)').extract():
            if not a:
                continue
            next_page = response.urljoin(a)
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_item(self, response):
        il = ItemLoader(item=RoisItem(), response=response)
        il.add_css('image_urls', 'img::attr(src)')
        return il.load_item()

    def errback(self):
        pass