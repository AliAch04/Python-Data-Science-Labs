import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_single_page(url):
    """
    Scrape une seule page de citations
    """
    # Faire la requête
    response = requests.get(url)
    
    # Vérifier le succès
    if response.status_code != 200:
        print(f"Erreur: Status code {response.status_code}")
        return []
    
    # Parser le HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Trouver toutes les citations
    quotes_divs = soup.find_all('div', class_='quote')
    
    quotes_data = []
    
    for quote_div in quotes_divs:
        # Extraire le texte de la citation
        text = quote_div.find('span', class_='text').text
        
        # Extraire l'auteur
        author = quote_div.find('small', class_='author').text
        
        # Extraire les tags
        tags = [tag.text for tag in quote_div.find_all('a', class_='tag')]
        
        # Créer un dictionnaire
        quote_data = {
            'text': text,
            'author': author,
            'tags': ', '.join(tags)
        }
        
        quotes_data.append(quote_data)
    
    return quotes_data

# Test de la fonction
if __name__ == "__main__":
    # Début du chronomètre
    start_time = time.time()
    
    url = "http://quotes.toscrape.com/"
    quotes = scrape_single_page(url)
    
    print(f"Nombre de citations scrapées: {len(quotes)}")
    print("\nPremière citation:")
    print(quotes[0])
    
    # Fin du chronomètre
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Affichage du temps d'exécution
    print(f"\n{'='*50}")
    print(f"Temps d'exécution: {execution_time:.2f} secondes")
    print(f"Temps d'exécution manuel: 4 min 27 sec (267 secondes)")
    print(f"Différence: {267 - execution_time:.2f} secondes de gain")
    print(f"Rapport de performance: {267/execution_time:.1f}x plus rapide")