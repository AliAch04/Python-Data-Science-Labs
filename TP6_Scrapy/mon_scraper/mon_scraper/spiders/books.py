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
        book = BookItem()
        
        # Fonction de nettoyage helper
        clean_text = lambda x: x.strip() if x else None
        clean_price = lambda x: float(x.replace('£', '').strip()) if x and x.replace('£', '').strip() else None
        
        book['title'] = clean_text(response.css('h1::text').get())
        book['price'] = clean_price(response.css('p.price_color::text').get())
        
        availability = response.css('p.availability::text').getall()
        book['availability'] = ' '.join(filter(None, [text.strip() for text in availability])) or None
        
        book['description'] = clean_text(response.xpath('//div[@id="product_description"]/following-sibling::p/text()').get())
        book['upc'] = clean_text(response.xpath('//th[contains(text(), "UPC")]/following-sibling::td/text()').get())
        book['product_type'] = clean_text(response.xpath('//th[contains(text(), "Product Type")]/following-sibling::td/text()').get())
        
        tax_raw = response.xpath('//th[contains(text(), "Tax")]/following-sibling::td/text()').get()
        book['tax'] = clean_price(tax_raw)
        
        yield book

            