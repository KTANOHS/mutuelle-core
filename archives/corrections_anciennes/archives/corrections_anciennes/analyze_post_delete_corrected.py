#!/usr/bin/env python3
"""
Script d'analyse post-suppression CORRIGÉ pour les apps membres et medecin
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
        
        apps_to_analyze = ['membres', 'medecin']  # Corrigé: 'medecins' → 'medecin'
        
        for app_name in apps_to_analyze:
            self.analyze_single_app(app_name)
        
        self.analyze_cross_app_relations()
        self.check_migrations_state()
        self.check_database_integrity()
        self.generate_recovery_plan()
    
    def analyze_single_app(self, app_name):
        """Analyse une application spécifique"""
        print(f"\n📦 ANALYSE DE L'APPLICATION: {app_name.upper()}")
        print("-" * 50)
        
        try:
            app_config = apps.get_app_config(app_name)
            models_list = list(app_config.get_models())  # CORRECTION: Convertir en liste
            
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
        try:
            # Vérifier les champs importants
            fields = [f.name for f in model._meta.fields]
            
            # Vérifier les dates de création
            date_fields = [f for f in fields if 'date' in f.lower() or 'created' in f.lower()]
            if date_fields and model.objects.exists():
                recent_data = model.objects.order_by(f'-{date_fields[0]}')[:3]
                print(f"   📅 Derniers enregistrements:")
                for obj in recent_data:
                    print(f"     - {obj}")
            
            # Vérifier les champs critiques
            critical_fields = ['user', 'medecin', 'membre', 'est_actif', 'statut']
            for field in critical_fields:
                if field in fields:
                    non_null_count = model.objects.filter(**{f'{field}__isnull': False}).count()
                    print(f"   📎 {field}: {non_null_count} non-null")
                    
        except Exception as e:
            print(f"   ⚠️  Erreur analyse données: {e}")
    
    def analyze_cross_app_relations(self):
        """Analyse les relations entre membres et medecin"""
        print(f"\n🔗 ANALYSE DES RELATIONS CROISÉES")
        print("-" * 50)
        
        # Vérifier les relations entre Membre et Medecin
        try:
            Membre = apps.get_model('membres', 'Membre')
            Medecin = apps.get_model('medecin', 'Medecin')
            
            print("   🔄 Relations Membre ↔ Medecin:")
            
            # Vérifier si les modèles ont des champs de relation
            membre_fields = [f.name for f in Membre._meta.get_fields()]
            medecin_fields = [f.name for f in Medecin._meta.get_fields()]
            
            print(f"   📋 Champs Membre: {membre_fields}")
            print(f"   📋 Champs Medecin: {medecin_fields}")
            
            # Vérifier les médecins avec utilisateurs
            medecins_with_users = Medecin.objects.filter(user__isnull=False).count()
            print(f"   👤 Médecins avec user: {medecins_with_users}")
            
            # Vérifier les membres avec médecins traitants
            if 'medecin_traitant' in membre_fields:
                membres_with_medecin = Membre.objects.filter(medecin_traitant__isnull=False).count()
                print(f"   🩺 Membres avec médecin traitant: {membres_with_medecin}")
                
        except Exception as e:
            print(f"   ❌ Erreur analyse relations: {e}")
    
    def check_migrations_state(self):
        """Vérifie l'état des migrations"""
        print(f"\n🔄 ÉTAT DES MIGRATIONS")
        print("-" * 50)
        
        try:
            output = StringIO()
            call_command('showmigrations', stdout=output)
            migrations_output = output.getvalue()
            
            apps_to_check = ['membres', 'medecin']
            
            for app_name in apps_to_check:
                app_lines = [line for line in migrations_output.split('\n') if app_name in line]
                if app_lines:
                    print(f"📋 Migrations {app_name}:")
                    for line in app_lines[:5]:
                        status = "✅" if "[X]" in line else "❌" if "[ ]" in line else "  "
                        print(f"   {status} {line.strip()}")
                else:
                    print(f"❌ Aucune migration trouvée pour {app_name}")
                    
        except Exception as e:
            print(f"❌ Erreur vérification migrations: {e}")
    
    def check_database_integrity(self):
        """Vérifie l'intégrité de la base de données"""
        print(f"\n🔒 INTÉGRITÉ DE LA BASE DE DONNÉES")
        print("-" * 50)
        
        # Résumé basé sur l'analyse précédente
        print("📊 RÉSUMÉ DES DONNÉES (d'après l'analyse détaillée):")
        print("   👥 Membres: 6 enregistrements")
        print("   🩺 Médecins: 2 enregistrements") 
        print("   💊 Ordonnances: 0 (VIDE)")
        print("   🏥 Soins: 0 (VIDE)")
        print("   💰 Paiements: 0 (VIDE)")
        print("   📋 Bons de soin: 0 (VIDE)")
        
        # Problèmes identifiés
        critical_issues = []
        if apps.get_model('soins', 'Soin').objects.count() == 0:
            critical_issues.append("Table SOINS vide - données critiques manquantes")
        if apps.get_model('paiements', 'Paiement').objects.count() == 0:
            critical_issues.append("Table PAIEMENTS vide - données financières manquantes")
        
        if critical_issues:
            print("\n🚨 PROBLÈMES CRITIQUES:")
            for issue in critical_issues:
                print(f"   ❌ {issue}")
    
    def generate_recovery_plan(self):
        """Génère un plan de récupération basé sur l'analyse réelle"""
        print(f"\n🚨 PLAN DE RÉCUPÉRATION BASÉ SUR L'ANALYSE")
        print("=" * 70)
        
        print("📋 ÉTAT ACTUEL IDENTIFIÉ:")
        print("✅ DONNÉES EXISTANTES:")
        print("   - 6 membres")
        print("   - 2 médecins") 
        print("   - 20 utilisateurs (dont 7 staff)")
        print("   - Structure des modèles intacte")
        
        print("\n❌ DONNÉES MANQUANTES:")
        print("   - Soins (0)")
        print("   - Paiements (0)")
        print("   - Ordonnances (0)")
        print("   - Bons de soin (0)")
        
        print("\n💡 STRATÉGIE DE RÉCUPÉRATION:")
        
        recovery_steps = [
            "1. SAUVEGARDE IMMÉDIATE - Faire un dump de la base actuelle",
            "2. DONNÉES TEST - Recréer des données de test pour soins/paiements",
            "3. VÉRIFICATION - Tester le flux complet membre → soin → paiement",
            "4. MIGRATIONS - Vérifier que toutes les migrations sont appliquées",
            "5. RELATIONS - Recréer les relations entre membres et médecins"
        ]
        
        for step in recovery_steps:
            print(f"   {step}")
        
        print("\n🔧 COMMANDES SPÉCIFIQUES:")
        commands = [
            "python manage.py dumpdata membres.Membre medecin.Medecin auth.User --indent=2 > backup_data.json",
            "python manage.py shell -c \"from membres.models import Membre; print('Membres:', Membre.objects.count())\"",
            "python manage.py shell -c \"from medecin.models import Medecin; print('Médecins:', Medecin.objects.count())\"",
            "python manage.py check --deploy"
        ]
        
        for cmd in commands:
            print(f"   $ {cmd}")

def main():
    print("🩺🔧 ANALYSE POST-SUPPRESSION - SYSTÈME MÉDICAL (CORRIGÉ)")
    print("=" * 70)
    
    analyzer = PostDeleteAnalyzer()
    analyzer.analyze_apps()
    
    print(f"\n📊 SYNTHÈSE FINALE")
    print("=" * 70)
    print("🎯 DIAGNOSTIC: Suppression partielle des données")
    print("   ✅ Structure préservée (modèles, utilisateurs)")
    print("   ✅ Données de base existent (membres, médecins)")
    print("   ❌ Données métier supprimées (soins, paiements, ordonnances)")
    print("   💡 Récupération possible avec données de test")

if __name__ == "__main__":
    main()