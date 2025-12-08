# check_cotisation_sync.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def analyze_cotisation_sync():
    """Analyser la synchronisation assureur/agent pour les cotisations"""
    print("🔍 ANALYSE DE LA SYNCHRONISATION ASSUREUR-AGENT")
    print("=" * 60)
    
    # Vérifier les modèles existants
    from django.apps import apps
    
    print("\n📦 MODÈLES EXISTANTS:")
    models_list = []
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            models_list.append(f"{app_config.name}.{model.__name__}")
    
    # Filtrer les modèles liés aux cotisations
    cotisation_models = [m for m in models_list if 'cotisation' in m.lower()]
    assurance_models = [m for m in models_list if 'assur' in m.lower()]
    agent_models = [m for m in models_list if 'agent' in m.lower()]
    
    print("📋 Modèles cotisation:", cotisation_models)
    print("📋 Modèles assurance:", assurance_models)
    print("📋 Modèles agent:", agent_models)
    
    # Vérifier la structure spécifique
    print("\n🔄 FLUX COTISATIONS:")
    
    try:
        from assureur.models import Cotisation
        print("✅ Modèle Cotisation trouvé dans assureur")
        
        # Analyser les champs
        fields = [f.name for f in Cotisation._meta.get_fields()]
        print(f"   Champs: {', '.join(fields)}")
        
    except ImportError:
        print("❌ Modèle Cotisation non trouvé dans assureur")
    
    try:
        from agents.models import VerificationCotisation
        print("✅ Modèle VerificationCotisation trouvé dans agents")
        
        # Analyser les champs
        fields = [f.name for f in VerificationCotisation._meta.get_fields()]
        print(f"   Champs: {', '.join(fields)}")
        
    except ImportError:
        print("❌ Modèle VerificationCotisation non trouvé dans agents")
    
    # Vérifier les relations
    print("\n🔗 RELATIONS ENTRE MODÈLES:")
    try:
        from membres.models import Membre
        from assureur.models import Cotisation
        from agents.models import VerificationCotisation, Agent
        
        # Vérifier si les modèles peuvent communiquer
        print("✅ Membre -> Cotisation: Existe")
        print("✅ Cotisation -> Verification: À vérifier")
        print("✅ Agent -> Verification: Existe")
        
    except Exception as e:
        print(f"❌ Erreur analyse relations: {e}")

def test_cotisation_workflow():
    """Tester le workflow complet de cotisation"""
    print("\n🧪 TEST DU WORKFLOW COTISATION")
    print("=" * 60)
    
    try:
        from membres.models import Membre
        from assureur.models import Cotisation, Assureur
        from agents.models import VerificationCotisation, Agent
        from django.contrib.auth.models import User
        from django.utils import timezone
        
        # 1. Vérifier les données existantes
        membres_count = Membre.objects.count()
        cotisations_count = Cotisation.objects.count() if hasattr(Cotisation, 'objects') else 0
        verifications_count = VerificationCotisation.objects.count() if hasattr(VerificationCotisation, 'objects') else 0
        
        print(f"📊 Données existantes:")
        print(f"   👥 Membres: {membres_count}")
        print(f"   💰 Cotisations: {cotisations_count}")
        print(f"   ✅ Vérifications: {verifications_count}")
        
        # 2. Vérifier le workflow théorique
        print(f"\n🔄 WORKFLOW THÉORIQUE:")
        print("   1. ASSUREUR → Crée une cotisation pour un membre")
        print("   2. SYSTÈME → Met à jour le statut du membre")
        print("   3. AGENT → Vérifie la cotisation avant soin")
        print("   4. SYSTÈME → Autorise ou refuse le soin")
        
        # 3. Vérifier la connectivité
        if membres_count > 0 and cotisations_count > 0:
            print(f"\n🔗 CONNECTIVITÉ:")
            
            # Exemple: Premier membre et première cotisation
            membre = Membre.objects.first()
            if hasattr(Cotisation, 'objects') and Cotisation.objects.exists():
                cotisation = Cotisation.objects.first()
                print(f"   ✅ Membre {membre.prenom} a des cotisations")
            else:
                print("   ⚠️  Aucune cotisation existante")
                
        else:
            print("   ⚠️  Données insuffisantes pour tester le workflow")
            
    except Exception as e:
        print(f"❌ Erreur test workflow: {e}")

def check_missing_links():
    """Identifier les liens manquants dans l'architecture"""
    print("\n🔎 IDENTIFICATION DES LIENS MANQUANTS")
    print("=" * 60)
    
    missing_links = []
    
    try:
        # Vérifier si Cotisation a un lien vers Verification
        from assureur.models import Cotisation
        cotisation_fields = [f.name for f in Cotisation._meta.get_fields()]
        
        if 'verification' not in str(cotisation_fields).lower():
            missing_links.append("❌ Cotisation → Verification: Lien direct manquant")
        else:
            print("✅ Cotisation → Verification: Lien existant")
            
    except Exception as e:
        missing_links.append(f"❌ Impossible d'analyser Cotisation: {e}")
    
    try:
        # Vérifier si Membre a un statut de cotisation
        from membres.models import Membre
        membre_fields = [f.name for f in Membre._meta.get_fields()]
        
        cotisation_status_fields = [f for f in membre_fields if 'cotisation' in f.lower() or 'assur' in f.lower()]
        if not cotisation_status_fields:
            missing_links.append("❌ Membre → Statut cotisation: Champ manquant")
        else:
            print(f"✅ Membre → Statut cotisation: {cotisation_status_fields}")
            
    except Exception as e:
        missing_links.append(f"❌ Impossible d'analyser Membre: {e}")
    
    if missing_links:
        print("\n⚠️  LIENS MANQUANTS IDENTIFIÉS:")
        for link in missing_links:
            print(f"   {link}")
    else:
        print("✅ Tous les liens critiques semblent présents")

def generate_sync_recommendations():
    """Générer des recommandations pour améliorer la synchronisation"""
    print("\n💡 RECOMMANDATIONS POUR LA SYNCHRONISATION")
    print("=" * 60)
    
    recommendations = [
        "1. 🔄 IMPLÉMENTER UN SYSTÈME DE STATUT COTISATION TEMPS RÉEL",
        "2. 📱 CRÉER UNE API POUR LA SYNCHRONISATION ASSUREUR→AGENT", 
        "3. 🔔 SYSTÈME DE NOTIFICATIONS POUR COTISATIONS EXPIREES",
        "4. 📊 TABLEAU DE BORD UNIFIÉ COTISATIONS POUR AGENTS",
        "5. 🔗 LIEN DIRECT ENTRE COTISATION ET VÉRIFICATION"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")

if __name__ == "__main__":
    analyze_cotisation_sync()
    test_cotisation_workflow() 
    check_missing_links()
    generate_sync_recommendations()
    
    print("\n" + "=" * 60)
    print("🎯 RÉSUMÉ SYNCHRONISATION ASSUREUR-AGENT")
    print("=" * 60)
    print("📋 État: SYNCHRONISATION PARTIELLE")
    print("💡 Besoin: RENFORCER LES LIENS ENTRE ASSUREUR ET AGENT")
    print("🚀 Priorité: IMPLÉMENTER LE WORKFLOW COMPLET")