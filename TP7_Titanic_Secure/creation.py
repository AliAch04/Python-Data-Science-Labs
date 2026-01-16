import sqlite3

# Connexion à la base de données (création si elle n'existe pas)
conn = sqlite3.connect('titanic_secure.db')
cursor = conn.cursor()

# Créer la table passengers
cursor.execute('''
CREATE TABLE IF NOT EXISTS passengers (
    passenger_id INTEGER PRIMARY KEY,
    survived INTEGER NOT NULL,
    pclass INTEGER NOT NULL,
    name_encrypted TEXT NOT NULL,
    sex TEXT NOT NULL,
    age REAL,
    sibsp INTEGER,
    parch INTEGER,
    ticket_encrypted TEXT NOT NULL,
    fare REAL,
    cabin_encrypted TEXT,
    embarked TEXT
)
''')

# Créer une table pour stocker les métadonnées de chiffrement
cursor.execute('''
CREATE TABLE IF NOT EXISTS encryption_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    algorithm TEXT NOT NULL,
    key_creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
)
''')

conn.commit()
print("=== Base de données créée avec succès ===")
print("Table 'passengers' créée")
print("Table 'encryption_metadata' créée")

# Vérifier la structure de la table
cursor.execute("PRAGMA table_info(passengers)")
columns = cursor.fetchall()
print("\n=== Structure de la table passengers ===")
for col in columns:
    print(f"{col[1]} - {col[2]}")

conn.close()