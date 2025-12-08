import sqlite3
import os

def fix_urgence():
    # Connexion à la base de données
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    try:
        # 1. Vérifier la structure de la table
        cursor.execute("PRAGMA table_info(medecin_ordonnance)")
        columns = cursor.fetchall()
        print("Structure de medecin_ordonnance:")
        for col in columns:
            print(f"  {col[1]} ({col[2]}) - Nullable: {not col[3]}")
        
        # 2. Insérer des données avec notes
        ordonnances_urgence = [
            (1, 1, '2024-01-15', 'Traitement urgence', 7, 'Notes médicales standard'),
            (2, 2, '2024-01-16', 'Antibiotique urgence', 10, 'Suivi nécessaire'),
            (3, 3, '2024-01-17', 'Antidouleur urgence', 5, 'Contrôle dans 48h')
        ]
        
        for ord in ordonnances_urgence:
            cursor.execute('''
                INSERT OR IGNORE INTO medecin_ordonnance 
                (patient_id, medecin_id, date_prescription, instructions, duree_traitement, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ord)
        
        # 3. Créer les partages
        cursor.execute('''
            INSERT OR IGNORE INTO ordonnance_partage 
            (ordonnance_id, pharmacien_id, date_partage, est_actif)
            SELECT id, 1, date('now'), 1 
            FROM medecin_ordonnance 
            WHERE id NOT IN (SELECT ordonnance_id FROM ordonnance_partage)
        ''')
        
        conn.commit()
        print("✅ Données d'urgence insérées avec succès")
        
        # 4. Vérification
        cursor.execute("SELECT COUNT(*) FROM medecin_ordonnance")
        count = cursor.fetchone()[0]
        print(f"📊 Ordonnances totales: {count}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_urgence()