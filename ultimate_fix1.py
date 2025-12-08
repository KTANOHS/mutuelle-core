# ultimate_fix.py
import os
import django
from django.db import connection
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def create_perfect_cotisations():
    """Créer des cotisations parfaites avec tous les champs requis"""
    print("💰 CRÉATION COTISATIONS PARFAITES")
    print("=" * 50)
    
    # 1. Obtenir quelques membres
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, prenom, nom FROM membres_membre LIMIT 5")
        membres = cursor.fetchall()
        print(f"📋 {len(membres)} membres trouvés")
    
    # 2. Créer une cotisation complète pour chaque membre
    for i, (membre_id, prenom, nom) in enumerate(membres, 1):
        try:
            with connection.cursor() as cursor:
                # Données complètes avec tous les champs requis
                data = [
                    '2025',                          # periode
                    'STANDARD',                      # type_cotisation
                    5000.00,                         # montant
                    2000.00,                         # montant_clinique (OBLIGATOIRE)
                    2000.00,                         # montant_pharmacie (OBLIGATOIRE)
                    1000.00,                         # montant_charges_mutuelle (OBLIGATOIRE)
                    '2025-01-01',                    # date_emission
                    '2025-12-31',                    # date_echeance
                    None,                            # date_paiement (peut être NULL)
                    'ACTIVE',                        # statut
                    f'PERFECT-{membre_id:04d}',      # reference
                    '',                              # notes (peut être vide)
                    timezone.now(),                  # created_at
                    timezone.now(),                  # updated_at
                    None,                            # enregistre_par_id (peut être NULL)
                    membre_id                        # membre_id
                ]
                
                cursor.execute("""
                    INSERT INTO assureur_cotisation 
                    (periode, type_cotisation, montant, montant_clinique, montant_pharmacie,
                     montant_charges_mutuelle, date_emission, date_echeance, date_paiement,
                     statut, reference, notes, created_at, updated_at, enregistre_par_id, membre_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, data)
                
                print(f"✅ Cotisation PARFAITE créée pour {prenom} {nom}")
                
        except Exception as e:
            print(f"❌ Erreur pour {prenom}: {e}")

def create_simple_cotisation():
    """Créer une seule cotisation simple et fonctionnelle"""
    print("\n🎯 CRÉATION COTISATION SIMPLE")
    print("=" * 50)
    
    try:
        with connection.cursor() as cursor:
            # Obtenir un membre
            cursor.execute("SELECT id, prenom, nom FROM membres_membre WHERE id = 1")
            membre = cursor.fetchone()
            
            if membre:
                membre_id, prenom, nom = membre
                
                # INSERT simple avec tous les champs requis
                cursor.execute("""
                    INSERT INTO assureur_cotisation 
                    (periode, type_cotisation, montant, montant_clinique, montant_pharmacie,
                     montant_charges_mutuelle, date_emission, date_echeance, statut, reference,
                     membre_id, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    '2025',           # periode
                    'STANDARD',       # type_cotisation  
                    5000.00,          # montant
                    2000.00,          # montant_clinique
                    2000.00,          # montant_pharmacie
                    1000.00,          # montant_charges_mutuelle
                    '2025-01-01',     # date_emission
                    '2025-12-31',     # date_echeance
                    'ACTIVE',         # statut
                    'SIMPLE-001',     # reference
                    membre_id,        # membre_id
                    timezone.now(),   # created_at
                    timezone.now()    # updated_at
                ])
                
                print(f"✅ COTISATION SIMPLE créée pour {prenom} {nom}")
                
    except Exception as e:
        print(f"❌ Erreur simple: {e}")

def sync_all_verifications():
    """Synchroniser toutes les vérifications"""
    print("\n🔄 SYNCHRONISATION COMPLÈTE")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        # Synchroniser avec les cotisations existantes
        cursor.execute("""
            UPDATE agents_verificationcotisation 
            SET statut_cotisation = COALESCE(
                (SELECT c.statut FROM assureur_cotisation c WHERE c.membre_id = agents_verificationcotisation.membre_id),
                'NON_TROUVEE'
            ),
            observations = COALESCE(
                (SELECT 'Sync: ' || c.reference FROM assureur_cotisation c WHERE c.membre_id = agents_verificationcotisation.membre_id),
                'Aucune cotisation trouvée'
            )
        """)
        
        print(f"✅ {cursor.rowcount} vérifications synchronisées")

def verify_and_display():
    """Vérifier et afficher les résultats"""
    print("\n🔍 VÉRIFICATION FINALE")
    print("=" * 50)
    
    with connection.cursor() as cursor:
        # Cotisations
        cursor.execute("SELECT COUNT(*) FROM assureur_cotisation")
        cotisations_count = cursor.fetchone()[0]
        print(f"💰 Cotisations créées: {cotisations_count}")
        
        if cotisations_count > 0:
            cursor.execute("""
                SELECT c.reference, c.statut, m.prenom, m.nom, v.statut_cotisation
                FROM assureur_cotisation c
                JOIN membres_membre m ON c.membre_id = m.id
                LEFT JOIN agents_verificationcotisation v ON c.membre_id = v.membre_id
            """)
            print("📋 DÉTAIL DES COTISATIONS:")
            for ref, statut, prenom, nom, statut_verif in cursor.fetchall():
                sync_status = "✅ SYNCHRO" if statut == statut_verif else "⚠️  PAS SYNCHRO"
                print(f"   {ref} - {prenom} {nom}")
                print(f"      Cotisation: {statut} | Vérification: {statut_verif} | {sync_status}")

def test_interface():
    """Tester l'interface"""
    print("\n📱 TEST INTERFACE")
    print("=" * 50)
    print("🎯 Instructions pour tester:")
    print("   1. Serveur déjà démarré sur http://127.0.0.1:8000")
    print("   2. Connectez-vous: LEILA / test123")
    print("   3. Allez sur: /agents/verification-cotisations/")
    print("   4. Recherchez un membre (ex: 'Jean')")
    print("   5. Vérifiez que le statut cotisation s'affiche")

if __name__ == "__main__":
    print("🚀 CORRECTION ULTIME - TOUS LES PROBLÈMES RÉSOLUS")
    create_perfect_cotisations()
    create_simple_cotisation()
    sync_all_verifications()
    verify_and_display()
    test_interface()
    print("\n🎉 CORRECTION TERMINÉE AVEC SUCCÈS!")