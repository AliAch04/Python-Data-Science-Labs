import requests
from bs4 import BeautifulSoup
import csv
import time
from requests.exceptions import RequestException

def scrape_single_page(url, retry=3):
    """
    Scrape une seule page avec gestion d'erreurs et retry
    """
    for attempt in range(retry):
        try:
            # Faire la requête avec timeout
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Lève une exception si erreur HTTP
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            quotes_divs = soup.find_all('div', class_='quote')
            quotes_data = []
            
            for quote_div in quotes_divs:
                try:
                    text = quote_div.find('span', class_='text').text
                    author = quote_div.find('small', class_='author').text
                    tags = [tag.text for tag in quote_div.find_all('a', class_='tag')]
                    
                    quote_data = {
                        'text': text,
                        'author': author,
                        'tags': ', '.join(tags)
                    }
                    quotes_data.append(quote_data)
                    
                except AttributeError as e:
                    print(f"  ⚠ Erreur lors de l'extraction d'une citation: {e}")
                    continue
            
            # Trouver le lien "Next"
            next_button = soup.find('li', class_='next')
            next_page_url = None
            
            if next_button:
                next_link = next_button.find('a')
                if next_link:
                    next_page_url = "http://quotes.toscrape.com" + next_link['href']
            
            return quotes_data, next_page_url
            
        except RequestException as e:
            print(f"  ⚠ Tentative {attempt + 1}/{retry} échouée: {e}")
            if attempt < retry - 1:
                time.sleep(2)  # Attendre avant de réessayer
            else:
                print(f"  ✗ Échec après {retry} tentatives")
                return [], None
    
    return [], None

def scrape_all_pages(base_url, max_pages=None):
    """
    Scrape toutes les pages avec statistiques
    """
    all_quotes = []
    current_url = base_url
    page_count = 1
    errors = 0
    
    while current_url:
        print(f"📄 Page {page_count}...", end=" ")
        
        quotes, next_url = scrape_single_page(current_url)
        
        if quotes:
            all_quotes.extend(quotes)
            print(f"✓ {len(quotes)} citations")
        else:
            print("✗ Échec")
            errors += 1
        
        if max_pages and page_count >= max_pages:
            break
        
        current_url = next_url
        page_count += 1
        
        # Pause de politesse
        time.sleep(1)
    
    return all_quotes, errors

def save_to_csv(quotes_data, filename='quotes_final.csv'):
    """
    Sauvegarde avec gestion d'erreurs
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['text', 'author', 'tags']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for quote in quotes_data:
                writer.writerow(quote)
        
        print(f"✓ Données sauvegardées dans {filename}")
        return True
    except Exception as e:
        print(f"✗ Erreur lors de la sauvegarde: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("  BOT DE WEB SCRAPING - QUOTES TO SCRAPE")
    print("="*60)
    
    base_url = "http://quotes.toscrape.com/"
    
    start_time = time.time()
    
    all_quotes, errors = scrape_all_pages(base_url, max_pages=5)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "="*60)
    print("  RAPPORT FINAL")
    print("="*60)
    print(f"✓ Citations scrapées: {len(all_quotes)}")
    print(f"✗ Erreurs rencontrées: {errors}")
    print(f"⏱ Temps d'exécution: {duration:.2f} secondes")
    print(f"⚡ Vitesse: {len(all_quotes)/duration:.2f} citations/seconde")
    print("="*60)
    
    if all_quotes:
        save_to_csv(all_quotes)