import requests
from bs4 import BeautifulSoup

# 1. Faire une requête HTTP
url = "http://quotes.toscrape.com/"
response = requests.get(url)

# 2. Vérifier le statut de la requête
print(f"Status Code: {response.status_code}")

# 3. Parser le HTML
soup = BeautifulSoup(response.content, 'html.parser')

# 4. Afficher le titre de la page
print(f"Titre de la page: {soup.title.string}")

# 5. Afficher la structure HTML (extrait)
print("\nExtrait du HTML:")
print(soup.prettify()[:500])