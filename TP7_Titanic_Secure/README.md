# TP7 : Gestion Sécurisée des Données du Titanic

## Intro
L'objectif est de gérer de manière sécurisée les données du dataset Titanic :
- Création d'une base de données SQLite.
- Chiffrement des données sensibles (nom, ticket, cabine) avec AES via la bibliothèque `cryptography`.
- Insertion des données chiffrées dans la base avec protection contre les injections SQL.
- Analyse des données avec une classe `TitanicDatabase` pour des requêtes SQL avancées, statistiques agrégées, recherche avec déchiffrement, et affichage formaté.

## Fichiers Inclus
- **creation.py** : Script pour créer la base de données SQLite (`titanic_secure.db`) et la table `passengers`.
- **chiffrement.py** : Script pour générer la clé de chiffrement (`encryption_key.key`), tester le chiffrement/déchiffrement AES.
- **insertion.py** : Script pour charger le CSV, nettoyer les données, chiffrer les colonnes sensibles, insérer dans la base, et tester le déchiffrement.
- **analyse.py** : Module d'analyse avec la classe `TitanicDatabase` pour afficher des passagers, calculer des statistiques de survie, et rechercher par nom.
- **titanic.csv** : Dataset source (891 passagers).
- **encryption_key.key** : Clé de chiffrement AES (fichier sensible !).

**Note** : La base de données générée (`titanic_secure.db`) n'est pas incluse dans le livrable car elle est créée lors de l'exécution. De même, `encryption_key.key` est généré par `chiffrement.py`.


## Les Commandes d'exécution

1. **Création de la base** :
   ```
   python creation.py
   ```
   Creation de `titanic_secure.db` et la table `passengers`.

2. **Génération et test du chiffrement** :
   ```
   python chiffrement.py
   ```
   Génère `encryption_key.key` et teste le chiffrement.

3. **Insertion des données** :
   ```
   python insertion.py
   ```
   Charge, nettoie, chiffre et insère les données. Affiche un résumé 

4. **Analyse des données** :
   ```
   python analyse.py
   ```
   Affiche des exemples de passagers, statistiques de survie, et une recherche de test (ex. : "Smith").


## Outputs de Test
Voici les outputs console (exécutés sur mon environnement `/venv`).

### Output de `chiffrement.py`
```
=== Nouvelle clé de chiffrement générée et sauvegardée ===
=== Test de Chiffrement ===
Message original : John Smith
Message chiffré : gAAAAABpaq-QhgjSjz5k0diLOZnoaDzdbHFr64zMXOi0RmIb7H...
Message déchiffré : John Smith
Validation : True
```

### Output de `insertion.py`
```
=== ÉTAPE 1 : Chargement du dataset ===
D:\Py_Labs\Python-Data-Science-Labs\TP7_Titanic_Secure\insertion.py:14: FutureWarning: A value is trying to be set on a copy of a DataFrame or Series through chained assignment using an inplace method.
The behavior will change in pandas 3.0. This inplace method will never work because the intermediate object on which we are setting values always behaves as a copy.
For example, when doing 'df[col].method(value, inplace=True)', try using 'df.method({col: value}, inplace=True)' or df[col] = df[col].method(value) instead, to perform the operation inplace on the original object.
  df['Age'].fillna(df['Age'].median(), inplace=True)
D:\Py_Labs\Python-Data-Science-Labs\TP7_Titanic_Secure\insertion.py:15: FutureWarning: A value is trying to be set on a copy of a DataFrame or Series through chained assignment using an inplace method.
The behavior will change in pandas 3.0. This inplace method will never work because the intermediate object on which we are setting values always behaves as a copy.
For example, when doing 'df[col].method(value, inplace=True)', try using 'df.method({col: value}, inplace=True)' or df[col] = df[col].method(value) instead, to perform the operation inplace on the original object.
  df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
D:\Py_Labs\Python-Data-Science-Labs\TP7_Titanic_Secure\insertion.py:16: FutureWarning: A value is trying to be set on a copy of a DataFrame or Series through chained assignment using an inplace method.
The behavior will change in pandas 3.0. This inplace method will never work because the intermediate object on which we are setting values always behaves as a copy.
For example, when doing 'df[col].method(value, inplace=True)', try using 'df.method({col: value}, inplace=True)' or df[col] = df[col].method(value) instead, to perform the operation inplace on the original object.
  df['Cabin'].fillna('Unknown', inplace=True)
D:\Py_Labs\Python-Data-Science-Labs\TP7_Titanic_Secure\insertion.py:17: FutureWarning: A value is trying to be set on a copy of a DataFrame or Series through chained assignment using an inplace method.
The behavior will change in pandas 3.0. This inplace method will never work because the intermediate object on which we are setting values always behaves as a copy.
For example, when doing 'df[col].method(value, inplace=True)', try using 'df.method({col: value}, inplace=True)' or df[col] = df[col].method(value) instead, to perform the operation inplace on the original object.
  df['Fare'].fillna(df['Fare'].median(), inplace=True)
Nombre de passagers à insérer : 891
=== ÉTAPE 2 : Initialisation du chiffrement ===
=== Clé de chiffrement chargée depuis encryption_key.key ===
=== ÉTAPE 3 : Chiffrement des données sensibles ===
✓ Colonne Name chiffrée
✓ Colonne Ticket chiffrée
✓ Colonne Cabin chiffrée
=== ÉTAPE 4 : Connexion à la base de données ===
=== Métadonnées de chiffrement sauvegardées ===
=== ÉTAPE 5 : Insertion des données ===
  → 100 passagers insérés...
  → 200 passagers insérés...
  → 300 passagers insérés...
  → 400 passagers insérés...
  → 500 passagers insérés...
  → 600 passagers insérés...
  → 700 passagers insérés...
  → 800 passagers insérés...
=== RÉSUMÉ DE L'INSERTION ===
✓ Insertions réussies : 891
✗ Insertions échouées : 0
Total : 891
=== Vérification : 891 passagers dans la base ===
=== ÉTAPE 6 : Test de lecture et déchiffrement ===
Exemple de 3 passagers (données déchiffrées) :
Passager ID: 1
  Survécu : Non
  Classe : 3
  Nom : Braund, Mr. Owen Harris
  Sexe : male
  Âge : 22.0
  Ticket : A/5 21171
  Cabine : Unknown
Passager ID: 2
  Survécu : Oui
  Classe : 1
  Nom : Cumings, Mrs. John Bradley (Florence Briggs Thayer)
  Sexe : female
  Âge : 38.0
  Ticket : PC 17599
  Cabine : C85
Passager ID: 3
  Survécu : Oui
  Classe : 3
  Nom : Heikkinen, Miss. Laina
  Sexe : female
  Âge : 26.0
  Ticket : STON/O2. 3101282
  Cabine : Unknown
=== Processus terminé avec succès ! ===
```

### Output de `analyse.py`
```
=== Clé de chiffrement chargée depuis encryption_key.key ===
=== 3 PREMIERS PASSAGERS ===
============================================================
Passager ID : 1
Survécu : ✗ Non
Classe : 3
Nom : Braund, Mr. Owen Harris
Sexe : male
Âge : 22.0 ans
Ticket : A/5 21171
Prix : 7.25£
Cabine : Unknown
Embarquement: S
============================================================
Passager ID : 2
Survécu : ✓ Oui
Classe : 1
Nom : Cumings, Mrs. John Bradley (Florence Briggs Thayer)
Sexe : female
Âge : 38.0 ans
Ticket : PC 17599
Prix : 71.28£
Cabine : C85
Embarquement: C
============================================================
Passager ID : 3
Survécu : ✓ Oui
Classe : 3
Nom : Heikkinen, Miss. Laina
Sexe : female
Âge : 26.0 ans
Ticket : STON/O2. 3101282
Prix : 7.92£
Cabine : Unknown
Embarquement: S
=== STATISTIQUES DE SURVIE ===
Taux de survie global : 38.38%
Par sexe :
  female: 233/314 survécus (74.20%)
  male: 109/577 survécus (18.89%)
Par classe :
  Classe 1: 136/216 survécus (62.96%)
  Classe 2: 87/184 survécus (47.28%)
  Classe 3: 119/491 survécus (24.24%)
=== Recherche de 'Smith' ===
Trouvé 7 résultat(s) :
  ID: 166 | Nom: Goldsmith, Master. Frank John William "Frankie"
  Survécu: Oui | Classe: 3 | Âge: 9.0
  ID: 175 | Nom: Smith, Mr. James Clinch
  Survécu: Non | Classe: 1 | Âge: 56.0
  ID: 261 | Nom: Smith, Mr. Thomas
  Survécu: Non | Classe: 3 | Âge: 28.0
  ID: 285 | Nom: Smith, Mr. Richard William
  Survécu: Non | Classe: 1 | Âge: 28.0
  ID: 329 | Nom: Goldsmith, Mrs. Frank John (Emily Alice Brown)
  Survécu: Oui | Classe: 3 | Âge: 31.0
  ID: 347 | Nom: Smith, Miss. Marion Elsie
  Survécu: Oui | Classe: 2 | Âge: 40.0
  ID: 549 | Nom: Goldsmith, Mr. Frank John
  Survécu: Non | Classe: 3 | Âge: 33.0
```

## Auteur
- Ali ACHENAN, Master IAOC M1
