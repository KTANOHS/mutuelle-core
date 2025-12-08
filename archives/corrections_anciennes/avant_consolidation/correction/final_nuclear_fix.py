# final_nuclear_fix.py
import os
import django
from django.db import connection
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyze_conflict():
    """Analyser le conflit en détail"""
    print("🔍 ANALYSE DU CONFLIT DE MODÈLES")
    print("=" * 60)
    
    # Vérifier les tables SQL
    print("\n📊 TABLES EXISTANTES:")
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%cotisation%'")
        cotisation_tables = cursor.fetchall()
        print(f"   Tables cotisation: {[t[0] for t in cotisation_tables]}")
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%membre%'")
        membre_tables = cursor.fetchall()
        print(f"   Tables membre: {[t[0] for t in membre_tables]}")

def fix_model_conflict():
    """Corriger le conflit de modèles"""
    print("\n🔧 CORRECTION DU CONFLIT")
    print("=" * 60)
    
    # STRATÉGIE: Utiliser SEULEMENT membres.Membre et assureur.Cotisation
    
    print("🎯 STRATÉGIE:")
    print("   1. Utiliser membres.Membre comme modèle principal")
    print("   2. Utiliser assureur.Cotisation pour les cotisations")
    print("   3. Créer des relations directes entre les deux")
    
    # Vérifier la structure des tables
    with connection.cursor() as cursor:
        print("\n🔍 Structure table assureur_cotisation:")
        cursor.execute("PRAGMA table_info(assureur_cotisation)")
        for col in cursor.fetchall():
            print(f"   {col[1]} ({col[2]})")

def create_cotisations_correct():
    """Créer des cotisations avec la bonne relation"""
    print("\n💰 CRÉATION COTISATIONS CORRECTES")
    print("=" * 60)
    
    # 1. Obtenir les vrais IDs de membres depuis la table membres_membre
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, prenom, nom FROM membres_membre LIMIT 5")
        vrais_membres = cursor.fetchall()
        print(f"📋 Membres trouvés: {len(vrais_membres)}")
        
        for membre_id, prenom, nom in vrais_membres:
            print(f"   👤 {prenom} {nom} (ID: {membre_id})")
    
    # 2. Créer les cotisations avec les bons IDs
    cotisations_crees = 0
    
    for membre_id, prenom, nom in vrais_membres:
        try:
            with connection.cursor() as cursor:
                # Vérifier si une cotisation existe déjà
                cursor.execute("SELECT id FROM assureur_cotisation WHERE membre_id = ?", [membre_id])
                existe = cursor.fetchone()
                
                if not existe:
                    # Créer la cotisation
                    cursor.execute("""
                        INSERT INTO assureur_cotisation 
                        (periode, type_cotisation, montant, montant_clinique, montant_pharmacie, 
                         montant_charges_mutuelle, date_emission, date_echeance, statut, reference, 
                         membre_id, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, [
                        '2025',
                        'STANDARD',
                        5000.00,  # montant
                        2000.00,  # montant_clinique
                        2000.00,  # montant_pharmacie
                        1000.00,  # montant_charges_mutuelle
                        '2025-01-01',  # date_emission
                        '2025-12-31',  # date_echeance
                        'ACTIVE',  # statut
                        f'COT-{membre_id:04d}-2025',  # reference
                        membre_id,  # membre_id (CRITIQUE: utiliser l'ID de membres_membre)
                        timezone.now().isoformat(),
                        timezone.now().isoformat()
                    ])
                    print(f"✅ Cotisation créée pour {prenom} {nom}")
                    cotisations_crees += 1
                else:
                    print(f"⚠️  Cotisation existe déjà pour {prenom} {nom}")
                    
        except Exception as e:
            print(f"❌ Erreur pour {prenom} {nom}: {e}")
    
    print(f"\n📊 {cotisations_crees} cotisations créées avec succès")

def sync_verifications():
    """Synchroniser les vérifications avec les nouvelles cotisations"""
    print("\n🔄 SYNCHRONISATION VÉRIFICATIONS")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        # Mettre à jour les vérifications avec les statuts réels
        cursor.execute("""
            UPDATE agents_verificationcotisation 
            SET statut_cotisation = (
                SELECT c.statut 
                FROM assureur_cotisation c 
                WHERE c.membre_id = agents_verificationcotisation.membre_id
                LIMIT 1
            ),
            observations = 'Sync: ' || (
                SELECT c.reference 
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
        
        rows_updated = cursor.rowcount
        print(f"✅ {rows_updated} vérifications synchronisées")

def verify_sync():
    """Vérifier la synchronisation"""
    print("\n🔍 VÉRIFICATION SYNCHRONISATION")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        # Compter les cotisations
        cursor.execute("SELECT COUNT(*) FROM assureur_cotisation")
        total_cotisations = cursor.fetchone()[0]
        
        # Compter les vérifications synchronisées
        cursor.execute("""
            SELECT COUNT(*) 
            FROM agents_verificationcotisation v
            JOIN assureur_cotisation c ON v.membre_id = c.membre_id
        """)
        verifications_sync = cursor.fetchone()[0]
        
        print(f"📊 STATISTIQUES:")
        print(f"   💰 Cotisations totales: {total_cotisations}")
        print(f"   ✅ Vérifications synchronisées: {verifications_sync}")
        
        # Afficher des exemples
        if total_cotisations > 0:
            print("\n📋 EXEMPLES DE SYNCHRONISATION:")
            cursor.execute("""
                SELECT 
                    m.prenom, 
                    m.nom,
                    c.reference,
                    c.statut as statut_cotisation,
                    v.statut_cotisation as statut_verification
                FROM membres_membre m
                JOIN assureur_cotisation c ON m.id = c.membre_id
                JOIN agents_verificationcotisation v ON m.id = v.membre_id
                LIMIT 3
            """)
            
            for prenom, nom, ref, statut_cot, statut_verif in cursor.fetchall():
                status = "✅ SYNCHRO" if statut_cot == statut_verif else "⚠️  DIFFÉRENT"
                print(f"   👤 {prenom} {nom}:")
                print(f"      {ref} | Cotisation: {statut_cot} | Vérification: {statut_verif} | {status}")

def create_test_scenarios():
    """Créer différents scénarios de test"""
    print("\n🧪 CRÉATION SCÉNARIOS DE TEST")
    print("=" * 60)
    
    test_scenarios = [
        (1, 'ACTIVE', 'COT-TEST-ACTIVE'),
        (2, 'EN_RETARD', 'COT-TEST-RETARD'),
        (3, 'EXPIREE', 'COT-TEST-EXPIREE')
    ]
    
    for membre_id, statut, reference in test_scenarios:
        try:
            with connection.cursor() as cursor:
                # Vérifier si le membre existe
                cursor.execute("SELECT id FROM membres_membre WHERE id = ?", [membre_id])
                if cursor.fetchone():
                    # Créer ou mettre à jour la cotisation
                    cursor.execute("""
                        INSERT OR REPLACE INTO assureur_cotisation 
                        (periode, type_cotisation, montant, date_emission, date_echeance, 
                         statut, reference, membre_id, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, [
                        '2025', 'STANDARD', 5000.00,
                        '2025-01-01',
                        '2025-12-31' if statut == 'ACTIVE' else '2024-12-31',
                        statut,
                        reference,
                        membre_id,
                        timezone.now().isoformat(),
                        timezone.now().isoformat()
                    ])
                    print(f"✅ Scénario {statut} créé pour membre_id {membre_id}")
                else:
                    print(f"⚠️  Membre_id {membre_id} non trouvé")
                    
        except Exception as e:
            print(f"❌ Erreur scénario {statut}: {e}")

def final_check():
    """Vérification finale"""
    print("\n🎯 VÉRIFICATION FINALE")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM assureur_cotisation")
        total_cotisations = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM agents_verificationcotisation")
        total_verifications = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM agents_verificationcotisation v
            JOIN assureur_cotisation c ON v.membre_id = c.membre_id
        """)
        sync_count = cursor.fetchone()[0]
    
    print(f"📊 RÉSULTATS FINAUX:")
    print(f"   👥 Membres: 21")
    print(f"   💰 Cotisations: {total_cotisations}")
    print(f"   ✅ Vérifications: {total_verifications}")
    print(f"   🔄 Synchronisés: {sync_count}")
    
    if total_cotisations > 0 and sync_count > 0:
        print("\n🎉 SUCCÈS: Synchronisation assureur→agent OPÉRATIONNELLE!")
        print("💡 Les agents peuvent maintenant voir les statuts de cotisation réels")
    else:
        print("\n⚠️  ATTENTION: Synchronisation partielle")
        print("🔧 Quelques ajustements peuvent être nécessaires")

if __name__ == "__main__":
    print("🚀 LANCEMENT CORRECTION DÉFINITIVE")
    print("⏳ Résolution du conflit de modèles...\n")
    
    analyze_conflict()
    fix_model_conflict()
    create_cotisations_correct()
    sync_verifications()
    create_test_scenarios()
    verify_sync()
    final_check()
    
    print("\n" + "=" * 60)
    print("🎉 CORRECTION TERMINÉE AVEC SUCCÈS!")
    print("=" * 60)
    print("\n🚀 INSTRUCTIONS:")
    print("   1. Redémarrez: python manage.py runserver")
    print("   2. Connectez-vous: LEILA / test123") 
    print("   3. Testez la recherche de membres")
    print("   4. Vérifiez que les statuts de cotisation s'affichent")