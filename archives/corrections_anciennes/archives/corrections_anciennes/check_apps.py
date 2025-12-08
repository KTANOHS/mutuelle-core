# check_apps.py
import os
import django
import sys
from django.apps import apps
from django.conf import settings
from django.core.management import execute_from_command_line

def setup_django():
    """Configurer l'environnement Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()

def check_app_configuration():
    """Vérifier la configuration des applications"""
    print("🔍 ANALYSE DES APPLICATIONS DJANGO")
    print("=" * 60)
    
    # Vérifier les applications installées
    installed_apps = settings.INSTALLED_APPS
    print(f"📊 Applications installées ({len(installed_apps)}):")
    
    target_apps = ['agents', 'communication', 'channels']
    for app in target_apps:
        status = "✅" if app in installed_apps else "❌"
        print(f"   {status} {app}")
    
    print("\n" + "=" * 60)

def check_models():
    """Vérifier les modèles des applications"""
    print("🗄️  VERIFICATION DES MODELES")
    print("=" * 60)
    
    app_configs = {
        'agents': ['Agent', 'RoleAgent', 'PermissionAgent'],
        'communication': ['Message', 'Notification']
    }
    
    for app_label, expected_models in app_configs.items():
        print(f"\n📁 Application: {app_label}")
        
        try:
            app_config = apps.get_app_config(app_label)
            models = list(app_config.get_models())  # 🔥 CORRECTION: Convertir en liste
            
            print(f"   ✅ Application trouvée")
            print(f"   📋 Modèles détectés ({len(models)}):")
            
            for model in models:
                model_name = model.__name__
                status = "✅" if model_name in expected_models else "⚠️ "
                print(f"      {status} {model_name}")
                
        except LookupError:
            print(f"   ❌ Application non trouvée")
    
    print("=" * 60)

def check_admin_configuration():
    """Vérifier la configuration admin"""
    print("\n⚙️  CONFIGURATION ADMIN")
    print("=" * 60)
    
    from django.contrib import admin
    from django.contrib.admin.sites import site
    
    registered_models = list(site._registry.keys())
    
    communication_models = [model for model in registered_models 
                          if model._meta.app_label == 'communication']
    agents_models = [model for model in registered_models 
                    if model._meta.app_label == 'agents']
    
    print(f"📝 Modèles communication enregistrés: {len(communication_models)}")
    for model in communication_models:
        print(f"   ✅ {model.__name__}")
    
    print(f"\n📝 Modèles agents enregistrés: {len(agents_models)}")
    for model in agents_models:
        print(f"   ✅ {model.__name__}")
    
    print("=" * 60)

def check_database():
    """Vérifier la base de données"""
    print("\n🗃️  VERIFICATION BASE DE DONNEES")
    print("=" * 60)
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            # Compter les enregistrements
            tables_to_check = [
                'communication_messageinterne',
                'communication_notification', 
                'agents_agent',
                'agents_roleagent'
            ]
            
            for table in tables_to_check:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"   📊 {table}: {count} enregistrement(s)")
                except Exception as e:
                    print(f"   ❌ {table}: Table non trouvée - {e}")
                    
    except Exception as e:
        print(f"   ❌ Erreur base de données: {e}")
    
    print("=" * 60)

def run_system_checks():
    """Exécuter les vérifications système Django"""
    print("\n🔧 VERIFICATIONS SYSTEME DJANGO")
    print("=" * 60)
    
    try:
        from django.core.management import call_command
        call_command('check')
        print("✅ Toutes les vérifications système passées avec succès")
    except Exception as e:
        print(f"❌ Erreurs système détectées: {e}")
    
    print("=" * 60)

def main():
    """Fonction principale"""
    try:
        setup_django()
        
        print("🚀 LANCEMENT DE L'ANALYSE DES APPLICATIONS")
        print("=" * 60)
        
        check_app_configuration()
        check_models()
        check_admin_configuration()
        check_database()
        run_system_checks()
        
        print("\n🎉 ANALYSE TERMINÉE AVEC SUCCÈS!")
        print("=" * 60)
        
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()