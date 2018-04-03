# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TestItemItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class House(scrapy.Item):
    Real_Estate_Name = scrapy.Field()
    Real_Estate_Address = scrapy.Field()
    Real_Estate_Url = scrapy.Field()
    Price = scrapy.Field()
    The_Latest_Opening_Time = scrapy.Field()
    Earliest_Delivery_Time = scrapy.Field()
    Years_Of_Property_Rights = scrapy.Field()
    Parking_Space = scrapy.Field()
    First_Update_Time = scrapy.Field()
    Latest_Update_Time = scrapy.Field()
    Metro = scrapy.Field()
