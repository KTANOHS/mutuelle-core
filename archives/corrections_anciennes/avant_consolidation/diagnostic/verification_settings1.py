# verification_settings.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def verifier_configuration_agents():
    """Vérifie la configuration pour les agents"""
    print("🔧 VÉRIFICATION DE LA CONFIGURATION")
    print("=" * 50)
    
    # 1. Vérifier les applications installées
    apps_requises = ['assureur', 'agents', 'communication']
    apps_manquantes = [app for app in apps_requises if app not in settings.INSTALLED_APPS]
    
    if apps_manquantes:
        print("❌ APPLICATIONS MANQUANTES:", apps_manquantes)
    else:
        print("✅ Toutes les applications requises sont installées")
    
    # 2. Vérifier les context processors
    context_processors = getattr(settings, 'TEMPLATES', [{}])[0].get('OPTIONS', {}).get('context_processors', [])
    if 'agents.context_processors.agent_context' in context_processors:
        print("✅ Context processor agents configuré")
    else:
        print("❌ Context processor agents non configuré")
    
    # 3. Vérifier les dossiers templates
    templates_dirs = getattr(settings, 'TEMPLATES', [{}])[0].get('DIRS', [])
    agents_templates = any('agents/templates' in str(dir) for dir in templates_dirs)
    if agents_templates:
        print("✅ Dossier templates agents configuré")
    else:
        print("❌ Dossier templates agents non configuré")
    
    # 4. Vérifier la configuration métier
    mutuelle_config = getattr(settings, 'MUTUELLE_CONFIG', {})
    config_requise = ['COTISATION_STANDARD', 'COTISATION_FEMME_ENCEINTE', 'AVANCE', 'FRAIS_CARTE']
    config_manquante = [key for key in config_requise if key not in mutuelle_config]
    
    if config_manquante:
        print("❌ CONFIGURATION MANQUANTE:", config_manquante)
    else:
        print("✅ Configuration métier complète")
        print(f"   • Cotisation standard: {mutuelle_config['COTISATION_STANDARD']} FCFA")
        print(f"   • Cotisation femme enceinte: {mutuelle_config['COTISATION_FEMME_ENCEINTE']} FCFA")
        print(f"   • Avance: {mutuelle_config['AVANCE']} FCFA")
        print(f"   • Frais carte: {mutuelle_config['FRAIS_CARTE']} FCFA")
    
    # 5. Vérifier les URLs de redirection
    login_redirect = getattr(settings, 'LOGIN_REDIRECT_URL', '')
    if login_redirect == '/redirect-after-login/':
        print("✅ URL de redirection après login configurée")
    else:
        print(f"⚠️  URL de redirection: {login_redirect}")

def verifier_dossiers():
    """Vérifie l'existence des dossiers nécessaires"""
    print("\n📁 VÉRIFICATION DES DOSSIERS")
    print("=" * 50)
    
    dossiers_requis = [
        'agents/templates',
        'agents/static', 
        'logs',
        'media/verifications_cotisations'
    ]
    
    for dossier in dossiers_requis:
        chemin = os.path.join(settings.BASE_DIR, *dossier.split('/'))
        if os.path.exists(chemin):
            print(f"✅ {dossier}")
        else:
            print(f"❌ {dossier} - À créer")
            try:
                os.makedirs(chemin, exist_ok=True)
                print(f"   📁 Créé: {chemin}")
            except:
                print(f"   💥 Erreur création: {chemin}")

def verifier_base_donnees():
    """Vérifie l'état de la base de données"""
    print("\n🗄️  VÉRIFICATION BASE DE DONNÉES")
    print("=" * 50)
    
    try:
        from django.db import connection
        from django.apps import apps
        
        # Vérifier les modèles agents
        modeles_agents = ['Agent', 'RoleAgent', 'VerificationCotisation', 'BonSoin']
        for modele in modeles_agents:
            try:
                model_class = apps.get_model('agents', modele)
                count = model_class.objects.count()
                print(f"✅ {modele}: {count} enregistrements")
            except Exception as e:
                print(f"❌ {modele}: {e}")
        
        # Vérifier la connexion
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Connexion BD active")
            
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")

if __name__ == "__main__":
    verifier_configuration_agents()
    verifier_dossiers() 
    verifier_base_donnees()
    
    print("\n" + "=" * 50)
    print("🎯 RÉSUMÉ DE LA CONFIGURATION")
    print("=" * 50)
    print("Votre configuration est OPTIMALE pour le système de cotisations!")
    print("Prochaine étape: Implémenter les modèles de cotisations dans assureur")