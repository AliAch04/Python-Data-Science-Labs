import scrapy

class PaginationSpider(scrapy.Spider):
    name = 'pagination'
    start_urls = ['https://example.com/page/1']

    def parse(self, response):
        # Extraction des données
        for item in response.css('div.item'):
            yield {
                'title': item.css('h2::text').get(),
                'price': item.css('span.price::text').get(),
            }
        
        current_page = int(response.url.split('/')[-1])
        next_page = current_page + 1

        if next_page <= 100:
            yield scrapy.Request(f'https://example.com/page/{next_page}', callback=self.parse)