import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import os

# Pour les images (optionnel)
class BookImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        # Nommer l'image par UPC
        upc = item.get('upc', 'unknown')
        image_name = f"{upc}.jpg"
        return f'full/{image_name}'

class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    
    # Variable pour suivre les livres déjà scrappés
    scraped_books = set()
    
    def __init__(self, *args, **kwargs):
        super(BooksSpider, self).__init__(*args, **kwargs)
        
        # Récupérer la catégorie depuis les settings
        from scrapy.utils.project import get_project_settings
        settings = get_project_settings()
        
        self.category_filter = settings.get('CATEGORY', 'all').lower()
        self.export_format = settings.get('EXPORT_FORMAT', 'csv')
        self.download_images = settings.get('DOWNLOAD_IMAGES', False)
        
        # Afficher la configuration
        self.logger.info(f"Configuration: Catégorie='{self.category_filter}', Format='{self.export_format}'")
    
    rules = (
        # Règle 1: Suivre les pages de pagination
        Rule(
            LinkExtractor(allow=r'catalogue/page-\d+\.html', 
                         deny=r'catalogue/category/books/page-\d+\.html'),
            callback='parse_page',
            follow=True,
            process_request='set_category_request'
        ),
        
        # Règle 2: Suivre les catégories
        Rule(
            LinkExtractor(allow=r'catalogue/category/books/'),
            callback='parse_category_page',
            follow=True,
            process_request='set_category_request'
        ),
        
        # Règle 3: Suivre les pages de pagination dans les catégories
        Rule(
            LinkExtractor(allow=r'catalogue/category/books/.+page-\d+\.html'),
            callback='parse_category_page',
            follow=True,
            process_request='set_category_request'
        ),
        
        # Règle 4: Scraper les pages de détail des livres
        Rule(
            LinkExtractor(allow=r'catalogue/.+/index\.html',
                         deny=[r'catalogue/page-', r'catalogue/category/']),
            callback='parse_book',
            follow=False,
            process_request='set_category_request'
        ),
        
        # Règle 5: Page d'accueil -> catégories
        Rule(
            LinkExtractor(restrict_xpaths='//div[@class="side_categories"]//a'),
            callback='parse_category_page',
            follow=True,
            process_request='set_category_request'
        ),
    )
    
    def set_category_request(self, request, response):
        """Ajoute des métadonnées à la requête pour suivre la catégorie"""
        # Extraire la catégorie de l'URL si possible
        if 'category' in request.url:
            parts = request.url.split('/')
            for i, part in enumerate(parts):
                if part == 'category' and i + 1 < len(parts):
                    request.meta['category'] = parts[i + 1].replace('_', ' ').replace('-', ' ')
                    break
        
        # Ajouter un header pour éviter le bannissement
        request.headers['Referer'] = response.url
        
        return request
    
    def parse_page(self, response):
        """Parse une page de liste de livres (page d'accueil)"""
        self.logger.info(f'Crawling page: {response.url}')
        
        # Extraire les liens de livres sur cette page
        book_links = response.css('h3 a::attr(href)').getall()
        
        for link in book_links:
            full_url = response.urljoin(link)
            if full_url not in self.scraped_books:
                self.scraped_books.add(full_url)
                yield scrapy.Request(
                    full_url,
                    callback=self.parse_book,
                    meta={'category': 'homepage'}
                )
    
    def parse_category_page(self, response):
        """Parse une page de catégorie"""
        # Extraire le nom de la catégorie
        category_name = response.css('h1::text').get()
        if not category_name:
            category_name = response.meta.get('category', 'unknown')
        
        self.logger.info(f'Crawling category page: {category_name} - {response.url}')
        
        # Appliquer le filtre de catégorie
        if self.category_filter != 'all' and self.category_filter not in category_name.lower():
            self.logger.info(f"Skipping category: {category_name} (filter: {self.category_filter})")
            return
        
        # Extraire les liens de livres dans cette catégorie
        book_links = response.css('h3 a::attr(href)').getall()
        
        for link in book_links:
            full_url = response.urljoin(link)
            if full_url not in self.scraped_books:
                self.scraped_books.add(full_url)
                yield scrapy.Request(
                    full_url,
                    callback=self.parse_book,
                    meta={'category': category_name}
                )
    
    def parse_book(self, response):
        """Parse une page de détail de livre"""
        # Helper functions
        clean_text = lambda x: x.strip() if x else None
        clean_price = lambda x: float(x.replace('£', '').strip()) if x and x.replace('£', '').strip() else None
        
        # Extraire la catégorie
        category = response.meta.get('category', 'unknown')
        
        # Extraire le breadcrumb pour la catégorie si non défini
        if category == 'unknown' or category == 'homepage':
            breadcrumb = response.css('ul.breadcrumb li a::text').getall()
            if len(breadcrumb) > 1:
                category = breadcrumb[-1]
        
        # Construction de l'item
        book = {
            # Informations de base
            'title': clean_text(response.css('h1::text').get()),
            'price': clean_price(response.css('p.price_color::text').get()),
            
            # Catégorie et URL
            'category': category,
            'url': response.url,
            
            # Disponibilité
            'availability': self._extract_availability(response),
            
            # Description
            'description': clean_text(response.xpath('//div[@id="product_description"]/following-sibling::p/text()').get()),
            
            # Informations produit
            'upc': clean_text(response.xpath('//th[contains(text(), "UPC")]/following-sibling::td/text()').get()),
            'product_type': clean_text(response.xpath('//th[contains(text(), "Product Type")]/following-sibling::td/text()').get()),
            
            # Prix et taxes
            'price_excl_tax': clean_price(response.xpath('//th[contains(text(), "Price (excl. tax)")]/following-sibling::td/text()').get()),
            'price_incl_tax': clean_price(response.xpath('//th[contains(text(), "Price (incl. tax)")]/following-sibling::td/text()').get()),
            'tax': clean_price(response.xpath('//th[contains(text(), "Tax")]/following-sibling::td/text()').get()),
            
            # Stock
            'number_available': self._extract_number_available(response),
            
            # Reviews
            'number_of_reviews': clean_text(response.xpath('//th[contains(text(), "Number of reviews")]/following-sibling::td/text()').get()),
            
            # Rating
            'rating': self._extract_rating(response),
            
            # Image
            'image_url': response.urljoin(response.css('div.item.active img::attr(src)').get()),
        }
        
        self.logger.debug(f"Book extracted: {book['title']} - {book['category']}")
        yield book
        
        # Télécharger l'image si configuré
        if self.download_images and book['image_url']:
            yield {
                'image_urls': [book['image_url']],
                'upc': book['upc']
            }
    
    def _extract_availability(self, response):
        """Extrait la disponibilité"""
        availability = response.css('p.availability::text').getall()
        if availability:
            return ' '.join(filter(None, [text.strip() for text in availability])).strip()
        return None
    
    def _extract_number_available(self, response):
        """Extrait le nombre disponible"""
        availability_text = response.css('p.availability::text').getall()
        if availability_text:
            import re
            for text in availability_text:
                numbers = re.findall(r'\d+', text)
                if numbers:
                    return int(numbers[0])
        return 0
    
    def _extract_rating(self, response):
        """Extrait la note sous forme numérique"""
        rating_class = response.css('p.star-rating::attr(class)').get()
        if rating_class:
            # Convertir "star-rating Three" en "3"
            rating_map = {
                'One': 1, 'Two': 2, 'Three': 3, 
                'Four': 4, 'Five': 5
            }
            for key, value in rating_map.items():
                if key in rating_class:
                    return value
        return None
    
    def closed(self, reason):
        """Appelé quand le spider se ferme"""
        self.logger.info(f"Spider closed: {reason}")
        self.logger.info(f"Total books scraped: {len(self.scraped_books)}")