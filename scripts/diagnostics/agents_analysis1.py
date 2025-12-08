#!/usr/bin/env python
"""
SCRIPT D'ANALYSE COMPLET - MODULE AGENTS - VERSION CORRIGÉE DES CHEMINS
"""

import os
import sys
import django
from pathlib import Path
import re

# CORRECTION : Chemin de base correct
BASE_DIR = Path(__file__).resolve().parent
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
        # CORRECTION : Chemins relatifs corrects
        self.agents_dir = BASE_DIR / 'agents'
        self.templates_dir = BASE_DIR / 'templates' / 'agents'
        self.issues = []
        self.warnings = []
        self.success = []
        
        print(f"📍 BASE_DIR: {BASE_DIR}")
        print(f"📍 Agents dir: {self.agents_dir}")
        print(f"📍 Templates dir: {self.templates_dir}")

    def analyze_all(self):
        """Lance l'analyse complète"""
        print("=" * 80)
        print("🔍 ANALYSE COMPLÈTE DU MODULE AGENTS - CHEMINS CORRIGÉS")
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
            # Vérifier si les modèles sont accessibles
            models_to_check = [
                'Agent', 'VerificationCotisation', 'ActiviteAgent', 'BonSoin'
            ]
            
            for model_name in models_to_check:
                try:
                    model = apps.get_model('agents', model_name)
                    if model:
                        fields_count = len([f for f in model._meta.get_fields()])
                        self.success.append(f"✅ Modèle {model_name} - OK ({fields_count} champs)")
                        
                        # Vérifier le compte en base
                        try:
                            count = model.objects.count()
                            self.success.append(f"   📊 {model_name}: {count} enregistrements")
                        except Exception as e:
                            self.warnings.append(f"⚠️  {model_name}: Erreur compte - {e}")
                    else:
                        self.issues.append(f"❌ Modèle {model_name} - NON CHARGÉ")
                except LookupError:
                    self.issues.append(f"❌ Modèle {model_name} - NON TROUVÉ")
                    
        except Exception as e:
            self.issues.append(f"❌ Erreur analyse modèles: {e}")

    def analyze_admin(self):
        """Analyse le fichier admin.py"""
        print("\n👨‍💼 ANALYSE ADMIN.PY")
        print("-" * 40)
        
        admin_file = self.agents_dir / 'admin.py'
        
        if not admin_file.exists():
            self.issues.append("❌ Fichier admin.py - MANQUANT")
            return
            
        self.success.append("✅ Fichier admin.py - PRÉSENT")
        
        with open(admin_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
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
                self.warnings.append("⚠️  Aucun modèle enregistré dans admin.py")

    def analyze_views(self):
        """Analyse le fichier views.py"""
        print("\n🎯 ANALYSE DES VUES")
        print("-" * 40)
        
        views_file = self.agents_dir / 'views.py'
        
        if not views_file.exists():
            self.issues.append("❌ Fichier views.py - MANQUANT")
            return
            
        self.success.append("✅ Fichier views.py - PRÉSENT")
        
        with open(views_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Vérifier les vues principales
        views_to_check = [
            ('def dashboard', 'Vue dashboard'),
            ('def verification_cotisations', 'Vue vérification cotisations'),
            ('def creer_bon_soin', 'Vue création bon soin'),
            ('def recherche_membres_api', 'API recherche membres'),
            ('def verifier_cotisation_api', 'API vérification cotisation'),
            ('def creer_bon_soin_membre', 'Vue création bon soin membre'),
            ('def confirmation_bon_soin', 'Vue confirmation bon soin'),
            ('def historique_bons', 'Vue historique bons'),
            ('def rapport_performance', 'Vue rapport performance'),
        ]
        
        for pattern, description in views_to_check:
            if pattern in content:
                self.success.append(f"✅ {description} - PRÉSENT")
            else:
                self.warnings.append(f"⚠️  {description} - MANQUANT")

    def analyze_urls(self):
        """Analyse le fichier urls.py"""
        print("\n🌐 ANALYSE DES URLs")
        print("-" * 40)
        
        urls_file = self.agents_dir / 'urls.py'
        
        if not urls_file.exists():
            self.issues.append("❌ Fichier urls.py - MANQUANT")
            return
            
        self.success.append("✅ Fichier urls.py - PRÉSENT")
        
        with open(urls_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Vérifier les URLs principales
        urls_to_check = [
            ('dashboard', 'URL dashboard'),
            ('verification-cotisations', 'URL vérification cotisations'),
            ('creer-bon-soin', 'URL création bon soin'),
            ('api/recherche-membres', 'API recherche membres'),
            ('api/verifier-cotisation', 'API vérification cotisation'),
            ('historique-bons', 'URL historique bons'),
            ('rapport-performance', 'URL rapport performance'),
        ]
        
        for pattern, description in urls_to_check:
            if pattern in content:
                self.success.append(f"✅ {description} - PRÉSENT")
            else:
                self.warnings.append(f"⚠️  {description} - MANQUANT")

    def analyze_templates(self):
        """Analyse les templates"""
        print("\n📄 ANALYSE DES TEMPLATES")
        print("-" * 40)
        
        if not self.templates_dir.exists():
            self.issues.append(f"❌ Dossier templates/agents - MANQUANT: {self.templates_dir}")
            return
            
        self.success.append("✅ Dossier templates/agents - PRÉSENT")
        
        # Templates requis
        required_templates = [
            'dashboard.html',
            'verification_cotisations.html', 
            'creer_bon_soin.html',
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

    def analyze_consistency(self):
        """Analyse la cohérence entre les composants"""
        print("\n🔗 ANALYSE DE COHÉRENCE")
        print("-" * 40)
        
        # Vérifier si les URLs correspondent aux vues
        try:
            from agents import urls as agents_urls
            from agents import views
            
            # Vérifier que les vues référencées dans les URLs existent
            urls_file = self.agents_dir / 'urls.py'
            with open(urls_file, 'r') as f:
                urls_content = f.read()
                
            # Extraire les noms de vues des URLs
            view_patterns = re.findall(r'views\.(\w+)', urls_content)
            for view_name in set(view_patterns):
                if hasattr(views, view_name):
                    self.success.append(f"✅ Vue {view_name} référencée dans les URLs")
                else:
                    self.issues.append(f"❌ Vue {view_name} référencée mais non trouvée")
                    
        except Exception as e:
            self.warnings.append(f"⚠️  Impossible d'analyser la cohérence: {e}")

    def generate_report(self):
        """Génère le rapport final"""
        print("\n" + "=" * 80)
        print("📋 RAPPORT FINAL D'ANALYSE - CHEMINS CORRIGÉS")
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
        
        # Afficher les succès (premiers 10)
        if self.success:
            print(f"\n✅ SUCCÈS (premiers {min(10, len(self.success))}):")
            for success in self.success[:10]:
                print(f"   {success}")
            if len(self.success) > 10:
                print(f"   ... et {len(self.success) - 10} autres succès")

def main():
    """Fonction principale"""
    analyzer = AgentsAnalyzer()
    analyzer.analyze_all()

if __name__ == '__main__':
    main()