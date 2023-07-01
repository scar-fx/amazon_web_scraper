# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class product_items(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    number_of_ratings = scrapy.Field()