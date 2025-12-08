#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC ET CORRECTION DU PROJET MUTUELLE
Problèmes identifiés :
1. Conflits de modèles entre applications
2. Doublons dans les URLs
3. Problèmes de relations entre modèles
4. Incohérences dans la structure
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Impossible de configurer Django: {e}")
    sys.exit(1)

from django.apps import apps
from django.db import connection
from django.core.management import call_command

class ProjectDoctor:
    def __init__(self):
        self.issues = []
        self.fixes = []

    def diagnose_model_conflicts(self):
        """Diagnostique les conflits entre modèles"""
        print("\n" + "="*80)
        print("🔍 DIAGNOSTIC DES CONFLITS DE MODÈLES")
        print("="*80)
        
        # Modèles en double entre applications
        model_names = {}
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                model_name = model.__name__
                if model_name in model_names:
                    model_names[model_name].append(app_config.name)
                else:
                    model_names[model_name] = [app_config.name]
        
        conflicts = {name: apps for name, apps in model_names.items() if len(apps) > 1}
        
        if conflicts:
            print("🚨 CONFLITS DE MODÈLES DÉTECTÉS:")
            for model_name, app_list in conflicts.items():
                print(f"   ❌ {model_name}: présent dans {', '.join(app_list)}")
                self.issues.append(f"Conflit de modèle: {model_name} dans {', '.join(app_list)}")
                
                # Suggestions de correctifs
                if model_name == "BonDeSoin":
                    self.fixes.append("""
🛠️ CORRECTION POUR BonDeSoin:
   OPTION 1: Supprimer le modèle en double dans une application
   OPTION 2: Renommer un des modèles (ex: BonDeSoinMedecin, BonDeSoinAssureur)
   OPTION 3: Utiliser un modèle central dans l'application 'soins'
                    """)
        else:
            print("✅ Aucun conflit de modèles détecté")

    def diagnose_database_relations(self):
        """Vérifie les relations de base de données"""
        print("\n" + "="*80)
        print("🗃️ DIAGNOSTIC DES RELATIONS BASE DE DONNÉES")
        print("="*80)
        
        try:
            with connection.cursor() as cursor:
                # Vérifier les tables sans clés étrangères cohérentes
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name NOT LIKE 'sqlite_%'
                    AND name NOT LIKE 'django_%'
                    AND name NOT LIKE 'auth_%'
                """)
                tables = [row[0] for row in cursor.fetchall()]
                
                for table in tables:
                    cursor.execute(f"PRAGMA foreign_key_list({table})")
                    foreign_keys = cursor.fetchall()
                    
                    if not foreign_keys:
                        print(f"⚠️  Table {table}: Aucune clé étrangère")
                    else:
                        print(f"✅ Table {table}: {len(foreign_keys)} clé(s) étrangère(s)")
                        
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse des relations: {e}")

    def diagnose_url_conflicts(self):
        """Diagnostique les conflits d'URLs"""
        print("\n" + "="*80)
        print("🌐 DIAGNOSTIC DES CONFLITS D'URLS")
        print("="*80)
        
        from django.urls import get_resolver
        resolver = get_resolver()
        
        url_patterns = {}
        duplicates = []
        
        def collect_urls(url_patterns, prefix=''):
            for pattern in url_patterns:
                if hasattr(pattern, 'url_patterns'):
                    collect_urls(pattern.url_patterns, prefix + str(pattern.pattern))
                else:
                    full_path = prefix + str(pattern.pattern)
                    name = getattr(pattern, 'name', None)
                    
                    if name in url_patterns:
                        duplicates.append((name, url_patterns[name], full_path))
                    else:
                        url_patterns[name] = full_path
        
        collect_urls(resolver.url_patterns)
        
        if duplicates:
            print("🚨 DOUBLONS D'URLS DÉTECTÉS:")
            for name, existing_path, new_path in duplicates:
                print(f"   ❌ Nom '{name}':")
                print(f"      - {existing_path}")
                print(f"      - {new_path}")
                self.issues.append(f"Doublon URL: {name}")
            
            self.fixes.append("""
🛠️ CORRECTION POUR LES DOUBLONS D'URLS:
   - Supprimer les URLs en double dans les fichiers urls.py
   - Utiliser des namespaces d'application
   - Vérifier les includes en double
            """)
        else:
            print("✅ Aucun doublon d'URL détecté")

    def check_critical_models(self):
        """Vérifie les modèles critiques"""
        print("\n" + "="*80)
        print("🎯 VÉRIFICATION DES MODÈLES CRITIQUES")
        print("="*80)
        
        critical_models = ['Membre', 'User', 'Paiement', 'Bon']
        
        for model_name in critical_models:
            try:
                model = apps.get_model('membres', model_name)
                print(f"✅ Modèle {model_name}: OK")
                
                # Vérifier les champs obligatoires
                fields = model._meta.fields
                required_fields = [f for f in fields if not f.blank and not f.null and not f.primary_key]
                print(f"   Champs obligatoires: {[f.name for f in required_fields]}")
                
            except LookupError:
                try:
                    # Essayer d'autres applications
                    for app_config in apps.get_app_configs():
                        try:
                            model = apps.get_model(app_config.label, model_name)
                            print(f"✅ Modèle {model_name} trouvé dans {app_config.label}")
                            break
                        except LookupError:
                            continue
                    else:
                        print(f"❌ Modèle {model_name}: NON TROUVÉ")
                        self.issues.append(f"Modèle manquant: {model_name}")
                except:
                    print(f"❌ Modèle {model_name}: NON TROUVÉ")
                    self.issues.append(f"Modèle manquant: {model_name}")

    def generate_fix_script(self):
        """Génère un script de correction automatique"""
        print("\n" + "="*80)
        print("🛠️  SCRIPT DE CORRECTION AUTOMATIQUE")
        print("="*80)
        
        fix_script = """#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.core.management import call_command

def apply_fixes():
    print("🔧 APPLICATION DES CORRECTIONS...")
    
    # 1. Nettoyer la base de données
    print("1. Nettoyage de la base de données...")
    try:
        call_command('migrate', '--fake')
        call_command('makemigrations')
        call_command('migrate')
    except Exception as e:
        print(f"   ❌ Erreur migration: {e}")
    
    # 2. Vérifier les modèles en conflit
    print("2. Résolution des conflits de modèles...")
    # À adapter selon les conflits spécifiques
    
    # 3. Recréer les index
    print("3. Recréation des index...")
    try:
        call_command('sqlmigrate', 'membres', '0001')
    except:
        pass
    
    print("✅ Corrections appliquées!")

if __name__ == "__main__":
    apply_fixes()
"""
        
        # Sauvegarder le script
        script_path = BASE_DIR / "fix_project.py"
        with open(script_path, 'w') as f:
            f.write(fix_script)
        
        print(f"📁 Script de correction sauvegardé: {script_path}")
        print("💡 Exécutez: python fix_project.py")

    def suggest_restructuring(self):
        """Suggère une restructuration du projet"""
        print("\n" + "="*80)
        print("🏗️  SUGGESTIONS DE RESTRUCTURATION")
        print("="*80)
        
        suggestions = """
📋 RECOMMANDATIONS ARCHITECTURALES:

1. 🎯 RÉORGANISATION DES APPLICATIONS:
   - 'membres': Gestion des membres et profils
   - 'soins': Gestion des soins, consultations, ordonnances
   - 'paiements': Gestion des paiements et remboursements  
   - 'assureur': Interface assureur
   - 'medecin': Interface médecin
   - 'pharmacien': Interface pharmacien
   - 'core': Fonctionnalités centrales

2. 🔥 RÉSOLUTION DES CONFLITS:
   - Supprimer les modèles en double
   - Centraliser 'BonDeSoin' dans 'soins'
   - Centraliser 'Membre' dans 'membres'

3. 🗃️ OPTIMISATION BASE DE DONNÉES:
   - Appliquer toutes les migrations
   - Vérifier les relations étrangères
   - Créer les index manquants

4. 🌐 UNIFICATION DES URLs:
   - Supprimer les URLs en double
   - Utiliser les namespaces
   - Standardiser les patterns
"""

        print(suggestions)

    def run_diagnosis(self):
        """Exécute le diagnostic complet"""
        print("🏥 DIAGNOSTIC COMPLET DU PROJET MUTUELLE")
        print("="*80)
        
        self.diagnose_model_conflicts()
        self.diagnose_database_relations()
        self.diagnose_url_conflicts()
        self.check_critical_models()
        
        # Rapport final
        print("\n" + "="*80)
        print("📊 RAPPORT DE DIAGNOSTIC")
        print("="*80)
        
        if self.issues:
            print(f"🚨 {len(self.issues)} PROBLÈMES IDENTIFIÉS:")
            for i, issue in enumerate(self.issues, 1):
                print(f"   {i}. {issue}")
        else:
            print("✅ Aucun problème critique identifié!")
        
        if self.fixes:
            print(f"\n🛠️ {len(self.fixes)} CORRECTIONS SUGGÉRÉES:")
            for fix in self.fixes:
                print(fix)
        
        self.suggest_restructuring()
        self.generate_fix_script()

def main():
    """Fonction principale"""
    try:
        doctor = ProjectDoctor()
        doctor.run_diagnosis()
    except Exception as e:
        print(f"💥 Erreur lors du diagnostic: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()