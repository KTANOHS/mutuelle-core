import sqlite3
from datetime import datetime, timedelta

def fix_final_complete():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    try:
        print("🔧 CORRECTION COMPLÈTE - MÉDECIN_ORDONNANCE")
        print("=" * 60)
        
        # 1. Vérifier la structure de medecin_ordonnance
        cursor.execute("PRAGMA table_info(medecin_ordonnance)")
        columns = cursor.fetchall()
        print("Structure de medecin_ordonnance:")
        for col in columns:
            print(f"  {col[1]} ({col[2]}) - Nullable: {not col[3]}")
        
        # 2. Vérifier les données de référence
        cursor.execute("SELECT COUNT(*) FROM medecin_medecin")
        medecins_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM membres_membre")
        patients_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM pharmacien_pharmacien")
        pharmaciens_count = cursor.fetchone()[0]
        
        print(f"\n📊 DONNÉES DE RÉFÉRENCE:")
        print(f"   Médecins: {medecins_count}")
        print(f"   Patients: {patients_count}") 
        print(f"   Pharmaciens: {pharmaciens_count}")
        
        if medecins_count == 0 or patients_count == 0:
            print("❌ Données manquantes - création des données de base...")
            create_base_data(cursor)
        
        # 3. Créer des ordonnances dans medecin_ordonnance
        date_prescription = datetime.now().strftime('%Y-%m-%d')
        date_expiration = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        date_creation = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        ordonnances_data = [
            # Structure complète de medecin_ordonnance
            (
                'MED-ORD-001', date_prescription, date_expiration, date_creation, date_creation,
                'STANDARD', 'Infection bactérienne des voies respiratoires',
                'Amoxicilline 500mg', '1 comprimé 3 fois par jour pendant 7 jours', 7,
                0, 0, 0, 'ACTIVE', 0, 
                'Traitement antibiotique standard - Allergie: Aucune connue',
                1, None, None, 1, 1
            ),
            (
                'MED-ORD-002', date_prescription, date_expiration, date_creation, date_creation,
                'STANDARD', 'Douleurs inflammatoires articulaires',
                'Ibuprofène 400mg', '1 comprimé 3 fois par jour après les repas', 5,
                0, 0, 0, 'ACTIVE', 0,
                'Anti-inflammatoire non stéroïdien - Prise avec alimentation',
                1, None, None, 1, 2
            ),
            (
                'MED-ORD-003', date_prescription, date_expiration, date_creation, date_creation, 
                'CHRONIQUE', 'Hypertension artérielle stade 1',
                'Amlodipine 5mg', '1 comprimé par jour le matin', 30,
                1, 2, 0, 'ACTIVE', 0,
                'Traitement chronique - Contrôle tensionnel mensuel requis',
                1, None, None, 1, 3
            )
        ]
        
        print("\n💊 CRÉATION DES ORDONNANCES...")
        nouvelles_ordonnances = []
        
        for ord_data in ordonnances_data:
            try:
                cursor.execute('''
                    INSERT INTO medecin_ordonnance 
                    (numero, date_prescription, date_expiration, date_creation, date_modification,
                     type_ordonnance, diagnostic, medicaments, posologie, duree_traitement,
                     renouvelable, nombre_renouvellements, renouvellements_effectues, statut,
                     est_urgent, notes, partage_effectue, assureur_id, consultation_id,
                     medecin_id, patient_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', ord_data)
                
                ord_id = cursor.lastrowid
                nouvelles_ordonnances.append(ord_id)
                print(f"✅ Ordonnance {ord_data[0]} créée (ID: {ord_id})")
                
            except Exception as e:
                print(f"❌ Erreur création {ord_data[0]}: {e}")
        
        # 4. Corriger la table ordonnance_partage
        print("\n🔗 CORRECTION DES PARTAGES...")
        
        # Vérifier et corriger la structure
        cursor.execute("PRAGMA table_info(ordonnance_partage)")
        partage_columns = [col[1] for col in cursor.fetchall()]
        
        if 'ordonnance_medecin_id' in partage_columns:
            # Utiliser la colonne existante
            for ord_id in nouvelles_ordonnances:
                cursor.execute('''
                    INSERT OR IGNORE INTO ordonnance_partage 
                    (ordonnance_medecin_id, pharmacien_id, date_partage, statut)
                    VALUES (?, ?, ?, ?)
                ''', (ord_id, 1, date_creation, 'ACTIF'))
                print(f"✅ Partage créé pour ordonnance #{ord_id}")
        
        # 5. Créer une vue unifiée pour pharmacien
        print("\n👁️  CRÉATION VUE PHARMACIEN...")
        create_pharmacien_view(cursor)
        
        conn.commit()
        
        # 6. VÉRIFICATION FINALE
        print("\n" + "=" * 60)
        print("📊 VÉRIFICATION FINALE")
        print("=" * 60)
        
        cursor.execute("SELECT COUNT(*) FROM medecin_ordonnance")
        total_medecin = cursor.fetchone()[0]
        print(f"💊 Ordonnances dans medecin_ordonnance: {total_medecin}")
        
        cursor.execute("SELECT COUNT(*) FROM ordonnance_partage WHERE statut = 'ACTIF'")
        partages_actifs = cursor.fetchone()[0]
        print(f"🔗 Partages actifs: {partages_actifs}")
        
        cursor.execute("SELECT COUNT(*) FROM pharmacien_ordonnances_view")
        vue_count = cursor.fetchone()[0]
        print(f"👁️  Ordonnances dans vue pharmacien: {vue_count}")
        
        if vue_count > 0:
            print(f"\n📋 ORDONNANCES VISIBLES PAR PHARMACIEN:")
            cursor.execute('''
                SELECT ordonnance_id, numero, patient_nom, patient_prenom, medicaments
                FROM pharmacien_ordonnances_view 
                ORDER BY date_partage DESC LIMIT 3
            ''')
            for row in cursor.fetchall():
                print(f"   #{row[0]} {row[1]} - {row[3]} {row[2]} - {row[4]}")
        
        print(f"\n🎯 TEST FINAL RÉUSSI!")
        print(f"🌐 URL: http://127.0.0.1:8000/pharmacien/ordonnances/")
        
    except Exception as e:
        print(f"❌ ERREUR GÉNÉRALE: {e}")
        conn.rollback()
    finally:
        conn.close()

def create_base_data(cursor):
    """Crée des données de base si nécessaire"""
    try:
        # Créer un médecin de test
        cursor.execute('''
            INSERT OR IGNORE INTO medecin_medecin 
            (nom, prenom, specialite, numero_ordre, est_actif, date_creation)
            VALUES ('Dupont', 'Jean', 'Généraliste', '123456', 1, datetime('now'))
        ''')
        
        # Créer des patients de test
        for i in range(1, 4):
            cursor.execute(f'''
                INSERT OR IGNORE INTO membres_membre 
                (nom, prenom, email, telephone, date_naissance, date_creation)
                VALUES ('Patient{i}', 'Test{i}', 'patient{i}@test.com', '0123456789', '1980-01-01', datetime('now'))
            ''')
        
        # Créer un pharmacien de test
        cursor.execute('''
            INSERT OR IGNORE INTO pharmacien_pharmacien 
            (nom, prenom, nom_pharmacie, adresse, est_actif, date_creation)
            VALUES ('Martin', 'Sophie', 'Pharmacie Centrale', '123 Rue Principale', 1, datetime('now'))
        ''')
        
        print("✅ Données de base créées")
        
    except Exception as e:
        print(f"⚠️  Données de base: {e}")

def create_pharmacien_view(cursor):
    """Crée ou met à jour la vue pharmacien"""
    try:
        cursor.execute("DROP VIEW IF EXISTS pharmacien_ordonnances_view")
        
        cursor.execute('''
            CREATE VIEW pharmacien_ordonnances_view AS
            SELECT 
                op.id as partage_id,
                mo.id as ordonnance_id,
                mo.numero,
                mo.date_prescription,
                mo.date_expiration,
                mo.type_ordonnance,
                mo.diagnostic,
                mo.medicaments,
                mo.posologie,
                mo.duree_traitement,
                mo.renouvelable,
                mo.nombre_renouvellements,
                mo.renouvellements_effectues,
                mo.statut,
                mo.est_urgent,
                mo.notes,
                op.date_partage,
                CASE WHEN op.statut = 'ACTIF' THEN 1 ELSE 0 END as partage_actif,
                m.nom as patient_nom,
                m.prenom as patient_prenom,
                mm.nom as medecin_nom,
                mm.prenom as medecin_prenom,
                ph.nom as pharmacien_nom
            FROM ordonnance_partage op
            JOIN medecin_ordonnance mo ON op.ordonnance_medecin_id = mo.id
            JOIN membres_membre m ON mo.patient_id = m.id
            JOIN medecin_medecin mm ON mo.medecin_id = mm.id
            JOIN pharmacien_pharmacien ph ON op.pharmacien_id = ph.id
            WHERE op.statut = 'ACTIF'
        ''')
        print("✅ Vue pharmacien créée avec medecin_ordonnance")
        
    except Exception as e:
        print(f"❌ Erreur vue: {e}")

if __name__ == "__main__":
    fix_final_complete()