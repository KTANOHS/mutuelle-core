import sqlite3
import os
from datetime import datetime, timedelta

def fix_urgence_v2():
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
        
        # 2. Dates pour les ordonnances
        date_prescription = datetime.now().strftime('%Y-%m-%d')
        date_expiration = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        date_creation = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 3. Insérer des données avec la structure correcte
        ordonnances_urgence = [
            # (numero, date_prescription, date_expiration, date_creation, date_modification, 
            # type_ordonnance, diagnostic, medicaments, posologie, duree_traitement,
            # renouvelable, nombre_renouvellements, renouvellements_effectues, statut,
            # est_urgent, notes, partage_effectue, medecin_id, patient_id)
            (
                f"ORD-001-{datetime.now().strftime('%Y%m%d')}",
                date_prescription, date_expiration, date_creation, date_creation,
                'STANDARD', 'Infection bactérienne', 
                'Amoxicilline 500mg', '1 comprimé 3 fois par jour', 7,
                0, 0, 0, 'ACTIVE', 1, 
                'Traitement antibiotique pour infection - Suivi dans 7 jours',
                1, 1, 1
            ),
            (
                f"ORD-002-{datetime.now().strftime('%Y%m%d')}",
                date_prescription, date_expiration, date_creation, date_creation,
                'STANDARD', 'Douleurs inflammatoires',
                'Ibuprofène 400mg', '1 comprimé 3 fois par jour après les repas', 5,
                0, 0, 0, 'ACTIVE', 0,
                'Antidouleur et anti-inflammatoire - Contre-indication estomac vide',
                1, 2, 2
            ),
            (
                f"ORD-003-{datetime.now().strftime('%Y%m%d')}",
                date_prescription, date_expiration, date_creation, date_creation,
                'CHRONIQUE', 'Hypertension artérielle',
                'Amlodipine 5mg', '1 comprimé par jour le matin', 30,
                1, 2, 0, 'ACTIVE', 0,
                'Traitement chronique hypertension - Contrôle tensionnel mensuel',
                1, 3, 3
            )
        ]
        
        for ord in ordonnances_urgence:
            cursor.execute('''
                INSERT OR IGNORE INTO medecin_ordonnance 
                (numero, date_prescription, date_expiration, date_creation, date_modification,
                 type_ordonnance, diagnostic, medicaments, posologie, duree_traitement,
                 renouvelable, nombre_renouvellements, renouvellements_effectues, statut,
                 est_urgent, notes, partage_effectue, medecin_id, patient_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', ord)
        
        print("✅ Données d'urgence insérées avec succès")
        
        # 4. Vérifier si la table ordonnance_partage existe et a la bonne structure
        try:
            cursor.execute("PRAGMA table_info(ordonnance_partage)")
            partage_columns = cursor.fetchall()
            print("\nStructure de ordonnance_partage:")
            for col in partage_columns:
                print(f"  {col[1]} ({col[2]}) - Nullable: {not col[3]}")
            
            # 5. Créer les partages
            cursor.execute('''
                INSERT OR IGNORE INTO ordonnance_partage 
                (ordonnance_id, pharmacien_id, date_partage, est_actif)
                SELECT id, 1, date('now'), 1 
                FROM medecin_ordonnance 
                WHERE id NOT IN (SELECT ordonnance_id FROM ordonnance_partage)
            ''')
            print("✅ Partages créés avec succès")
            
        except Exception as e:
            print(f"⚠️  Problème avec ordonnance_partage: {e}")
            print("📋 Création manuelle des partages...")
            
            # Création manuelle des partages
            cursor.execute("SELECT id FROM medecin_ordonnance ORDER BY id DESC LIMIT 3")
            ordonnance_ids = cursor.fetchall()
            
            for ord_id in ordonnance_ids:
                cursor.execute('''
                    INSERT OR IGNORE INTO ordonnance_partage 
                    (ordonnance_id, pharmacien_id, date_partage, est_actif)
                    VALUES (?, 1, ?, 1)
                ''', (ord_id[0], date_prescription))
        
        conn.commit()
        
        # 6. Vérification finale
        cursor.execute("SELECT COUNT(*) FROM medecin_ordonnance")
        count_ord = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ordonnance_partage")
        count_partage = cursor.fetchone()[0]
        
        print(f"\n📊 VÉRIFICATION FINALE:")
        print(f"📝 Ordonnances totales: {count_ord}")
        print(f"🔗 Partages créés: {count_partage}")
        
        # Afficher les dernières ordonnances
        cursor.execute('''
            SELECT o.id, o.numero, p.nom, p.prenom, m.nom, o.statut
            FROM medecin_ordonnance o
            JOIN patient_patient p ON o.patient_id = p.id
            JOIN medecin_medecin m ON o.medecin_id = m.id
            ORDER BY o.id DESC LIMIT 3
        ''')
        ordonnances = cursor.fetchall()
        
        print(f"\n📋 DERNIÈRES ORDONNANCES CRÉÉES:")
        for ord in ordonnances:
            print(f"   #{ord[0]} - {ord[1]} - Patient: {ord[3]} {ord[2]} - Médecin: {ord[4]} - Statut: {ord[5]}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_urgence_v2()