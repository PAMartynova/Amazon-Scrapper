# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    ratings = scrapy.Field()
    country = scrapy.Field()

class MobileItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    brand = scrapy.Field()
    OS = scrapy.Field()