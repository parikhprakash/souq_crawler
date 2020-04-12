# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SouqItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    product_url = scrapy.Field()
    product_price = scrapy.Field()
    product_specification = scrapy.Field()
    product_description = scrapy.Field()
    product_images = scrapy.Field()
    product_categories = scrapy.Field()