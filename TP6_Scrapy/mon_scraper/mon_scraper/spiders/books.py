from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    rules = (
        Rule(LinkExtractor(allow=r'catalogue/page-\d+\.html'), callback='parse_page', follow=True),
        Rule(LinkExtractor(allow=r'catalogue/.+/index\.html'), callback='parse_book',follow=False),
    )

    def parse_page(self, response):
        self.logger.info(f'Crawling page: {response.url}')
        

    def parse_book(self, response):
        yield {
            'title': response.css('h1::text').get(),
            'price': response.css('p.price_color::text').get(),
            'availability': response.css('p.availability::text').re_first(r'\d+'),
            'rating': response.css('p.star-rating::attr(class)').re_first(r'star-rating (\w+)'),
            'description': response.css('article.product_page p::text').get(),
            'url': response.url,
        }