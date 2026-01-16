from cryptography.fernet import Fernet
import os
import json
from datetime import datetime

class DataEncryption:
    """Classe pour gérer le chiffrement/déchiffrement des données sensibles"""
    
    def __init__(self, key_file='encryption_key.key'):
        self.key_file = key_file
        self.key = self._load_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _load_or_create_key(self):
        """Charge la clé existante ou en crée une nouvelle"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                key = f.read()
            print(f"=== Clé de chiffrement chargée depuis {self.key_file} ===")
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            # Restreindre les permissions du fichier (Unix/Linux)
            try:
                os.chmod(self.key_file, 0o600)
            except:
                pass
            print(f"=== Nouvelle clé de chiffrement générée et sauvegardée ===")
        return key
    
    def encrypt(self, data):
        """Chiffre une chaîne de caractères"""
        if data is None or data == '':
            return ''
        if isinstance(data, str):
            data = data.encode('utf-8')
        encrypted = self.cipher.encrypt(data)
        return encrypted.decode('utf-8')
    
    def decrypt(self, encrypted_data):
        """Déchiffre une chaîne de caractères"""
        if encrypted_data is None or encrypted_data == '':
            return ''
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode('utf-8')
        decrypted = self.cipher.decrypt(encrypted_data)
        return decrypted.decode('utf-8')
    
    def encrypt_dataframe_columns(self, df, columns):
        """Chiffre les colonnes spécifiées d'un DataFrame"""
        df_encrypted = df.copy()
        for col in columns:
            if col in df.columns:
                print(f"Chiffrement de la colonne : {col}")
                df_encrypted[f'{col}_encrypted'] = df[col].astype(str).apply(self.encrypt)
        return df_encrypted
    
    def save_metadata(self, conn):
        """Sauvegarde les métadonnées de chiffrement dans la base"""
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO encryption_metadata (algorithm, description)
            VALUES (?, ?)
        ''', ('AES-128 (Fernet)', 'Chiffrement symétrique avec authentification HMAC'))
        conn.commit()
        print("=== Métadonnées de chiffrement sauvegardées ===")

# Démonstration du chiffrement
if __name__ == "__main__":
    # Créer une instance de chiffrement
    encryptor = DataEncryption()
    
    # Test de chiffrement/déchiffrement
    message_original = "John Smith"
    message_chiffre = encryptor.encrypt(message_original)
    message_dechiffre = encryptor.decrypt(message_chiffre)
    
    print("\n=== Test de Chiffrement ===")
    print(f"Message original  : {message_original}")
    print(f"Message chiffré   : {message_chiffre[:50]}...")
    print(f"Message déchiffré : {message_dechiffre}")
    print(f"Validation        : {message_original == message_dechiffre}")