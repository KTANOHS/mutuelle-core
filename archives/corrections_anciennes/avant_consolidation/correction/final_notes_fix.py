# final_notes_fix.py
import os
import django
from django.db import connection
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def create_cotisation_with_notes():
    """Créer une cotisation avec le champ notes obligatoire"""
    print("💰 CRÉATION COTISATION AVEC NOTES")
    print("=" * 50)
    
    try:
        with connection.cursor() as cursor:
            # SQL COMPLET avec tous les champs requis
            sql = """
                INSERT INTO assureur_cotisation 
                (periode, type_cotisation, montant, montant_clinique, montant_pharmacie,
                 montant_charges_mutuelle, date_emission, date_echeance, statut, reference,
                 notes, membre_id, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            params = [
                '2025',                    # periode
                'STANDARD',                # type_cotisation
                5000.00,                   # montant
                2000.00,                   # montant_clinique
                2000.00,                   # montant_pharmacie
                1000.00,                   # montant_charges_mutuelle
                '2025-01-01',              # date_emission
                '2025-12-31',              # date_echeance
                'ACTIVE',                  # statut
                'FINAL-FIX-001',           # reference
                'Cotisation créée automatiquement',  # notes (OBLIGATOIRE!)
                1,                         # membre_id
                timezone.now().isoformat(), # created_at
                timezone.now().isoformat()  # updated_at
            ]
            
            cursor.execute(sql, params)
            print("✅ COTISATION CRÉÉE avec succès!")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def create_multiple_with_notes():
    """Créer plusieurs cotisations avec notes"""
    print("\n💰 CRÉATION MULTIPLE COTISATIONS")
    print("=" * 50)
    
    membres = [
        (1, "Jean Bernard"),
        (2, "Dramane Coulibaly"), 
        (3, "ASIA DRAMANE")
    ]
    
    for membre_id, nom in membres:
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO assureur_cotisation 
                    (periode, type_cotisation, montant, montant_clinique, montant_pharmacie,
                     montant_charges_mutuelle, date_emission, date_echeance, statut, reference,
                     notes, membre_id, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    '2025', 'STANDARD', 5000.00, 2000.00, 2000.00, 1000.00,
                    '2025-01-01', '2025-12-31', 'ACTIVE', f'COT-{membre_id:03d}',
                    f'Cotisation standard pour {nom}',
                    membre_id, timezone.now(), timezone.now()
                ])
                print(f"✅ Cotisation créée pour {nom}")
                
        except Exception as e:
            print(f"❌ Erreur pour {nom}: {e}")

def sync_verifications():
    """Synchroniser les vérifications"""
    print("\n🔄 SYNCHRONISATION")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE agents_verificationcotisation 
            SET statut_cotisation = (
                SELECT c.statut 
                FROM assureur_cotisation c 
                WHERE c.membre_id = agents_verificationcotisation.membre_id
                LIMIT 1
            ),
            observations = (
                SELECT 'Sync: ' || c.reference 
                FROM assureur_cotisation c 
                WHERE c.membre_id = agents_verificationcotisation.membre_id
                LIMIT 1
            )
            WHERE EXISTS (
                SELECT 1 
                FROM assureur_cotisation c 
                WHERE c.membre_id = agents_verificationcotisation.membre_id
            )
        """)
        print(f"✅ {cursor.rowcount} vérifications synchronisées")

def verify_results():
    """Vérifier les résultats"""
    print("\n🔍 VÉRIFICATION")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM assureur_cotisation")
        count = cursor.fetchone()[0]
        print(f"💰 Cotisations créées: {count}")
        
        if count > 0:
            cursor.execute("""
                SELECT c.reference, c.statut, m.prenom, m.nom, v.statut_cotisation
                FROM assureur_cotisation c
                JOIN membres_membre m ON c.membre_id = m.id
                LEFT JOIN agents_verificationcotisation v ON c.membre_id = v.membre_id
            """)
            print("📋 DÉTAIL:")
            for ref, statut, prenom, nom, statut_verif in cursor.fetchall():
                print(f"   ✅ {ref} - {prenom} {nom}")
                print(f"      Cotisation: {statut} | Vérification: {statut_verif}")

if __name__ == "__main__":
    print("🚀 CORRECTION FINALE - CHAMP NOTES")
    create_cotisation_with_notes()
    create_multiple_with_notes()
    sync_verifications()
    verify_results()
    print("\n🎉 CORRECTION TERMINÉE!")