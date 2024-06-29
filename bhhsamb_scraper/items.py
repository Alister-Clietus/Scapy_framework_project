import scrapy

class PropertyItem(scrapy.Item):
    title = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    details = scrapy.Field()
    url = scrapy.Field()
