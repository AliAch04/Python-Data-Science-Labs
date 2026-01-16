import sqlite3
from chiffrement import DataEncryption

class TitanicDatabase:
    """Classe pour interroger la base de données sécurisée"""
    
    def __init__(self, db_file='titanic_secure.db'):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.encryptor = DataEncryption()
    
    def rechercher_par_nom(self, nom_recherche):
        """Recherche un passager par nom (nécessite déchiffrement)"""
        print(f"\n=== Recherche de '{nom_recherche}' ===")
        
        # Récupérer tous les passagers (car les noms sont chiffrés)
        self.cursor.execute("SELECT * FROM passengers")
        all_passengers = self.cursor.fetchall()
        
        resultats = []
        for p in all_passengers:
            nom_dechiffre = self.encryptor.decrypt(p[3])
            if nom_recherche.lower() in nom_dechiffre.lower():
                resultats.append((p, nom_dechiffre))
        
        if resultats:
            print(f"Trouvé {len(resultats)} résultat(s) :")
            for p, nom in resultats:
                print(f"\n  ID: {p[0]} | Nom: {nom}")
                print(f"  Survécu: {'Oui' if p[1] == 1 else 'Non'} | Classe: {p[2]} | Âge: {p[5]}")
        else:
            print("Aucun résultat trouvé")
        
        return resultats
    
    def statistiques_survie(self):
        """Affiche des statistiques sur la survie"""
        print("\n=== STATISTIQUES DE SURVIE ===")
        
        # Taux de survie global
        self.cursor.execute("SELECT AVG(survived) * 100 FROM passengers")
        taux_global = self.cursor.fetchone()[0]
        print(f"\nTaux de survie global : {taux_global:.2f}%")
        
        # Par sexe
        print("\nPar sexe :")
        self.cursor.execute("""
            SELECT sex, 
                   COUNT(*) as total,
                   SUM(survived) as survecus,
                   AVG(survived) * 100 as taux
            FROM passengers 
            GROUP BY sex
        """)
        for row in self.cursor.fetchall():
            print(f"  {row[0]}: {row[2]}/{row[1]} survécus ({row[3]:.2f}%)")
        
        # Par classe
        print("\nPar classe :")
        self.cursor.execute("""
            SELECT pclass,
                   COUNT(*) as total,
                   SUM(survived) as survecus,
                   AVG(survived) * 100 as taux
            FROM passengers 
            GROUP BY pclass
            ORDER BY pclass
        """)
        for row in self.cursor.fetchall():
            print(f"  Classe {row[0]}: {row[2]}/{row[1]} survécus ({row[3]:.2f}%)")
    
    def afficher_passagers(self, limite=5):
        """Affiche les n premiers passagers avec déchiffrement"""
        print(f"\n=== {limite} PREMIERS PASSAGERS ===")
        
        self.cursor.execute(f"SELECT * FROM passengers LIMIT {limite}")
        passengers = self.cursor.fetchall()
        
        for p in passengers:
            print(f"\n{'='*60}")
            print(f"Passager ID : {p[0]}")
            print(f"Survécu     : {'✓ Oui' if p[1] == 1 else '✗ Non'}")
            print(f"Classe      : {p[2]}")
            print(f"Nom         : {self.encryptor.decrypt(p[3])}")
            print(f"Sexe        : {p[4]}")
            print(f"Âge         : {p[5]} ans")
            print(f"Ticket      : {self.encryptor.decrypt(p[8])}")
            print(f"Prix        : {p[9]:.2f}£")
            print(f"Cabine      : {self.encryptor.decrypt(p[10])}")
            print(f"Embarquement: {p[11]}")
    
    def close(self):
        self.conn.close()

# Utilisation
if __name__ == "__main__":
    db = TitanicDatabase()
    
    # Afficher quelques passagers
    db.afficher_passagers(3)
    
    # Statistiques
    db.statistiques_survie()
    
    # Recherche
    db.rechercher_par_nom("Smith")
    
    db.close()