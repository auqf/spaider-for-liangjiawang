# -*- coding: utf-8 -*-
import scrapy


class JuliveSpider(scrapy.Spider):
    name = 'julive_url'
    start_urls = ['http://gz.julive.com/project/s/zengcheng',]

    def parse(self, response):
        for url in response.css('div.main_click_total'):
            yield {
                'url': url.css('div.main_click_total').css('h4').xpath('a[1]/@href').extract(),
            }
        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

