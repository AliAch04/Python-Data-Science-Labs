import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_single_page(url):
    """
    Scrape une seule page de citations
    """
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erreur: Status code {response.status_code}")
        return [], None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extraire les citations
    quotes_divs = soup.find_all('div', class_='quote')
    quotes_data = []
    
    for quote_div in quotes_divs:
        text = quote_div.find('span', class_='text').text
        author = quote_div.find('small', class_='author').text
        tags = [tag.text for tag in quote_div.find_all('a', class_='tag')]
        
        quote_data = {
            'text': text,
            'author': author,
            'tags': ', '.join(tags)
        }
        quotes_data.append(quote_data)
    
    # Trouver le lien "Next"
    next_button = soup.find('li', class_='next')
    next_page_url = None
    
    if next_button:
        next_link = next_button.find('a')
        if next_link:
            next_page_url = "http://quotes.toscrape.com" + next_link['href']
    
    return quotes_data, next_page_url

def scrape_all_pages(base_url, max_pages=None):
    """
    Scrape toutes les pages du site
    """
    all_quotes = []
    current_url = base_url
    page_count = 1
    
    while current_url:
        print(f"Scraping page {page_count}...")
        
        # Scraper la page actuelle
        quotes, next_url = scrape_single_page(current_url)
        all_quotes.extend(quotes)
        
        print(f"  → {len(quotes)} citations trouvées")
        
        # Vérifier la limite de pages
        if max_pages and page_count >= max_pages:
            print(f"Limite de {max_pages} pages atteinte")
            break
        
        # Passer à la page suivante
        current_url = next_url
        page_count += 1
        
        # Pause de politesse (ne pas surcharger le serveur)
        time.sleep(1)
    
    return all_quotes

def save_to_csv(quotes_data, filename='quotes_all.csv'):
    """
    Sauvegarde les citations dans un fichier CSV
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['text', 'author', 'tags']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for quote in quotes_data:
            writer.writerow(quote)
    
    print(f"\nDonnées sauvegardées dans {filename}")

# Exécution principale
if __name__ == "__main__":
    base_url = "http://quotes.toscrape.com/"
    
    print("Démarrage du scraping...")
    start_time = time.time()
    
    # Scraper toutes les pages (limité à 3 pages pour le test)
    all_quotes = scrape_all_pages(base_url, max_pages=3)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n{'='*50}")
    print(f"Scraping terminé !")
    print(f"Total de citations: {len(all_quotes)}")
    print(f"Temps d'exécution: {duration:.2f} secondes")
    
    # Ajout de la comparaison avec votre temps manuel
    print(f"Temps d'exécution manuel (1 page): 4 min 27 sec (267 secondes)")
    
    # Pour 3 pages, votre temps manuel serait d'environ 3 x 267 = 801 secondes
    manual_time_for_3_pages = 3 * 267
    print(f"Temps manuel estimé pour {len(all_quotes)} citations: {manual_time_for_3_pages} secondes")
    print(f"Différence: {manual_time_for_3_pages - duration:.2f} secondes de gain")
    print(f"Rapport de performance: {manual_time_for_3_pages/duration:.1f}x plus rapide")
    print(f"{'='*50}")
    
    # Sauvegarder les données
    save_to_csv(all_quotes)