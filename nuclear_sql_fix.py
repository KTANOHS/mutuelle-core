# nuclear_sql_fix.py
import os
import django
from django.db import connection
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def raw_sql_fix():
    """Solution SQL brute pour contourner Django ORM"""
    print("🔧 CORRECTION SQL BRUTE")
    print("=" * 50)
    
    # 1. Créer une cotisation avec SQL direct
    try:
        with connection.cursor() as cursor:
            # APPROCHE: SQL direct sans paramètres
            sql = f"""
                INSERT INTO assureur_cotisation 
                (periode, type_cotisation, montant, montant_clinique, montant_pharmacie,
                 montant_charges_mutuelle, date_emission, date_echeance, statut, reference,
                 membre_id, created_at, updated_at)
                VALUES (
                    '2025', 
                    'STANDARD', 
                    5000.00, 
                    2000.00, 
                    2000.00, 
                    1000.00, 
                    '2025-01-01', 
                    '2025-12-31', 
                    'ACTIVE', 
                    'NUCLEAR-FIX-001', 
                    1, 
                    '{timezone.now().isoformat()}', 
                    '{timezone.now().isoformat()}'
                )
            """
            cursor.execute(sql)
            print("✅ COTISATION CRÉÉE avec SQL direct")
            
    except Exception as e:
        print(f"❌ Erreur SQL direct: {e}")

def manual_table_insert():
    """Insertion manuelle dans la table"""
    print("\n🔨 INSERTION MANUELLE TABLE")
    print("=" * 50)
    
    try:
        with connection.cursor() as cursor:
            # Vérifier la structure exacte
            cursor.execute("PRAGMA table_info(assureur_cotisation)")
            columns = cursor.fetchall()
            print("📋 Structure table assureur_cotisation:")
            for col in columns:
                print(f"   {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
            
            # Insertion manuelle avec valeurs fixes
            cursor.execute("""
                INSERT INTO assureur_cotisation 
                (periode, type_cotisation, montant, montant_clinique, montant_pharmacie,
                 montant_charges_mutuelle, date_emission, date_echeance, statut, reference,
                 membre_id, created_at, updated_at)
                VALUES 
                ('2025', 'STANDARD', 5000.00, 2000.00, 2000.00, 1000.00, 
                 '2025-01-01', '2025-12-31', 'ACTIVE', 'MANUAL-001',
                 1, datetime('now'), datetime('now'))
            """)
            print("✅ INSERTION MANUELLE RÉUSSIE")
            
    except Exception as e:
        print(f"❌ Erreur insertion manuelle: {e}")

def create_multiple_cotisations():
    """Créer plusieurs cotisations avec différentes approches"""
    print("\n💰 CRÉATION MULTIPLE COTISATIONS")
    print("=" * 50)
    
    # Différentes approches
    approaches = [
        # Approche 1: SQL direct avec f-string
        {
            'name': 'SQL Direct',
            'sql': """
                INSERT INTO assureur_cotisation 
                (periode, type_cotisation, montant, montant_clinique, montant_pharmacie,
                 montant_charges_mutuelle, date_emission, date_echeance, statut, reference,
                 membre_id, created_at, updated_at)
                VALUES 
                ('2025', 'STANDARD', 5000.00, 2000.00, 2000.00, 1000.00, 
                 '2025-01-01', '2025-12-31', 'ACTIVE', 'DIRECT-001',
                 2, datetime('now'), datetime('now'))
            """
        },
        # Approche 2: SQL avec paramètres simples
        {
            'name': 'SQL Paramètres',
            'sql': """
                INSERT INTO assureur_cotisation 
                (periode, type_cotisation, montant, montant_clinique, montant_pharmacie,
                 montant_charges_mutuelle, date_emission, date_echeance, statut, reference,
                 membre_id, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            'params': [
                '2025', 'STANDARD', 5000.00, 2000.00, 2000.00, 1000.00,
                '2025-01-01', '2025-12-31', 'ACTIVE', 'PARAMS-001',
                3, timezone.now(), timezone.now()
            ]
        }
    ]
    
    for approach in approaches:
        try:
            with connection.cursor() as cursor:
                if 'params' in approach:
                    cursor.execute(approach['sql'], approach['params'])
                else:
                    cursor.execute(approach['sql'])
                print(f"✅ {approach['name']}: SUCCÈS")
                
        except Exception as e:
            print(f"❌ {approach['name']}: {e}")

def verify_success():
    """Vérifier le succès des insertions"""
    print("\n🔍 VÉRIFICATION RÉSULTATS")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM assureur_cotisation")
        count = cursor.fetchone()[0]
        print(f"💰 Cotisations totales: {count}")
        
        if count > 0:
            cursor.execute("""
                SELECT reference, statut, membre_id 
                FROM assureur_cotisation 
                ORDER BY created_at DESC LIMIT 5
            """)
            print("📋 Dernières cotisations:")
            for ref, statut, membre_id in cursor.fetchall():
                print(f"   ✅ {ref} - Membre ID: {membre_id} - Statut: {statut}")
                
            # Synchroniser les vérifications
            cursor.execute("""
                UPDATE agents_verificationcotisation 
                SET statut_cotisation = 'ACTIVE',
                    observations = 'Sync: Cotisations créées'
                WHERE membre_id IN (SELECT membre_id FROM assureur_cotisation)
            """)
            print(f"✅ Vérifications mises à jour")

def final_test():
    """Test final"""
    print("\n🎯 TEST FINAL")
    print("=" * 50)
    print("📱 Interface prête à tester:")
    print("   🌐 http://127.0.0.1:8000/agents/verification-cotisations/")
    print("   👤 LEILA / test123")
    print("   🔍 Recherchez 'Jean' ou autres membres")

if __name__ == "__main__":
    print("🚀 CORRECTION NUCLÉAIRE - DERNIÈRE TENTATIVE")
    raw_sql_fix()
    manual_table_insert()
    create_multiple_cotisations()
    verify_success()
    final_test()
    print("\n🎉 OPÉRATION TERMINÉE!")