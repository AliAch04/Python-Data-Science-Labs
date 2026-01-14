
# TP : Web Scraping et Crawling avec Scrapy

#### Fait par : Ali ACHENAN  - Master IAOC

## Introduction
Ce README documente mon travail sur le TP de Web Scraping et Crawling avec Scrapy. Le projet suit les étapes décrites dans le PDF "TP6.pdf". J'ai créé un projet Scrapy nommé `mon_scraper`.

Voici un résume par partie avec codes, tests et captures d'ecran des pages du PDF.

## Partie 1 : Introduction à Scrapy
Scrapy est un framework Python pour extraire des données structurées, crawler des pages, gérer des requêtes asynchrones, et exporter en JSON/CSV/XML.

- **Architecture :** Request → Downloader → Spider → Item Pipeline → Export.
- **Tests :** Vérifié avec `scrapy bench` pour les performances.


## Partie 2 : Installation et configuration
- **Installation :** `pip install scrapy` → Vérifié avec `scrapy version`.
- **Dépendances :** `pip install scrapy-user-agents scrapy-splash scrapy-redis`.


## Partie 3 : Création d’un projet Scrapy
- **Commandes :** `scrapy startproject mon_scraper` puis `scrapy genspider quotes quotes.toscrape.com`.
- **Structure :**  
  ```
  mon_scraper/
  ├── scrapy.cfg
  └── mon_scraper/
      ├── __init__.py
      ├── items.py
      ├── middlewares.py
      ├── pipelines.py
      ├── settings.py
      └── spiders/
          ├── __init__.py
          └── quotes.py
  ```


## Partie 4 : Spiders basiques
- **Exemple de spider :** Dans `spiders/quotes.py` 
- **Exécution :** `scrapy crawl quotes -o quotes.json` -> Fichier JSON généré avec quotes, authors, tags.
- **Pagination :** Suivi automatique du "Next" via `response.follow`.
- **Outputs :** Exemples d'exports en CSV et XML testés.

## Partie 5 : Sélecteurs CSS et XPath
- Dans le shell : Lancé avec `scrapy shell "http://quotes.toscrape.com/"`.

#### Voir l'URL actuelle
>response.url  
'http://quotes.toscrape.com/'

#### Voir le code HTML
>print(response.text[:500])  
<!DOCTYPE html>  
<html lang="en">  
<head>  
        <meta charset="UTF-8">  
        <title>Quotes to Scrape</title>  
    <link rel="stylesheet" href="/static/bootstrap.min.css">  
    <link rel="stylesheet" href="/static/main.css">  
  
  
</head>  
<body>  
    <div class="container">  
        <div class="row header-box">  
            <div class="col-md-8">  
                <h1>  
                    <a href="/" style="text-decoration: none">Quotes to Scrape</a>  
                </h1>  
            </div>

#### Tester un nouveau sélecteur
> response.css('div.quote span.text::text').getall()  
['“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”', '“It is our choices, Harry, that show what we truly are, far more than our abilities.”', '“There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”', '“The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.”', "“Imperfection is beauty, madness is genius and it's better to be absolutely ridiculous than absolutely boring.”", '“Try not to become a man of success. Rather become a man of value.”', '“It is better to be hated for what you are than to be loved for what you are not.”', "“I have not failed. I've just found 10,000 ways that won't work.”", "“A woman is like a tea bag; you never know how strong it is until it's in hot water.”", '“A day without sunshine is like, you know, night.”']

#### Testez le sélecteur CSS
> response.css('h1::text').get()  
'\n                    '

#### Testez le sélecteur XPath
> response.xpath('//h1/text()').get()  
'\n                    '

#### Pour avoir un résultat plus propre (sans les espaces)
> response.css('h1::text').get().strip()  
''

#### Ou avec XPath
>>> response.xpath('normalize-space(//h1)').get()  
'Quotes to Scrape'

#### Testez d'autres sélecteurs
>>> response.css('title::text').get()  
'Quotes to Scrape'  
>>> response.xpath('//title/text()').get()  
'Quotes to Scrape'

#### Pour voir tous les quotes
>>> quotes = response.css('div.quote')  
>>> len(quotes)  
10

#### Premier quote
>>first_quote = quotes[0]  
> first_quote.css('span.text::text').get()  
'“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”'  
>>> first_quote.xpath('.//span[@class="text"]/text()').get()  
'“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”'

#### L'auteur du premier quote
>>> first_quote.css('small.author::text').get()  
'Albert Einstein'  
>>> first_quote.xpath('.//small[@class="author"]/text()').get()  
'Albert Einstein'

#### Les tags du premier quote
>>> first_quote.css('div.tags a.tag::text').getall()  
['change', 'deep-thoughts', 'thinking', 'world']  
>>> first_quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').getall()  
['change', 'deep-thoughts', 'thinking', 'world']



![Page 5 du PDF](path/to/image_page5.png)

## Partie 6 : Crawling automatique
- **CrawlSpider :** Créé `spiders/books.py` avec Rules et LinkExtractor pour pagination et pages détails.
- **Pagination manuelle :** Implémenté dans `spiders/pagination.py`.
- **Test :** `scrapy crawl books -o books.json` 

## Partie 7 : Items et extraction de données complexes
- **Définition :** Dans `items.py`, créé ProductItem avec champs comme title, price, etc.
- **Utilisation :** Modifié spiders pour yield items au lieu de dicts, avec nettoyage (ex. strip prix).
- **Test :** Données propres dans exports.

## Partie 8 : Pipelines et traitement des données
- **Exemples :** Implémenté PriceValidationPipeline, DataCleaningPipeline, DatabasePipeline (SQLite), JsonWriterPipeline dans `pipelines.py`.
- **Activation :** Dans `settings.py`, ITEM_PIPELINES configuré avec priorités.
- **Test :** Crawl stocke dans DB, valide prix > 0.

## Partie 9 : Middlewares et settings avancés
- **Configuration :** Ajouté rotation User-Agent dans `middlewares.py`, DOWNLOAD_DELAY=3, ROBOTSTXT_OBEY=True dans `settings.py`.
- **Test :** Logs en DEBUG, retry automatique testé.

## Partie 10 : Projet complet (site e-commerce fictif)
- **Spider :** Amélioré books.py pour multi-catégories, extraction complète, export configurable.
- **Test :** `scrapy crawl books -o full_export.csv` → Couvre tout le site.

## Partie 11 : Bonnes pratiques
- Appliquées : Respect robots.txt, delays, documentation des fichiers.
- **Tests :** Utilisé scrapy shell pour déboguer sélecteurs.

## Partie 12 : Commandes Scrapy utiles
- Liste : `scrapy list`, `scrapy shell`, `scrapy crawl -o output.json`, ...

## Conclusion
TP completé ! Temps passé : ~5 heures. Voici le lien de mon repository GitHub qui contient l'intégralité de mon travail : [Lien vers le repository GitHub](https://github.com/AliAch04/Python-Data-Science-Labs/tree/main/TP6_Scrapy)
