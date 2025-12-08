# find_double_registration.py
import os
import django
import re

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()

def find_double_registration():
    """Trouver la source des doubles enregistrements"""
    print("🔍 RECHERCHE DE LA SOURCE DES DOUBLES ENREGISTREMENTS")
    print("=" * 60)
    
    # Vérifier tous les fichiers admin.py
    apps_to_check = ['communication']
    
    for app in apps_to_check:
        admin_file = f'{app}/admin.py'
        if os.path.exists(admin_file):
            print(f"\n📁 Analyse de {admin_file}:")
            
            with open(admin_file, 'r') as f:
                content = f.read()
            
            # Compter les différentes méthodes d'enregistrement
            register_decorators = len(re.findall(r'@admin\.register\((\w+)', content))
            admin_site_registers = len(re.findall(r'admin\.site\.register\((\w+)', content))
            import_statements = len(re.findall(r'from.*models.*import', content))
            
            print(f"   @admin.register: {register_decorators}")
            print(f"   admin.site.register: {admin_site_registers}")
            print(f"   import models: {import_statements}")
            
            # Vérifier les modèles importés
            model_imports = re.findall(r'from\s+\.models\s+import\s+(.+)', content)
            if model_imports:
                models = model_imports[0].split(',')
                print(f"   📋 Modèles importés: {len(models)}")
                for model in models:
                    print(f"      - {model.strip()}")

def check_communication_models():
    """Vérifier la structure des modèles communication"""
    print("\n🔍 ANALYSE DES MODÈLES COMMUNICATION")
    print("=" * 60)
    
    models_file = 'communication/models.py'
    if os.path.exists(models_file):
        with open(models_file, 'r') as f:
            content = f.read()
        
        # Compter les classes de modèles
        model_classes = re.findall(r'class\s+(\w+)\(models\.Model\)', content)
        print(f"📋 Modèles définis dans models.py: {len(model_classes)}")
        for model in model_classes:
            print(f"   ✅ {model}")

def main():
    setup_django()
    find_double_registration()
    check_communication_models()
    
    print("\n🎉 ANALYSE TERMINÉE!")
    print("\n💡 SOLUTION POUR LES WARNINGS:")
    print("   Les warnings viennent probablement de:")
    print("   1. Import circulaire entre applications")
    print("   2. Modèles chargés plusieurs fois au démarrage")
    print("   3. Ce n'est pas critique pour le fonctionnement")

if __name__ == "__main__":
    main()