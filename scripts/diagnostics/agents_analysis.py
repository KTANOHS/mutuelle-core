#!/usr/bin/env python
"""
SCRIPT D'ANALYSE COMPLET - MODULE AGENTS
Analyse tous les composants du module agents pour détecter les problèmes
"""

import os
import sys
import django
from pathlib import Path
import re

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    from django.apps import apps
    from django.urls import get_resolver
except ImportError as e:
    print(f"❌ Erreur import Django: {e}")
    sys.exit(1)

class AgentsAnalyzer:
    def __init__(self):
        self.agents_dir = BASE_DIR / 'agents'
        self.templates_dir = BASE_DIR / 'templates' / 'agents'
        self.issues = []
        self.warnings = []
        self.success = []

    def analyze_all(self):
        """Lance l'analyse complète"""
        print("=" * 80)
        print("🔍 ANALYSE COMPLÈTE DU MODULE AGENTS")
        print("=" * 80)
        
        self.analyze_models()
        self.analyze_admin()
        self.analyze_views()
        self.analyze_urls()
        self.analyze_templates()
        self.analyze_consistency()
        
        self.generate_report()

    def analyze_models(self):
        """Analyse les modèles"""
        print("\n📊 ANALYSE DES MODÈLES")
        print("-" * 40)
        
        try:
            from agents.models import Agent, VerificationCotisation, ActiviteAgent, BonSoin
            
            models_to_check = [
                'Agent', 'VerificationCotisation', 'ActiviteAgent', 'BonSoin'
            ]
            
            for model_name in models_to_check:
                try:
                    model = apps.get_model('agents', model_name)
                    if model:
                        self.success.append(f"✅ Modèle {model_name} - OK")
                        # Vérifier les champs
                        fields = [f.name for f in model._meta.get_fields()]
                        print(f"   📋 Champs {model_name}: {len(fields)} champs")
                except LookupError:
                    self.issues.append(f"❌ Modèle {model_name} - NON TROUVÉ")
                    
        except ImportError as e:
            self.issues.append(f"❌ Erreur import modèles: {e}")

    def analyze_admin(self):
        """Analyse le fichier admin.py"""
        print("\n👨‍💼 ANALYSE ADMIN.PY")
        print("-" * 40)
        
        admin_file = self.agents_dir / 'admin.py'
        
        if not admin_file.exists():
            self.issues.append("❌ Fichier admin.py - MANQUANT")
            return
            
        with open(admin_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Vérifier les imports
        imports_to_check = [
            'from .models import',
            'from django.contrib import admin',
            '@admin.register'
        ]
        
        for import_check in imports_to_check:
            if import_check in content:
                self.success.append(f"✅ Import {import_check.split()[-1]} - OK")
            else:
                self.warnings.append(f"⚠️  Import manquant: {import_check}")
                
        # Vérifier les modèles enregistrés
        models_in_admin = re.findall(r'@admin\.register\((\w+)\)', content)
        if models_in_admin:
            for model in models_in_admin:
                self.success.append(f"✅ Modèle {model} enregistré dans admin")
        else:
            # Vérifier l'ancienne méthode
            models_old = re.findall(r'admin\.site\.register\((\w+)', content)
            if models_old:
                for model in models_old:
                    self.success.append(f"✅ Modèle {model} enregistré (ancienne méthode)")
            else:
                self.issues.append("❌ Aucun modèle enregistré dans admin.py")

    def analyze_views(self):
        """Analyse le fichier views.py"""
        print("\n🎯 ANALYSE DES VUES")
        print("-" * 40)
        
        views_file = self.agents_dir / 'views.py'
        
        if not views_file.exists():
            self.issues.append("❌ Fichier views.py - MANQUANT")
            return
            
        with open(views_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Vérifier les décorateurs et fonctions principales
        views_to_check = [
            ('@login_required', 'Décorateur login_required'),
            ('@gerer_erreurs', 'Décorateur gestion erreurs'),
            ('def dashboard', 'Vue dashboard'),
            ('def verification_cotisations', 'Vue vérification cotisations'),
            ('def creer_bon_soin', 'Vue création bon soin'),
            ('def recherche_membres_api', 'API recherche membres'),
            ('def verifier_cotisation_api', 'API vérification cotisation'),
        ]
        
        for pattern, description in views_to_check:
            if pattern in content:
                self.success.append(f"✅ {description} - PRÉSENT")
            else:
                self.issues.append(f"❌ {description} - MANQUANT")
                
        # Vérifier les imports critiques
        critical_imports = [
            'from django.shortcuts import render',
            'from django.http import JsonResponse',
            'from django.contrib.auth.decorators import login_required',
        ]
        
        for import_stmt in critical_imports:
            if import_stmt in content:
                self.success.append(f"✅ Import: {import_stmt.split()[-1]}")
            else:
                self.warnings.append(f"⚠️  Import manquant: {import_stmt}")

    def analyze_urls(self):
        """Analyse le fichier urls.py"""
        print("\n🌐 ANALYSE DES URLs")
        print("-" * 40)
        
        urls_file = self.agents_dir / 'urls.py'
        
        if not urls_file.exists():
            self.issues.append("❌ Fichier urls.py - MANQUANT")
            return
            
        with open(urls_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Vérifier la structure de base
        url_patterns = [
            ('app_name = \'agents\'', 'Namespace agents'),
            ('path\(''', 'Définition des paths'),
            ('dashboard', 'URL dashboard'),
            ('verification-cotisations', 'URL vérification cotisations'),
            ('creer-bon-soin', 'URL création bon soin'),
            ('api/recherche-membres', 'API recherche membres'),
        ]
        
        for pattern, description in url_patterns:
            if pattern in content:
                self.success.append(f"✅ {description} - PRÉSENT")
            else:
                self.issues.append(f"❌ {description} - MANQUANT")
                
        # Extraire toutes les URLs définies
        url_patterns = re.findall(r'path\(\s*[\'"]([^\'"]+)[\'"]', content)
        if url_patterns:
            print(f"   📍 URLs définies: {', '.join(url_patterns)}")

    def analyze_templates(self):
        """Analyse les templates"""
        print("\n📄 ANALYSE DES TEMPLATES")
        print("-" * 40)
        
        if not self.templates_dir.exists():
            self.issues.append("❌ Dossier templates/agents - MANQUANT")
            return
            
        # Templates requis
        required_templates = [
            'dashboard.html',
            'verification_cotisations.html', 
            'creer_bon_soin.html',
            'creer_bon_soin_membre.html',
            'confirmation_bon_soin.html',
            'historique_bons.html',
            'rapport_performance.html',
            'liste_membres.html',
            'creer_membre.html',
            'error.html'
        ]
        
        existing_templates = list(self.templates_dir.glob('*.html'))
        existing_names = [t.name for t in existing_templates]
        
        for template in required_templates:
            if template in existing_names:
                self.success.append(f"✅ Template {template} - PRÉSENT")
            else:
                self.issues.append(f"❌ Template {template} - MANQUANT")
                
        # Templates supplémentaires trouvés
        extra_templates = set(existing_names) - set(required_templates)
        if extra_templates:
            print(f"   📂 Templates supplémentaires: {', '.join(extra_templates)}")

    def analyze_consistency(self):
        """Analyse la cohérence entre les composants"""
        print("\n🔗 ANALYSE DE COHÉRENCE")
        print("-" * 40)
        
        # Vérifier la cohérence entre vues et URLs
        try:
            from agents import urls as agents_urls
            resolver = get_resolver(agents_urls)
            
            url_patterns = []
            for pattern in resolver.url_patterns:
                if hasattr(pattern, 'pattern'):
                    url_patterns.append(str(pattern.pattern))
                    
            print(f"   🔗 URLs chargées: {len(url_patterns)} patterns")
            
        except Exception as e:
            self.warnings.append(f"⚠️  Impossible d'analyser les URLs: {e}")

    def generate_report(self):
        """Génère le rapport final"""
        print("\n" + "=" * 80)
        print("📋 RAPPORT FINAL D'ANALYSE")
        print("=" * 80)
        
        # Résumé statistique
        total_checks = len(self.success) + len(self.issues) + len(self.warnings)
        success_rate = (len(self.success) / total_checks) * 100 if total_checks > 0 else 0
        
        print(f"📊 STATISTIQUES:")
        print(f"   ✅ Succès: {len(self.success)}")
        print(f"   ❌ Problèmes: {len(self.issues)}") 
        print(f"   ⚠️  Avertissements: {len(self.warnings)}")
        print(f"   📈 Taux de succès: {success_rate:.1f}%")
        
        # Afficher les problèmes critiques
        if self.issues:
            print(f"\n🚨 PROBLÈMES CRITIQUES ({len(self.issues)}):")
            for issue in self.issues:
                print(f"   {issue}")
                
        # Afficher les avertissements
        if self.warnings:
            print(f"\n⚠️  AVERTISSEMENTS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   {warning}")
                
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        if not self.issues:
            print("   🎉 Excellent! Le module agents semble bien configuré.")
        else:
            if any("MANQUANT" in issue for issue in self.issues):
                print("   🔧 Fichiers manquants à créer")
            if any("Modèle" in issue for issue in self.issues):
                print("   🗃️  Vérifier la configuration des modèles")
            if any("Template" in issue for issue in self.issues):
                print("   📄 Templates manquants à créer")
                
        print(f"\n📋 PROCHAINES ÉTAPES:")
        steps = [
            "1. Résoudre les problèmes critiques d'abord",
            "2. Traiter les avertissements ensuite", 
            "3. Tester les fonctionnalités principales",
            "4. Vérifier les permissions d'accès",
            "5. Tester les APIs"
        ]
        for step in steps:
            print(f"   {step}")

def main():
    """Fonction principale"""
    analyzer = AgentsAnalyzer()
    analyzer.analyze_all()

if __name__ == '__main__':
    main()