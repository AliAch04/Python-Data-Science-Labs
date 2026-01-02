import csv
from collections import Counter

def analyze_quotes(filename='quotes_final.csv'):
    """
    Analyse les citations scrapées
    """
    quotes = []
    authors = []
    all_tags = []
    
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            quotes.append(row['text'])
            authors.append(row['author'])
            if row['tags']:
                all_tags.extend(row['tags'].split(', '))
    
    print("="*60)
    print("  ANALYSE DES DONNÉES SCRAPÉES")
    print("="*60)
    
    print(f"\n Statistiques générales:")
    print(f"  • Nombre total de citations: {len(quotes)}")
    print(f"  • Nombre d'auteurs uniques: {len(set(authors))}")
    print(f"  • Nombre de tags uniques: {len(set(all_tags))}")
    
    print(f"\n Top 5 auteurs les plus cités:")
    author_counts = Counter(authors)
    for author, count in author_counts.most_common(5):
        print(f"  {count:2d}× {author}")
    
    print(f"\n Top 10 tags les plus utilisés:")
    tag_counts = Counter(all_tags)
    for tag, count in tag_counts.most_common(10):
        print(f"  {count:2d}× {tag}")
    
    print(f"\n Citation la plus longue:")
    longest = max(quotes, key=len)
    print(f"  {longest[:100]}...")
    print(f"  ({len(longest)} caractères)")
    
    print(f"\n Citation la plus courte:")
    shortest = min(quotes, key=len)
    print(f"  {shortest}")
    print(f"  ({len(shortest)} caractères)")

if __name__ == "__main__":
    analyze_quotes()