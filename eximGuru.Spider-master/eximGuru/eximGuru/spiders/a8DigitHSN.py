# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from eximGuru.items import EximguruItem

class A8digithsnSpider(scrapy.Spider):
    name = '8DigitHSN'
    allowed_domains = ['http://www.eximguru.com/india-trade-data/hs-locator/default.aspx?HSCode=0101']
    start_urls = ['http://www.eximguru.com/india-trade-data/hs-locator/default.aspx?HSCode=0101']
    def __init__(self,filename=None):
        if filename:
            with open(filename, 'r') as f:
                for line in f:
                    self.start_urls.append(line.rstrip())
    def make_requests_from_url(self, url):
        return scrapy.Request(url, dont_filter=True, meta = {
                  'dont_redirect': True,
                  'handle_httpstatus_list': [301,302]
            })
    def parse(self, response):
        data=response.xpath('//tr[contains(@class,"sliststyle")]')
        for d in data[1:]:
            item=EximguruItem()
            item['HSN_Code']=d.xpath('td[2]/text()').extract_first()
            item['Desc']=d.xpath('td[3]/text()').extract_first()
            yield item