import scrapy

class ProductItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    discount_price = scrapy.Field()
    rating = scrapy.Field()
    reviews_count = scrapy.Field()
    availability = scrapy.Field()
    images = scrapy.Field()
    specifications = scrapy.Field()
    url = scrapy.Field()
    scraped_at = scrapy.Field()