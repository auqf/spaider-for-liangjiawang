# -*- coding: utf-8 -*-
import scrapy
import csv
import sys
from test_item.items import House


class HousePropertySpider(scrapy.Spider):
    name = 'house_property'
    start_urls=[]
    f = csv.reader(open('/home/auqf/scrapy/test_item/url.csv'))
###需要创建三个spider一起爬行or 使用sitemap_rules
    for _ in f:
        start_urls.append(''.join(_).replace(".html","/news.html"))
        #if len(start_urls) > 10:
        #    break
    start_urls.pop(0)
    def parse(self, response):
        house=House()
        house['Real_Estate_Url'] = response._url.replace("/news.html",".html")
        house['First_Update_Time'] = response.xpath('//*[contains(@class,"feed") and (((count(preceding-sibling::*) + 1) = 15) and parent::*)]//*[contains(@class,"date")]/text()').extract()
        house['Latest_Update_Time'] = response.xpath('//*[contains(@class,"feed") and (((count(preceding-sibling::*) + 1) = 1) and parent::*)]//*[contains(@class,"date")]/text()').extract()
        request = scrapy.Request(response._url.replace('news','details'), callback=self.parse2)
        request.meta['house'] = house
        return request

    def parse2(self, response):
        house = response.meta['house']
        house['Real_Estate_Name'] = response.xpath('//*[contains(@class,"box-base")]//li[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]//p/text()').extract_first(),
        house['Real_Estate_Address'] = response.xpath('//*[contains(@class,"box-base")]//li[(((count(preceding-sibling::*) + 1) = 2) and parent::*)]//p/text()').extract_first(),
        house['Price'] = response.xpath('//*[(@id = "sale_status_pos")] //li[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]//p/text()').extract_first(),
        house['The_Latest_Opening_Time'] = response.xpath('//*[(@id = "sale_status_pos")]//li[(((count(preceding-sibling::*) + 1) = 4) and parent::*)]//p/text()').extract_first(),
        house['Earliest_Delivery_Time'] = response.xpath('//*[(@id = "sale_status_pos")]//li[(((count(preceding-sibling::*) + 1) = 5) and parent::*)]//p/text()').extract_first(),
        house['Years_Of_Property_Rights'] = response.xpath('//li[(((count(preceding-sibling::*) + 1) = 7) and parent::*)]//p/text()').extract_first(),
        house['Parking_Space']= response.xpath('//*[contains(@class,"house-details")]//li[(((count(preceding-sibling::*) + 1) = 5) and parent::*)]//p/text()').extract_first(),
        request = scrapy.Request(response._url.replace('details','su'), callback=self.parse3)
        request.meta['house'] = house
        return request

    def parse3(self, response):
        house = response.meta['house']
        house['Metro'] = response.xpath('//*[contains(@class,"lk-list")]/text').extract_first() if response.xpath('//*[contains(@class,"lk-list")]/text').extract_first()  else "No" 
        return house
