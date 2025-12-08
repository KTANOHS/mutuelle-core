#!/usr/bin/env python3
"""
Script d'analyse post-suppression pour les apps membres et medecin
Vérifie l'état des modèles, données, relations et configurations
"""

import os
import django
import sys
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.apps import apps
from django.db import connection, models
from django.contrib.auth import get_user_model
from django.core.management import call_command
from io import StringIO

class PostDeleteAnalyzer:
    def __init__(self):
        self.user_model = get_user_model()
        self.problems = []
        self.solutions = []
    
    def analyze_apps(self):
        """Analyse complète des applications membres et medecin"""
        print("🔍 ANALYSE POST-SUPPRESSION - MEMBRES & MÉDECIN")
        print("=" * 70)
        
        apps_to_analyze = ['membres', 'medecins', 'medecin']
        
        for app_name in apps_to_analyze:
            self.analyze_single_app(app_name)
        
        self.analyze_cross_app_relations()
        self.check_migrations_state()
        self.generate_recovery_plan()
    
    def analyze_single_app(self, app_name):
        """Analyse une application spécifique"""
        print(f"\n📦 ANALYSE DE L'APPLICATION: {app_name.upper()}")
        print("-" * 50)
        
        try:
            app_config = apps.get_app_config(app_name)
            models_list = app_config.get_models()
            
            print(f"✅ Application trouvée: {app_name}")
            print(f"📋 Modèles dans {app_name}: {len(models_list)}")
            
            for model in models_list:
                self.analyze_model(model)
                
        except LookupError:
            print(f"❌ Application non trouvée: {app_name}")
            self.problems.append(f"Application {app_name} non installée")
            self.solutions.append(f"Ajouter '{app_name}' à INSTALLED_APPS dans settings.py")
    
    def analyze_model(self, model):
        """Analyse un modèle spécifique"""
        model_name = model._meta.model_name
        app_label = model._meta.app_label
        
        print(f"\n   🗃️  Modèle: {model_name}")
        print(f"   📊 Statistiques:", end=" ")
        
        try:
            count = model.objects.count()
            print(f"{count} enregistrement(s)")
            
            # Analyser les données récentes
            if count > 0:
                self.analyze_model_data(model)
            else:
                print("   ⚠️  AUCUNE DONNÉE - Modèle vide")
                self.problems.append(f"Modèle {app_label}.{model_name} est vide")
                
        except Exception as e:
            print(f"❌ ERREUR: {e}")
            self.problems.append(f"Erreur accès modèle {app_label}.{model_name}: {e}")
    
    def analyze_model_data(self, model):
        """Analyse les données d'un modèle"""
        # Vérifier les champs importants
        fields = [f.name for f in model._meta.fields]
        
        # Vérifier les dates de création
        date_fields = [f for f in fields if 'date' in f.lower() or 'created' in f.lower()]
        if date_fields:
            recent_data = model.objects.order_by(f'-{date_fields[0]}')[:5]
            print(f"   📅 Données récentes: {recent_data.count()}")

        # Vérifier les relations
        related_fields = model._meta.get_fields()
        for field in related_fields:
            if hasattr(field, 'related_model') and field.related_model:
                related_count = model.objects.filter(**{f'{field.name}__isnull': False}).count()
                print(f"   🔗 Relations {field.name}: {related_count}")
    
    def analyze_cross_app_relations(self):
        """Analyse les relations entre membres et medecin"""
        print(f"\n🔗 ANALYSE DES RELATIONS CROISÉES")
        print("-" * 50)
        
        # Vérifier les modèles communs
        all_models = apps.get_models()
        
        for model in all_models:
            model_name = model._meta.model_name.lower()
            app_label = model._meta.app_label
            
            # Modèles liés aux membres
            if 'membre' in model_name:
                self.analyze_member_relations(model)
            
            # Modèles liés aux médecins
            if 'medecin' in model_name or 'doctor' in model_name:
                self.analyze_doctor_relations(model)
    
    def analyze_member_relations(self, model):
        """Analyse les relations des modèles membre"""
        print(f"\n   👤 RELATIONS MEMBRE: {model._meta.model_name}")
        
        try:
            count = model.objects.count()
            print(f"   📊 Total: {count}")
            
            if count > 0:
                # Exemple de membre pour analyse
                sample = model.objects.first()
                print(f"   🔍 Exemple: {sample}")
                
                # Vérifier les champs importants
                for field in model._meta.fields:
                    if field.name in ['user', 'medecin', 'assureur']:
                        related_count = model.objects.filter(**{f'{field.name}__isnull': False}).count()
                        print(f"   📎 {field.name}: {related_count} relations")
                        
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    def analyze_doctor_relations(self, model):
        """Analyse les relations des modèles médecin"""
        print(f"\n   🩺 RELATIONS MÉDECIN: {model._meta.model_name}")
        
        try:
            count = model.objects.count()
            print(f"   📊 Total: {count}")
            
            if count > 0:
                sample = model.objects.first()
                print(f"   🔍 Exemple: {sample}")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    def check_migrations_state(self):
        """Vérifie l'état des migrations"""
        print(f"\n🔄 ÉTAT DES MIGRATIONS")
        print("-" * 50)
        
        try:
            # Vérifier les migrations appliquées
            output = StringIO()
            call_command('showmigrations', stdout=output)
            migrations_output = output.getvalue()
            
            apps_to_check = ['membres', 'medecins', 'medecin']
            
            for app_name in apps_to_check:
                app_migrations = [line for line in migrations_output.split('\n') if app_name in line]
                if app_migrations:
                    print(f"📋 Migrations {app_name}:")
                    for migration in app_migrations[:3]:  # Afficher les 3 premières
                        print(f"   {migration.strip()}")
                else:
                    print(f"❌ Aucune migration trouvée pour {app_name}")
                    
        except Exception as e:
            print(f"❌ Erreur vérification migrations: {e}")
    
    def check_database_integrity(self):
        """Vérifie l'intégrité de la base de données"""
        print(f"\n🔒 INTÉGRITÉ DE LA BASE DE DONNÉES")
        print("-" * 50)
        
        with connection.cursor() as cursor:
            # Vérifier les tables
            if 'sqlite' in connection.settings_dict['ENGINE']:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            else:
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            
            tables = [row[0] for row in cursor.fetchall()]
            
            medical_tables = [t for t in tables if any(term in t.lower() for term in ['membre', 'medecin', 'doctor', 'patient', 'soin'])]
            
            print(f"📊 Tables médicales trouvées: {len(medical_tables)}")
            for table in medical_tables:
                # Compter les lignes
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table};")
                    count = cursor.fetchone()[0]
                    print(f"   📁 {table}: {count} ligne(s)")
                except:
                    print(f"   ❌ {table}: erreur comptage")
    
    def generate_recovery_plan(self):
        """Génère un plan de récupération"""
        print(f"\n🚨 PLAN DE RÉCUPÉRATION")
        print("=" * 70)
        
        if not self.problems:
            print("✅ Aucun problème critique détecté")
            return
        
        print("📋 PROBLÈMES IDENTIFIÉS:")
        for i, problem in enumerate(self.problems, 1):
            print(f"   {i}. {problem}")
        
        print("\n💡 SOLUTIONS RECOMMANDÉES:")
        solutions = [
            "1. Vérifier les sauvegardes de base de données",
            "2. Restaurer depuis la dernière sauvegarde valide",
            "3. Recréer les modèles manquants via l'admin Django",
            "4. Réinitialiser les données de test avec manage.py",
            "5. Vérifier les logs Django pour les erreurs récentes",
            "6. Contrôler l'intégrité des relations clés étrangères"
        ]
        
        for solution in solutions:
            print(f"   {solution}")
        
        print("\n🔧 COMMANDES DE RÉCUPÉRATION:")
        recovery_commands = [
            "python manage.py makemigrations membres medecins",
            "python manage.py migrate",
            "python manage.py check --deploy",
            "python manage.py createsuperuser",
            "python manage.py shell -c \"from membres.models import Membre; print(f'Membres: {Membre.objects.count()}')\""
        ]
        
        for cmd in recovery_commands:
            print(f"   $ {cmd}")

def analyze_deleted_data():
    """Analyse spécifique des données supprimées"""
    print("\n🗑️  ANALYSE DES DONNÉES SUPPRIMÉES")
    print("=" * 70)
    
    # Vérifier les tables avec très peu de données (potentiellement vidées)
    with connection.cursor() as cursor:
        if 'sqlite' in connection.settings_dict['ENGINE']:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        else:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        
        tables = [row[0] for row in cursor.fetchall()]
        
        empty_or_small_tables = []
        
        for table in tables:
            if any(term in table.lower() for term in ['membre', 'medecin', 'user', 'patient']):
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                
                if count <= 5:  # Tables avec très peu de données
                    empty_or_small_tables.append((table, count))
        
        if empty_or_small_tables:
            print("⚠️  TABLES POTENTIELLEMENT VIDÉES:")
            for table, count in empty_or_small_tables:
                print(f"   📊 {table}: {count} ligne(s)")
        else:
            print("✅ Aucune table vide détectée")

def main():
    print("🩺🔧 ANALYSE POST-SUPPRESSION - SYSTÈME MÉDICAL")
    print("=" * 70)
    
    analyzer = PostDeleteAnalyzer()
    
    # Analyses principales
    analyzer.analyze_apps()
    analyzer.check_database_integrity()
    
    # Analyse spécifique suppression
    analyze_deleted_data()
    
    # Rapport final
    print(f"\n📊 RAPPORT FINAL")
    print("=" * 70)
    print(f"❌ Problèmes identifiés: {len(analyzer.problems)}")
    print(f"💡 Solutions proposées: {len(analyzer.solutions)}")
    
    if analyzer.problems:
        print("\n🚨 ACTION REQUISE: Des problèmes critiques nécessitent une intervention")
    else:
        print("\n✅ SYSTÈME STABLE: Aucun problème critique détecté")

if __name__ == "__main__":
    main()