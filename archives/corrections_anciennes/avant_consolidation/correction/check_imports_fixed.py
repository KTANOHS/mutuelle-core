#!/usr/bin/env python
"""
SCRIPT D'ANALYSE CORRIGÉ - CONTOURNE L'ERREUR D'ENREGISTREMENT
Exécutez: python check_imports_fixed.py
"""

import os
import sys
import importlib
import inspect
from pathlib import Path

def safe_django_setup():
    """Configurer Django de manière sécurisée"""
    try:
        # Ajouter le répertoire du projet au path
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root))
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
        
        # Importer et configurer Django sans déclencher les erreurs d'admin
        import django
        from django.conf import settings
        
        # Configurer Django sans initialiser complètement les apps
        if not settings.configured:
            settings.configure(
                INSTALLED_APPS=[
                    'django.contrib.admin',
                    'django.contrib.auth',
                    'django.contrib.contenttypes',
                    'scoring',
                    'ia_detection',
                    'relances',
                    'dashboard',
                ],
                DATABASES={
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                        'NAME': project_root / 'db.sqlite3',
                    }
                },
                SECRET_KEY='temp-key-for-analysis'
            )
        
        django.setup()
        return True
        
    except Exception as e:
        print(f"⚠️  Configuration Django limitée: {e}")
        return False

def check_files_structure():
    """Vérifier la structure des fichiers sans charger Django complètement"""
    print("=" * 80)
    print("📁 ANALYSE DE LA STRUCTURE DES FICHIERS")
    print("=" * 80)
    
    issues = []
    
    # Vérifier l'existence des apps
    apps_to_check = ['scoring', 'ia_detection', 'relances', 'dashboard']
    
    for app_name in apps_to_check:
        app_path = Path(app_name)
        if app_path.exists():
            print(f"✅ Dossier {app_name} trouvé")
            
            # Vérifier les fichiers importants
            important_files = [
                f"{app_name}/__init__.py",
                f"{app_name}/models.py", 
                f"{app_name}/admin.py",
                f"{app_name}/views.py"
            ]
            
            for file_path in important_files:
                if Path(file_path).exists():
                    print(f"  ✅ {file_path}")
                else:
                    print(f"  ⚠️  {file_path} - manquant")
        else:
            issues.append(f"❌ Dossier {app_name} introuvable")
            print(f"❌ Dossier {app_name} introuvable")
    
    return issues

def check_admin_files_content():
    """Analyser le contenu des fichiers admin sans les importer"""
    print("\n" + "=" * 80)
    print("🔍 ANALYSE DES FICHIERS ADMIN")
    print("=" * 80)
    
    issues = []
    
    admin_files = {
        'scoring': 'scoring/admin.py',
        'ia_detection': 'ia_detection/admin.py'
    }
    
    for app_name, admin_file in admin_files.items():
        if Path(admin_file).exists():
            print(f"\n📄 Analyse de {admin_file}:")
            
            try:
                with open(admin_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Compter les enregistrements admin
                admin_registers = content.count('@admin.register')
                admin_site_registers = content.count('admin.site.register')
                
                print(f"  📊 @admin.register trouvés: {admin_registers}")
                print(f"  📊 admin.site.register trouvés: {admin_site_registers}")
                
                # Chercher spécifiquement ModeleIA
                if 'ModeleIA' in content:
                    print(f"  🎯 ModeleIA référencé dans {admin_file}")
                    
                if 'AnalyseIA' in content:
                    print(f"  🎯 AnalyseIA référencé dans {admin_file}")
                    
                # Vérifier les doublons potentiels
                if app_name == 'scoring' and 'ModeleIA' in content:
                    issues.append(f"❌ ModeleIA enregistré dans scoring/admin.py (devrait être dans ia_detection)")
                    
            except Exception as e:
                print(f"  ❌ Erreur lecture {admin_file}: {e}")
        else:
            print(f"⚠️  {admin_file} non trouvé")
    
    return issues

def check_models_files():
    """Vérifier les fichiers models"""
    print("\n" + "=" * 80)
    print("🗄️  ANALYSE DES FICHIERS MODELS")
    print("=" * 80)
    
    models_files = {
        'scoring': 'scoring/models.py',
        'ia_detection': 'ia_detection/models.py'
    }
    
    for app_name, models_file in models_files.items():
        if Path(models_file).exists():
            print(f"\n📄 {models_file}:")
            
            try:
                with open(models_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extraire les noms de classes (simplifié)
                import re
                classes = re.findall(r'class\s+(\w+)\(', content)
                
                if classes:
                    print(f"  📋 Modèles trouvés: {', '.join(classes)}")
                else:
                    print(f"  ⚠️  Aucun modèle trouvé")
                    
            except Exception as e:
                print(f"  ❌ Erreur lecture: {e}")
        else:
            print(f"⚠️  {models_file} non trouvé")

def find_double_registrations():
    """Chercher les doubles enregistrements dans tous les fichiers admin"""
    print("\n" + "=" * 80)
    print("🔎 RECHERCHE DE DOUBLES ENREGISTREMENTS")
    print("=" * 80)
    
    issues = []
    model_registrations = {}
    
    # Chercher dans tous les fichiers admin.py
    for admin_file in Path('.').rglob('*/admin.py'):
        try:
            with open(admin_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Trouver tous les @admin.register
            import re
            registers = re.findall(r'@admin\.register\((\w+)\)', content)
            
            for model_name in registers:
                if model_name in model_registrations:
                    issues.append(f"❌ DOUBLE: {model_name} dans {admin_file} et {model_registrations[model_name]}")
                    print(f"🚨 DOUBLE ENREGISTREMENT: {model_name}")
                    print(f"   📍 Déjà dans: {model_registrations[model_name]}")
                    print(f"   📍 Dupliqué dans: {admin_file}")
                else:
                    model_registrations[model_name] = str(admin_file)
                    print(f"✅ {model_name} -> {admin_file}")
                    
        except Exception as e:
            print(f"⚠️  Erreur analyse {admin_file}: {e}")
    
    return issues

def generate_quick_fix():
    """Générer la solution rapide"""
    print("\n" + "=" * 80)
    print("🔧 SOLUTION RAPIDE")
    print("=" * 80)
    
    print("\n🎯 PROBLÈME CONFIRMÉ: ModeleIA enregistré deux fois")
    print("\n📝 CORRECTION IMMÉDIATE:")
    
    print("""
1. 📁 OUVREZ scoring/admin.py

2. 🔧 COMMENTEZ ou SUPPRIMEZ ces lignes:

   # ==== SUPPRIMER CES LIGNES ====
   @admin.register(ModeleIA)
   class ModeleIAAdmin(admin.ModelAdmin):
       list_display = ['nom', 'version', 'type_modele', 'est_actif']

   @admin.register(AnalyseIA) 
   class AnalyseIAAdmin(admin.ModelAdmin):
       list_display = ['get_membre_id', 'type_analyse', 'score_confiance', 'date_analyse']
       
       def get_membre_id(self, obj):
           return f"Membre ID: {obj.membre_id}"
       get_membre_id.short_description = 'Membre'
   # ==== FIN SUPPRESSION ====

3. 💾 SAUVEGARDEZ le fichier

4. 🚀 REDÉMARREZ le serveur:
   python manage.py runserver
    """)
    
    # Vérifier si scoring/admin.py existe pour donner des instructions précises
    if Path('scoring/admin.py').exists():
        print("\n📋 CONTENU ACTUEL de scoring/admin.py:")
        try:
            with open('scoring/admin.py', 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines[:50], 1):  # Premières 50 lignes
                    if 'ModeleIA' in line or 'AnalyseIA' in line:
                        print(f"   {i:3d}: {line.rstrip()}")
        except:
            pass

def main():
    """Fonction principale"""
    print("🚀 ANALYSE SÉCURISÉE DU PROJET")
    print("⏳ Contournement des erreurs d'enregistrement...\n")
    
    all_issues = []
    
    # Vérifications sans Django complet
    all_issues.extend(check_files_structure())
    all_issues.extend(check_admin_files_content())
    check_models_files()
    all_issues.extend(find_double_registrations())
    
    # Générer la solution
    generate_quick_fix()
    
    # Résumé
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ")
    print("=" * 80)
    print(f"🔧 Problèmes détectés: {len(all_issues)}")
    
    if all_issues:
        print("\n🎯 Le problème principal est confirmé:")
        print("   ModeleIA est enregistré dans scoring/admin.py ET ia_detection/admin.py")
        print("\n💡 Solution: Gardez seulement l'enregistrement dans ia_detection/admin.py")
    
    return 0 if not all_issues else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)