# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import json
from scrapy.exceptions import DropItem

class PriceValidationPipeline:
    """Valide le prix et supprime les items avec prix invalides"""
    def __init__(self):
        self.spider = None  # Stocker la référence au spider
    
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        pipeline.crawler = crawler  # Stocker le crawler
        return pipeline
    
    def process_item(self, item, spider):
        # Votre code existant...
        if 'price' in item and item['price']:
            try:
                price_str = item['price'].replace('£', '').replace('€', '').strip()
                price = float(price_str)
                
                if price < 0:
                    raise DropItem(f"Prix négatif supprimé: {item}")
                    
            except (ValueError, AttributeError):
                item['price'] = None
        return item


class DataCleaningPipeline:
    """Nettoie les données (strip des strings)"""
    def __init__(self):
        self.spider = None
    
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        pipeline.crawler = crawler
        return pipeline
    
    def process_item(self, item, spider):
        # Votre code existant...
        adapter = ItemAdapter(item)
        # ... reste du code
        return item


class DatabasePipeline:
    """Stocke les items dans une base SQLite"""
    
    def __init__(self):
        self.con = None
        self.cur = None
        self.spider = None
        
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        pipeline.crawler = crawler
        return pipeline
    
    def open_spider(self, spider):
        """Ouvre la connexion à la base de données quand le spider démarre"""
        self.spider = spider  # Stocker le spider
        self.con = sqlite3.connect('books.db')
        self.cur = self.con.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                price REAL,
                availability INTEGER,
                rating TEXT,
                description TEXT,
                url TEXT UNIQUE,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.con.commit()
        
    def close_spider(self, spider):
        """Ferme la connexion à la base de données quand le spider s'arrête"""
        if self.con:
            self.con.close()
            
    def process_item(self, item, spider):
        """Insère l'item dans la base de données"""
        try:
            self.cur.execute('''
                INSERT OR IGNORE INTO books 
                (title, price, availability, rating, description, url)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                item.get('title'),
                float(item.get('price', 0).replace('£', '')) if item.get('price') else 0,
                int(item.get('availability', 0)) if item.get('availability') else 0,
                item.get('rating'),
                item.get('description'),
                item.get('url')
            ))
            self.con.commit()
        except Exception as e:
            # Utiliser spider.logger si disponible
            if spider:
                spider.logger.error(f"Erreur DB: {e}")
            else:
                print(f"Erreur DB: {e}")
        return item


class JsonWriterPipeline:
    """Écrit les items dans un fichier JSON"""
    
    def __init__(self):
        self.items = []
        self.spider = None
        
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        pipeline.crawler = crawler
        return pipeline
    
    def open_spider(self, spider):
        """Initialise la liste quand le spider démarre"""
        self.spider = spider
        self.items = []
        
    def close_spider(self, spider):
        """Écrit dans le fichier JSON quand le spider s'arrête"""
        if self.items:
            import json
            with open('output_pipeline.json', 'w', encoding='utf-8') as f:
                json.dump(self.items, f, ensure_ascii=False, indent=2)
            if spider:
                spider.logger.info(f"Écrit {len(self.items)} items dans output_pipeline.json")
            
    def process_item(self, item, spider):
        """Ajoute l'item à la liste"""
        self.items.append(dict(item))
        return item


class MonScraperPipeline:
    """Pipeline de base (peut être supprimé ou gardé)"""
    def process_item(self, item, spider):
        return item