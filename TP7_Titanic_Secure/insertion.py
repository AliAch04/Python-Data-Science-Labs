import pandas as pd
import sqlite3
from data_encryption import DataEncryption
from datetime import datetime

def insert_titanic_data():
    """Fonction principale pour charger, chiffrer et insérer les données"""
    
    # 1. Charger le dataset
    print("=== ÉTAPE 1 : Chargement du dataset ===")
    df = pd.read_csv('titanic.csv')
    
    # Nettoyer les données
    df['Age'].fillna(df['Age'].median(), inplace=True)
    df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
    df['Cabin'].fillna('Unknown', inplace=True)
    df['Fare'].fillna(df['Fare'].median(), inplace=True)
    
    print(f"Nombre de passagers à insérer : {len(df)}")
    
    # 2. Initialiser le chiffrement
    print("\n=== ÉTAPE 2 : Initialisation du chiffrement ===")
    encryptor = DataEncryption()
    
    # 3. Chiffrer les colonnes sensibles
    print("\n=== ÉTAPE 3 : Chiffrement des données sensibles ===")
    colonnes_a_chiffrer = ['Name', 'Ticket', 'Cabin']
    
    for col in colonnes_a_chiffrer:
        df[f'{col}_encrypted'] = df[col].astype(str).apply(encryptor.encrypt)
        print(f"✓ Colonne {col} chiffrée")
    
    # 4. Connexion à la base de données
    print("\n=== ÉTAPE 4 : Connexion à la base de données ===")
    conn = sqlite3.connect('titanic_secure.db')
    cursor = conn.cursor()
    
    # Sauvegarder les métadonnées de chiffrement
    encryptor.save_metadata(conn)
    
    # 5. Insertion des données avec requêtes paramétrées
    print("\n=== ÉTAPE 5 : Insertion des données ===")
    
    insertion_reussies = 0
    insertion_echouees = 0
    
    for index, row in df.iterrows():
        try:
            # Requête paramétrée (SÉCURISÉE contre SQL injection)
            cursor.execute('''
                INSERT INTO passengers (
                    passenger_id, survived, pclass, name_encrypted, sex, age,
                    sibsp, parch, ticket_encrypted, fare, cabin_encrypted, embarked
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                int(row['PassengerId']),
                int(row['Survived']),
                int(row['Pclass']),
                row['Name_encrypted'],
                row['Sex'],
                float(row['Age']),
                int(row['SibSp']),
                int(row['Parch']),
                row['Ticket_encrypted'],
                float(row['Fare']),
                row['Cabin_encrypted'],
                row['Embarked']
            ))
            insertion_reussies += 1
            
            # Afficher progression tous les 100 enregistrements
            if (index + 1) % 100 == 0:
                print(f"  → {index + 1} passagers insérés...")
                
        except Exception as e:
            print(f"Erreur lors de l'insertion du passager {row['PassengerId']}: {e}")
            insertion_echouees += 1
    
    # 6. Valider les modifications
    conn.commit()
    
    print("\n=== RÉSUMÉ DE L'INSERTION ===")
    print(f"✓ Insertions réussies : {insertion_reussies}")
    print(f"✗ Insertions échouées : {insertion_echouees}")
    print(f"Total                 : {len(df)}")
    
    # 7. Vérification
    cursor.execute("SELECT COUNT(*) FROM passengers")
    count = cursor.fetchone()[0]
    print(f"\n=== Vérification : {count} passagers dans la base ===")
    
    # 8. Exemple de lecture et déchiffrement
    print("\n=== ÉTAPE 6 : Test de lecture et déchiffrement ===")
    cursor.execute("SELECT * FROM passengers LIMIT 3")
    passengers = cursor.fetchall()
    
    print("\nExemple de 3 passagers (données déchiffrées) :")
    for p in passengers:
        print(f"\nPassager ID: {p[0]}")
        print(f"  Survécu    : {'Oui' if p[1] == 1 else 'Non'}")
        print(f"  Classe     : {p[2]}")
        print(f"  Nom        : {encryptor.decrypt(p[3])}")
        print(f"  Sexe       : {p[4]}")
        print(f"  Âge        : {p[5]}")
        print(f"  Ticket     : {encryptor.decrypt(p[8])}")
        print(f"  Cabine     : {encryptor.decrypt(p[10])}")
    
    conn.close()
    print("\n=== Processus terminé avec succès ! ===")

if __name__ == "__main__":
    insert_titanic_data()