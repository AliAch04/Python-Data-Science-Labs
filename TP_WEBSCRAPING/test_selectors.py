import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Méthode 1 : find() - Trouve le PREMIER élément
first_quote = soup.find('span', class_='text')
print("Première citation:", first_quote.text)

# Méthode 2 : find_all() - Trouve TOUS les éléments
all_quotes = soup.find_all('span', class_='text')
print(f"\nNombre total de citations: {len(all_quotes)}")

# Méthode 3 : select() - Utilise les sélecteurs CSS
quotes_css = soup.select('div.quote span.text')
print(f"Citations trouvées avec CSS selector: {len(quotes_css)}")

# Méthode 4 : Navigation dans l'arbre
first_quote_div = soup.find('div', class_='quote')
author = first_quote_div.find('small', class_='author')
print(f"\nAuteur de la première citation: {author.text}")