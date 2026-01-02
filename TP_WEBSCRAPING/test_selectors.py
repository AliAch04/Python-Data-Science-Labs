import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Trouver les 3 premières divs contenant les citations
quotes_divs = soup.find_all('div', class_='quote')[:3]

print("Les 3 premières citations :\n")

for i, quote_div in enumerate(quotes_divs, 1):
    # Texte de la citation
    text_span = quote_div.find('span', class_='text')
    text = text_span.text if text_span else "Non trouve"
    
    # Auteur
    author_span = quote_div.find('small', class_='author')
    author = author_span.text if author_span else "Non trouve"
    
    # Premier tag (dans div.tags > a.tag)
    tags_div = quote_div.find('div', class_='tags')
    first_tag = "Aucun tag"
    if tags_div:
        first_tag_tag = tags_div.find('a', class_='tag')
        if first_tag_tag:
            first_tag = first_tag_tag.text
    
    # Affichage
    print(f"Citation {i} :")
    print(f"  Texte : {text}")
    print(f"  Auteur : {author}")
    print(f"  Premier tag : {first_tag}")
