import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Importez votre spider
from mon_scraper.spiders.books import BooksSpider

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(BooksSpider, category='all')
    process.start()