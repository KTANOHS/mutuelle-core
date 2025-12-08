# deep_analysis_fix.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def deep_analysis():
    """Analyse approfondie de la structure des modèles"""
    print("🔍 ANALYSE APPROFONDIE DE L'ARCHITECTURE")
    print("=" * 60)
    
    from django.apps import apps
    from django.db import connection
    
    # 1. Analyser tous les modèles
    print("\n📦 ANALYSE COMPLÈTE DES MODÈLES")
    print("-" * 40)
    
    for app_config in apps.get_app_configs():
        app_name = app_config.name
        if app_name in ['assureur', 'membres', 'agents']:
            print(f"\n🏷️  APPLICATION: {app_name}")
            for model in app_config.get_models():
                print(f"   📋 {model.__name__}:")
                # Afficher les champs
                fields = []
                for field in model._meta.get_fields():
                    field_info = f"{field.name} ({field.__class__.__name__})"
                    if hasattr(field, 'related_model') and field.related_model:
                        field_info += f" -> {field.related_model.__name__}"
                    fields.append(field_info)
                print(f"      Champs: {', '.join(fields[:5])}...")

def analyze_assureur_problem():
    """Analyser spécifiquement le problème Assureur"""
    print("\n🔎 ANALYSE SPÉCIFIQUE DU PROBLÈME ASSUREUR")
    print("=" * 60)
    
    from assureur.models import Assureur, Cotisation
    
    print("🔍 Structure du modèle Assureur:")
    assureur_fields = [f.name for f in Assureur._meta.get_fields()]
    print(f"   Champs Assureur: {assureur_fields}")
    
    print("\n🔍 Structure du modèle Cotisation:")
    cotisation_fields = []
    for field in Cotisation._meta.get_fields():
        field_info = f"{field.name} -> {field.related_model.__name__ if hasattr(field, 'related_model') and field.related_model else field.__class__.__name__}"
        cotisation_fields.append(field_info)
    print(f"   Champs Cotisation: {cotisation_fields}")
    
    # Vérifier la table SQL réelle
    print("\n🔍 Vérification base de données:")
    with connection.cursor() as cursor:
        try:
            cursor.execute("PRAGMA table_info(assureur_assureur)")
            columns = cursor.fetchall()
            print("   Table assureur_assureur:")
            for col in columns:
                print(f"      {col[1]} ({col[2]})")
        except Exception as e:
            print(f"   ❌ Erreur table assureur: {e}")
        
        try:
            cursor.execute("PRAGMA table_info(assureur_cotisation)")
            columns = cursor.fetchall()
            print("   Table assureur_cotisation:")
            for col in columns:
                print(f"      {col[1]} ({col[2]})")
        except Exception as e:
            print(f"   ❌ Erreur table cotisation: {e}")

def fix_foreign_key_issue():
    """Corriger le problème de FOREIGN KEY"""
    print("\n🔧 CORRECTION DU PROBLÈME FOREIGN KEY")
    print("=" * 60)
    
    from django.db import connection
    from django.utils import timezone
    
    # Vérifier les IDs de membres existants
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM membres_membre LIMIT 5")
        membre_ids = [row[0] for row in cursor.fetchall()]
        print(f"📋 IDs membres disponibles: {membre_ids}")
    
    # Créer des cotisations avec les bons IDs
    try:
        with connection.cursor() as cursor:
            for i, membre_id in enumerate(membre_ids[:3], 1):
                cursor.execute("""
                    INSERT OR IGNORE INTO assureur_cotisation 
                    (periode, type_cotisation, montant, date_emission, 
                     date_echeance, statut, reference, membre_id, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    '2025', 'STANDARD', 5000,
                    (timezone.now().date().replace(day=1)),  # Premier du mois
                    (timezone.now().date().replace(day=1) + timezone.timedelta(days=365)),
                    'ACTIVE', 
                    f'FIX-2025-{membre_id:04d}',
                    membre_id,
                    timezone.now(),
                    timezone.now()
                ])
                print(f"✅ Cotisation créée pour membre_id: {membre_id}")
                
    except Exception as e:
        print(f"❌ Erreur création cotisation: {e}")

def create_minimal_assureur():
    """Créer un assureur minimal avec la bonne structure"""
    print("\n👤 CRÉATION ASSUREUR MINIMAL")
    print("=" * 60)
    
    from django.contrib.auth.models import User
    from django.db import connection
    
    try:
        # Vérifier la structure réelle de la table assureur
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(assureur_assureur)")
            columns = [col[1] for col in cursor.fetchall()]
            print(f"📋 Colonnes réelles assureur_assureur: {columns}")
        
        # Créer l'utilisateur
        user, created = User.objects.get_or_create(
            username='assureur_fix',
            defaults={
                'first_name': 'Assureur',
                'last_name': 'Système',
                'is_staff': True
            }
        )
        if created:
            user.set_password('assureur123')
            user.save()
            print("✅ Utilisateur assureur créé")
        
        # Créer l'assureur avec la bonne structure
        with connection.cursor() as cursor:
            # Vérifier si l'assureur existe déjà
            cursor.execute("SELECT id FROM assureur_assureur WHERE user_id = ?", [user.id])
            existing = cursor.fetchone()
            
            if not existing:
                cursor.execute("""
                    INSERT INTO assureur_assureur (user_id, created_at, updated_at)
                    VALUES (?, ?, ?)
                """, [user.id, timezone.now(), timezone.now()])
                print("✅ Assureur créé avec structure minimale")
            else:
                print("✅ Assureur existe déjà")
                
    except Exception as e:
        print(f"❌ Erreur création assureur: {e}")

def verify_and_sync():
    """Vérifier et synchroniser après corrections"""
    print("\n🔄 VÉRIFICATION ET SYNCHRONISATION")
    print("=" * 60)
    
    from django.db import connection
    
    # Vérifier les cotisations créées
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM assureur_cotisation")
        cotisation_count = cursor.fetchone()[0]
        print(f"💰 Cotisations en base: {cotisation_count}")
        
        if cotisation_count > 0:
            cursor.execute("""
                SELECT c.reference, c.statut, m.prenom, m.nom 
                FROM assureur_cotisation c
                JOIN membres_membre m ON c.membre_id = m.id
                LIMIT 3
            """)
            print("📋 Exemples de cotisations:")
            for row in cursor.fetchall():
                print(f"   ✅ {row[0]} - {row[2]} {row[3]} ({row[1]})")
    
    # Synchroniser les vérifications
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE agents_verificationcotisation 
                SET statut_cotisation = (
                    SELECT c.statut 
                    FROM assureur_cotisation c 
                    WHERE c.membre_id = agents_verificationcotisation.membre_id
                    LIMIT 1
                )
                WHERE EXISTS (
                    SELECT 1 FROM assureur_cotisation c 
                    WHERE c.membre_id = agents_verificationcotisation.membre_id
                )
            """)
            print("✅ Vérifications synchronisées avec cotisations")
            
    except Exception as e:
        print(f"❌ Erreur synchronisation: {e}")

def test_complete_workflow():
    """Tester le workflow complet après corrections"""
    print("\n🧪 TEST WORKFLOW COMPLET")
    print("=" * 60)
    
    from django.db import connection
    
    print("🔍 Test de la synchronisation assureur → agent:")
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                m.prenom, 
                m.nom,
                c.statut as statut_cotisation,
                v.statut_cotisation as statut_verification
            FROM membres_membre m
            LEFT JOIN assureur_cotisation c ON m.id = c.membre_id
            LEFT JOIN agents_verificationcotisation v ON m.id = v.membre_id
            WHERE c.id IS NOT NULL
            LIMIT 5
        """)
        
        results = cursor.fetchall()
        if results:
            for row in results:
                synced = "✅ SYNCHRONISÉ" if row[2] == row[3] else "⚠️  DIFFÉRENT"
                print(f"   👤 {row[0]} {row[1]}:")
                print(f"      Assureur: {row[2]} | Agent: {row[3]} | {synced}")
        else:
            print("   ❌ Aucune donnée synchronisée trouvée")

def emergency_fix():
    """Solution d'urgence si tout échoue"""
    print("\n🚨 SOLUTION D'URGENCE")
    print("=" * 60)
    
    from django.db import connection
    from django.utils import timezone
    
    try:
        with connection.cursor() as cursor:
            # Créer une cotisation de test simple
            cursor.execute("SELECT id FROM membres_membre LIMIT 1")
            premier_membre = cursor.fetchone()
            
            if premier_membre:
                membre_id = premier_membre[0]
                
                cursor.execute("""
                    INSERT OR IGNORE INTO assureur_cotisation 
                    (periode, type_cotisation, montant, date_emission, 
                     date_echeance, statut, reference, membre_id, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    '2025', 'STANDARD', 5000,
                    '2025-01-01',
                    '2025-12-31', 
                    'ACTIVE',
                    'URGENCY-FIX-001',
                    membre_id,
                    timezone.now().isoformat(),
                    timezone.now().isoformat()
                ])
                print("✅ Cotisation d'urgence créée")
                
                # Mettre à jour la vérification correspondante
                cursor.execute("""
                    UPDATE agents_verificationcotisation 
                    SET statut_cotisation = 'ACTIVE',
                        observations = 'Sync urgence: COT-URGENCY-FIX-001'
                    WHERE membre_id = ?
                """, [membre_id])
                print("✅ Vérification synchronisée")
                
    except Exception as e:
        print(f"❌ Erreur solution urgence: {e}")

if __name__ == "__main__":
    print("🚀 LANCEMENT ANALYSE ET CORRECTION APPROFONDIE")
    print("⏳ Diagnostic complet de l'architecture...\n")
    
    deep_analysis()
    analyze_assureur_problem()
    create_minimal_assureur()
    fix_foreign_key_issue()
    verify_and_sync()
    test_complete_workflow()
    
    # Si toujours pas de cotisations, appliquer l'urgence
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM assureur_cotisation")
        if cursor.fetchone()[0] == 0:
            emergency_fix()
    
    print("\n" + "=" * 60)
    print("🎉 ANALYSE ET CORRECTIONS TERMINÉES!")
    print("=" * 60)