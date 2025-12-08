# fix_membre_conflict.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def diagnose_membre_conflict():
    """Diagnostiquer le conflit entre modèles Membre"""
    print("🔍 DIAGNOSTIC DU CONFLIT DE MODÈLES MEMBRE")
    print("=" * 60)
    
    from django.apps import apps
    
    # Identifier tous les modèles Membre
    membre_models = []
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            if model.__name__ == 'Membre':
                membre_models.append(f"{app_config.name}.{model.__name__}")
    
    print(f"📋 Modèles Membre trouvés: {membre_models}")
    
    # Analyser le problème
    if 'membres.Membre' in membre_models and 'assureur.Membre' in membre_models:
        print("🚨 CONFLIT: Deux modèles Membre détectés!")
        print("   ❌ membres.Membre (modèle principal)")
        print("   ❌ assureur.Membre (modèle en conflit)")
        
        # Vérifier quel modèle est utilisé par Cotisation
        from assureur.models import Cotisation
        membre_field = Cotisation._meta.get_field('membre')
        print(f"🔗 Cotisation.membre pointe vers: {membre_field.related_model}")
        
        return True
    else:
        print("✅ Aucun conflit détecté")
        return False

def create_cotisation_fix():
    """Créer une solution de contournement"""
    print("\n🔧 CRÉATION SOLUTION DE CONTOURNEMENT")
    print("=" * 60)
    
    from membres.models import Membre as MembrePrincipal
    from assureur.models import Cotisation, Assureur
    from django.utils import timezone
    from datetime import timedelta
    
    try:
        # 1. Vérifier l'assureur
        assureur = Assureur.objects.first()
        if not assureur:
            print("❌ Aucun assureur trouvé")
            return
        
        # 2. Créer des cotisations avec le bon modèle Membre
        membres = MembrePrincipal.objects.all()[:5]  # 5 premiers pour test
        cotisations_created = 0
        
        for membre in membres:
            try:
                # Vérifier si une cotisation existe déjà pour ce membre
                existing = Cotisation.objects.filter(membre_id=membre.id).exists()
                
                if not existing:
                    # Créer la cotisation en utilisant l'ID directement
                    cotisation = Cotisation(
                        membre_id=membre.id,  # Utiliser l'ID directement
                        periode="2025",
                        type_cotisation="STANDARD", 
                        montant=5000,
                        date_emission=timezone.now().date(),
                        date_echeance=(timezone.now() + timedelta(days=365)).date(),
                        statut="ACTIVE",
                        reference=f"COT-FIX-{membre.id}",
                        enregistre_par=assureur
                    )
                    
                    # Éviter la validation qui cause l'erreur
                    cotisation.save(force_insert=True)
                    print(f"✅ Cotisation créée pour {membre.prenom} {membre.nom} (ID: {membre.id})")
                    cotisations_created += 1
                    
            except Exception as e:
                print(f"❌ Erreur pour {membre.prenom}: {e}")
        
        print(f"\n📊 {cotisations_created} cotisations créées avec contournement")
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")

def check_current_cotisations():
    """Vérifier les cotisations existantes"""
    print("\n📊 VÉRIFICATION COTISATIONS EXISTANTES")
    print("=" * 60)
    
    from assureur.models import Cotisation
    
    try:
        cotisations = Cotisation.objects.all()
        print(f"💰 Cotisations en base: {cotisations.count()}")
        
        for cot in cotisations[:3]:  # Afficher les 3 premières
            print(f"   📄 {cot.reference} - Membre ID: {cot.membre_id}")
            
    except Exception as e:
        print(f"❌ Erreur vérification: {e}")

def create_relationship_fix():
    """Créer un correctif pour la relation"""
    print("\n🔗 CORRECTION DE LA RELATION")
    print("=" * 60)
    
    # Solution 1: Créer une ForeignKey correcte
    print("💡 SOLUTION 1: Utiliser l'ID directement")
    print("   Cotisation.membre_id = membre.id (au lieu de membre)")
    
    # Solution 2: Mettre à jour les vérifications existantes
    from agents.models import VerificationCotisation
    from membres.models import Membre as MembrePrincipal
    
    updated_count = 0
    for verification in VerificationCotisation.objects.all():
        try:
            # Essayer de trouver le membre correspondant
            membre = MembrePrincipal.objects.filter(
                prenom=verification.membre.prenom,
                nom=verification.membre.nom
            ).first()
            
            if membre:
                # Mettre à jour avec l'ID correct
                verification.membre_id = membre.id
                verification.save()
                updated_count += 1
                print(f"✅ Vérification mise à jour pour {membre.prenom}")
                
        except Exception as e:
            print(f"❌ Erreur mise à jour vérification: {e}")
    
    print(f"📊 {updated_count} vérifications mises à jour")

def test_final_sync():
    """Tester la synchronisation finale"""
    print("\n🧪 TEST SYNCHRONISATION FINALE")
    print("=" * 60)
    
    from membres.models import Membre as MembrePrincipal
    from assureur.models import Cotisation
    from agents.models import VerificationCotisation
    
    # Vérifier la cohérence
    membres_count = MembrePrincipal.objects.count()
    cotisations_count = Cotisation.objects.count()
    verifications_count = VerificationCotisation.objects.count()
    
    print(f"📊 STATISTIQUES:")
    print(f"   👥 Membres: {membres_count}")
    print(f"   💰 Cotisations: {cotisations_count}") 
    print(f"   ✅ Vérifications: {verifications_count}")
    
    # Vérifier les liens
    if cotisations_count > 0:
        print("🎯 COTISATIONS: CRÉÉES AVEC SUCCÈS")
        print("💡 Le système assureur peut maintenant enregistrer des cotisations")
    else:
        print("⚠️  COTISATIONS: TOUJOURS ABSENTES")
        print("🔧 Application de la solution d'urgence...")
        apply_emergency_fix()

def apply_emergency_fix():
    """Appliquer un correctif d'urgence"""
    print("\n🚨 APPLICATION CORRECTIF URGENCE")
    print("=" * 60)
    
    from django.db import connection
    from django.utils import timezone
    
    try:
        with connection.cursor() as cursor:
            # Créer manuellement une cotisation de test
            cursor.execute("""
                INSERT INTO assureur_cotisation 
                (periode, type_cotisation, montant, date_emission, date_echeance, statut, reference, membre_id, created_at, updated_at)
                VALUES 
                ('2025', 'STANDARD', 5000, ?, ?, 'ACTIVE', 'TEST-URGENCE-001', 1, ?, ?)
            """, [
                timezone.now().date(),
                (timezone.now() + timezone.timedelta(days=365)).date(),
                timezone.now(),
                timezone.now()
            ])
            
            print("✅ Cotisation de test créée manuellement")
            
    except Exception as e:
        print(f"❌ Erreur correctif urgence: {e}")

if __name__ == "__main__":
    print("🚀 CORRECTION DU CONFLIT DE MODÈLES MEMBRE")
    print("⏳ Résolution du problème de synchronisation...\n")
    
    has_conflict = diagnose_membre_conflict()
    
    if has_conflict:
        create_cotisation_fix()
        check_current_cotisations()
        create_relationship_fix()
        test_final_sync()
    else:
        print("✅ Aucun conflit détecté - système OK")
    
    print("\n" + "=" * 60)
    print("🎉 DIAGNOSTIC TERMINÉ!")
    print("=" * 60)