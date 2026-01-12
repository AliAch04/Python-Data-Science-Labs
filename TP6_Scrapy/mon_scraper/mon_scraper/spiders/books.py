from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from mon_scraper.items import ProductItem 

class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    rules = (
        Rule(LinkExtractor(allow=r'catalogue/page-\d+\.html'), callback='parse_page', follow=True),
        Rule(LinkExtractor(allow=r'catalogue/.+/index\.html'), callback='parse_book', follow=False),
    )

    def parse_page(self, response):
        self.logger.info(f'Crawling page: {response.url}')

    def parse_book(self, response):
        item = ProductItem()
        
        item['title'] = response.css('h1::text').get()
        item['price'] = response.css('p.price_color::text').get()
        item['availability'] = response.css('p.availability::text').re_first(r'\d+')
        item['rating'] = response.css('p.star-rating::attr(class)').re_first(r'star-rating (\w+)')
        item['description'] = response.css('article.product_page p::text').get()
        item['url'] = response.url
        
        self.logger.info(f'Scraped book: {item["title"]} - {item["price"]}')
        
        # Yield l'item au lieu du dict
        yield item