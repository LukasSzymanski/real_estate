# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RealEstateItem(scrapy.Item):
    date = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    city = scrapy.Field()
    url = scrapy.Field()
