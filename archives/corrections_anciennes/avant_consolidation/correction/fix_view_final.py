import sqlite3
from datetime import datetime

def fix_view_final():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    try:
        print("🔧 CORRECTION FINALE DE LA VUE")
        print("=" * 50)
        
        # 1. Vérifier la structure de auth_user
        cursor.execute("PRAGMA table_info(auth_user)")
        user_columns = [col[1] for col in cursor.fetchall()]
        print("Colonnes auth_user:", user_columns)
        
        # 2. Recréer la vue avec les bonnes jointures
        cursor.execute("DROP VIEW IF EXISTS pharmacien_ordonnances_view")
        
        view_sql = '''
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
                u_med.first_name as medecin_prenom,
                u_med.last_name as medecin_nom,
                u_pharm.first_name as pharmacien_prenom,
                u_pharm.last_name as pharmacien_nom
            FROM ordonnance_partage op
            JOIN medecin_ordonnance mo ON op.ordonnance_medecin_id = mo.id
            JOIN membres_membre m ON mo.patient_id = m.id
            JOIN medecin_medecin mm ON mo.medecin_id = mm.id
            JOIN auth_user u_med ON mm.user_id = u_med.id
            JOIN pharmacien_pharmacien pp ON op.pharmacien_id = pp.id
            JOIN auth_user u_pharm ON pp.user_id = u_pharm.id
            WHERE op.statut = 'ACTIF'
        '''
        
        cursor.execute(view_sql)
        conn.commit()
        print("✅ Vue pharmacien créée avec les bonnes jointures")
        
        # 3. VÉRIFICATION
        print("\n📊 VÉRIFICATION FINALE:")
        
        cursor.execute("SELECT COUNT(*) FROM medecin_ordonnance")
        total_ord = cursor.fetchone()[0]
        print(f"💊 Ordonnances totales: {total_ord}")
        
        cursor.execute("SELECT COUNT(*) FROM ordonnance_partage WHERE statut = 'ACTIF'")
        partages = cursor.fetchone()[0]
        print(f"🔗 Partages actifs: {partages}")
        
        cursor.execute("SELECT COUNT(*) FROM pharmacien_ordonnances_view")
        vue_count = cursor.fetchone()[0]
        print(f"👁️  Ordonnances dans vue: {vue_count}")
        
        if vue_count > 0:
            print(f"\n📋 ORDONNANCES VISIBLES:")
            cursor.execute('''
                SELECT ordonnance_id, numero, patient_prenom, patient_nom, medicaments, medecin_prenom, medecin_nom
                FROM pharmacien_ordonnances_view 
                ORDER BY date_partage DESC LIMIT 3
            ''')
            for row in cursor.fetchall():
                print(f"   #{row[0]} {row[1]} - Patient: {row[2]} {row[3]} - Médecin: Dr {row[4]} {row[5]} - Médicaments: {row[6]}")
        
        print(f"\n🎯 SYSTÈME PRÊT!")
        print(f"🌐 URL: http://127.0.0.1:8000/pharmacien/ordonnances/")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_view_final()