# validate_apps.py
import os
import django
from django.apps import apps

def setup_django():
    """Configurer l'environnement Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()

def validate_agents_app():
    """Valider l'application agents"""
    print("🔧 VALIDATION APPLICATION AGENTS")
    
    try:
        # Vérifier que l'application est installée
        apps.get_app_config('agents')
        print("✅ Application agents installée")
        
        # Vérifier les modèles
        expected_models = ['Agent', 'RoleAgent', 'PermissionAgent']
        models_found = []
        
        for model_name in expected_models:
            try:
                model = apps.get_model('agents', model_name)
                models_found.append(model_name)
                print(f"✅ Modèle {model_name} trouvé")
                
                # Vérifier quelques champs basiques
                fields = [f.name for f in model._meta.get_fields()]
                print(f"   📋 Champs: {len(fields)} champs détectés")
                
            except LookupError:
                print(f"❌ Modèle {model_name} non trouvé")
        
        print(f"📊 Résumé agents: {len(models_found)}/{len(expected_models)} modèles trouvés")
        return len(models_found) > 0
        
    except LookupError:
        print("❌ Application agents non trouvée")
        return False

def validate_communication_app():
    """Valider l'application communication"""
    print("🔧 VALIDATION APPLICATION COMMUNICATION")
    
    try:
        # Vérifier que l'application est installée
        apps.get_app_config('communication')
        print("✅ Application communication installée")
        
        # Vérifier les modèles
        expected_models = ['Message', 'Notification']
        models_found = []
        
        for model_name in expected_models:
            try:
                model = apps.get_model('communication', model_name)
                models_found.append(model_name)
                print(f"✅ Modèle {model_name} trouvé")
                
                # Vérifier quelques champs basiques
                fields = [f.name for f in model._meta.get_fields()]
                print(f"   📋 Champs: {len(fields)} champs détectés")
                
            except LookupError:
                print(f"❌ Modèle {model_name} non trouvé")
        
        print(f"📊 Résumé communication: {len(models_found)}/{len(expected_models)} modèles trouvés")
        return len(models_found) > 0
        
    except LookupError:
        print("❌ Application communication non trouvée")
        return False

def validate_channels():
    """Valider Channels pour WebSocket"""
    print("🔧 VALIDATION CHANNELS")
    
    try:
        import channels
        print("✅ Channels installé")
        
        # Vérifier la configuration ASGI
        from django.conf import settings
        if hasattr(settings, 'ASGI_APPLICATION'):
            print("✅ Configuration ASGI détectée")
        else:
            print("⚠️  Configuration ASGI non détectée")
            
        return True
    except ImportError:
        print("❌ Channels non installé")
        return False

def check_double_registration():
    """Vérifier les doubles enregistrements de modèles"""
    print("\n🔍 VERIFICATION DOUBLES ENREGISTREMENTS")
    
    # Cette vérification explique les warnings vus au démarrage
    from django.contrib import admin
    from django.contrib.admin.sites import site
    
    registered_models = list(site._registry.keys())
    
    # Compter les modèles par application
    app_counts = {}
    for model in registered_models:
        app_label = model._meta.app_label
        app_counts[app_label] = app_counts.get(app_label, 0) + 1
    
    print("📊 Modèles enregistrés dans l'admin par application:")
    for app, count in app_counts.items():
        print(f"   📁 {app}: {count} modèles")
    
    # Vérifier spécifiquement communication
    comm_models = [m for m in registered_models if m._meta.app_label == 'communication']
    if len(comm_models) > 2:  # Normalement 2 modèles attendus
        print(f"⚠️  Attention: {len(comm_models)} modèles communication détectés (doubles possibles)")
    else:
        print("✅ Aucun double enregistrement détecté")

def run_validations():
    """Exécuter toutes les validations"""
    print("🚀 LANCEMENT DES VALIDATIONS")
    print("=" * 50)
    
    results = {
        'agents': validate_agents_app(),
        'communication': validate_communication_app(),
        'channels': validate_channels(),
    }
    
    check_double_registration()
    
    print("=" * 50)
    print("📊 RÉSULTATS DES VALIDATIONS:")
    
    success_count = sum(results.values())
    total_count = len(results)
    
    print(f"✅ {success_count}/{total_count} validations réussies")
    
    if success_count == total_count:
        print("🎉 Toutes les validations sont réussies!")
        return True
    else:
        print("💥 Certaines validations ont échoué")
        return False

if __name__ == "__main__":
    setup_django()
    run_validations()