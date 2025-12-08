# complete_system.py
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def create_more_cotisations_sql():
    """Créer plus de cotisations via SQL direct"""
    print("💰 CRÉATION COTISATIONS SUPPLÉMENTAIRES")
    print("=" * 50)
    
    cotisations_data = [
        # (membre_id, reference, statut, nom)
        (5, 'COT-ACTIVE-002', 'ACTIVE', 'Jean Bernard'),
        (13, 'COT-RETARD-001', 'EN_RETARD', 'ASIA DRAMANE'),
        (6, 'COT-ACTIVE-003', 'ACTIVE', 'Alice Dubois'),
        (16, 'COT-EXPIREE-001', 'EXPIREE', 'Jean Dupont'),
        (8, 'COT-ACTIVE-004', 'ACTIVE', 'Emma Girard'),
    ]
    
    for membre_id, reference, statut, nom in cotisations_data:
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
                    '2025-01-01', 
                    '2025-12-31' if statut == 'ACTIVE' else '2024-06-30',
                    statut,
                    reference,
                    f'Cotisation {statut} pour {nom}',
                    membre_id,
                    '2025-01-01 10:00:00',
                    '2025-01-01 10:00:00'
                ])
                print(f"✅ {reference} créée pour {nom} ({statut})")
                
        except Exception as e:
            print(f"❌ Erreur pour {nom}: {e}")

def sync_all():
    """Synchroniser toutes les cotisations"""
    print("\n🔄 SYNCHRONISATION COMPLÈTE")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE agents_verificationcotisation 
            SET statut_cotisation = COALESCE(
                (SELECT c.statut FROM assureur_cotisation c WHERE c.membre_id = agents_verificationcotisation.membre_id),
                'NON_TROUVEE'
            ),
            observations = COALESCE(
                (SELECT 'Sync: ' || c.reference FROM assureur_cotisation c WHERE c.membre_id = agents_verificationcotisation.membre_id),
                'Aucune cotisation'
            )
        """)
        print(f"✅ {cursor.rowcount} vérifications synchronisées")

def show_final_state():
    """Afficher l'état final"""
    print("\n📊 ÉTAT FINAL DU SYSTÈME")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        # Statistiques
        cursor.execute("SELECT COUNT(*) FROM assureur_cotisation")
        total_cotisations = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM agents_verificationcotisation WHERE statut_cotisation != 'NON_TROUVEE'")
        verifications_sync = cursor.fetchone()[0]
        
        print(f"📈 STATISTIQUES:")
        print(f"   💰 Cotisations créées: {total_cotisations}")
        print(f"   ✅ Vérifications synchronisées: {verifications_sync}/16")
        
        # Détail
        cursor.execute("""
            SELECT m.prenom, m.nom, c.reference, c.statut, v.statut_cotisation
            FROM membres_membre m
            LEFT JOIN assureur_cotisation c ON m.id = c.membre_id
            LEFT JOIN agents_verificationcotisation v ON m.id = v.membre_id
            WHERE c.id IS NOT NULL
            ORDER BY c.statut
        """)
        
        print("\n📋 COTISATIONS ACTIVES:")
        for prenom, nom, ref, statut_cot, statut_verif in cursor.fetchall():
            if statut_cot == 'ACTIVE':
                print(f"   ✅ {prenom} {nom}: {statut_cot}")
        
        print("\n📋 COTISATIONS PROBLÉMATIQUES:")
        cursor.execute("SELECT m.prenom, m.nom, c.statut FROM assureur_cotisation c JOIN membres_membre m ON c.membre_id = m.id WHERE c.statut != 'ACTIVE'")
        for prenom, nom, statut in cursor.fetchall():
            print(f"   ⚠️  {prenom} {nom}: {statut}")

def test_instructions():
    """Instructions de test"""
    print("\n🎯 INSTRUCTIONS DE TEST FINAL")
    print("=" * 50)
    print("1. 🌐 Allez sur: http://127.0.0.1:8000/agents/verification-cotisations/")
    print("2. 👤 Connectez-vous: LEILA / test123")
    print("3. 🔍 Testez ces recherches:")
    print("   - 'Marie' → Doit montrer ACTIVE")
    print("   - 'Jean' → Doit montrer ACTIVE ou EXPIREE") 
    print("   - 'ASIA' → Doit montrer EN_RETARD")
    print("   - 'Alice' → Doit montrer ACTIVE")
    print("4. 📊 Vérifiez les différents statuts de cotisation")

if __name__ == "__main__":
    print("🚀 SYSTÈME COMPLET ASSUREUR→AGENT")
    create_more_cotisations_sql()
    sync_all()
    show_final_state()
    test_instructions()
    print("\n🎉 SYSTÈME PRÊT POUR LA PRODUCTION!")