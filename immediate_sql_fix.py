# immediate_sql_fix.py
import os
import django
from django.db import connection
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def create_cotisations_simple():
    """Créer des cotisations avec une approche simple et directe"""
    print("💰 CRÉATION IMMÉDIATE DE COTISATIONS")
    print("=" * 50)
    
    # 1. Obtenir quelques membres
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, prenom, nom FROM membres_membre LIMIT 3")
        membres = cursor.fetchall()
        print(f"📋 {len(membres)} membres trouvés")
    
    # 2. Créer une cotisation pour chaque membre
    for membre_id, prenom, nom in membres:
        try:
            with connection.cursor() as cursor:
                # APPROCHE SIMPLE: valeurs directes sans paramètres complexes
                sql = """
                    INSERT INTO assureur_cotisation 
                    (periode, type_cotisation, montant, date_emission, date_echeance, 
                     statut, reference, membre_id, created_at, updated_at)
                    VALUES ('2025', 'STANDARD', 5000.00, '2025-01-01', '2025-12-31', 
                            'ACTIVE', 'COT-%s-2025', %s, '%s', '%s')
                """ % (membre_id, membre_id, timezone.now(), timezone.now())
                
                cursor.execute(sql)
                print(f"✅ Cotisation créée pour {prenom} {nom} (ID: {membre_id})")
                
        except Exception as e:
            print(f"❌ Erreur pour {prenom}: {e}")

def create_emergency_cotisation():
    """Créer une seule cotisation d'urgence pour tester"""
    print("\n🚨 CRÉATION COTISATION D'URGENCE")
    print("=" * 50)
    
    try:
        with connection.cursor() as cursor:
            # Obtenir le premier membre
            cursor.execute("SELECT id, prenom, nom FROM membres_membre LIMIT 1")
            membre = cursor.fetchone()
            
            if membre:
                membre_id, prenom, nom = membre
                
                # Créer une cotisation simple
                cursor.execute("""
                    INSERT INTO assureur_cotisation 
                    (periode, type_cotisation, montant, date_emission, date_echeance, 
                     statut, reference, membre_id, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    '2025',
                    'STANDARD', 
                    5000.00,
                    '2025-01-01',
                    '2025-12-31',
                    'ACTIVE',
                    f'URGENT-{membre_id}',
                    membre_id,
                    timezone.now(),
                    timezone.now()
                ])
                print(f"✅ COTISATION D'URGENCE créée pour {prenom} {nom}")
                
                # Synchroniser immédiatement la vérification
                cursor.execute("""
                    UPDATE agents_verificationcotisation 
                    SET statut_cotisation = 'ACTIVE',
                        observations = 'Sync urgence: COT-URGENT'
                    WHERE membre_id = ?
                """, [membre_id])
                print("✅ Vérification synchronisée")
                
    except Exception as e:
        print(f"❌ Erreur urgence: {e}")

def verify_cotisations():
    """Vérifier que les cotisations existent"""
    print("\n🔍 VÉRIFICATION COTISATIONS")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM assureur_cotisation")
        count = cursor.fetchone()[0]
        print(f"💰 Cotisations en base: {count}")
        
        if count > 0:
            cursor.execute("""
                SELECT c.reference, c.statut, m.prenom, m.nom 
                FROM assureur_cotisation c
                JOIN membres_membre m ON c.membre_id = m.id
            """)
            print("📋 Cotisations existantes:")
            for ref, statut, prenom, nom in cursor.fetchall():
                print(f"   ✅ {ref} - {prenom} {nom} ({statut})")

def test_synchronisation():
    """Tester la synchronisation"""
    print("\n🔄 TEST SYNCHRONISATION")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) 
            FROM agents_verificationcotisation v
            JOIN assureur_cotisation c ON v.membre_id = c.membre_id
        """)
        sync_count = cursor.fetchone()[0]
        print(f"✅ {sync_count} vérifications synchronisées avec cotisations")

if __name__ == "__main__":
    print("🚀 CORRECTION IMMÉDIATE SQL")
    create_cotisations_simple()
    create_emergency_cotisation()
    verify_cotisations()
    test_synchronisation()
    print("\n🎉 Correction terminée!")