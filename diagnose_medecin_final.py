#!/usr/bin/env python3
"""
Script de diagnostic et correction FINAL pour medecin
Les templates existent, mais il y a des problèmes de vues et de configuration
"""

import os
import django
import sys
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse, NoReverseMatch
from django.template.loader import get_template
from django.core.management import call_command
from io import StringIO

class MedecinFinalFixer:
    def __init__(self):
        self.base_dir = BASE_DIR
        self.problems = []
        self.solutions = []
    
    def diagnose_real_issues(self):
        """Diagnostique les vrais problèmes"""
        print("🔍 DIAGNOSTIC DES PROBLÈMES RÉELS MEDECIN")
        print("=" * 70)
        
        self.check_template_errors()
        self.check_missing_views()
        self.check_urls_configuration()
        self.check_template_inheritance()
        self.test_medecin_access()
        
    def check_template_errors(self):
        """Vérifie les erreurs dans les templates existants"""
        print("\n📄 VÉRIFICATION DES TEMPLATES EXISTANTS")
        print("-" * 40)
        
        template_dir = self.base_dir / 'templates' / 'medecin'
        
        if template_dir.exists():
            html_files = list(template_dir.glob('*.html'))
            print(f"✅ {len(html_files)} templates trouvés")
            
            # Vérifier les templates problématiques
            problematic_templates = []
            
            for html_file in html_files:
                try:
                    # Essayer de charger le template
                    template_name = f'medecin/{html_file.name}'
                    template = get_template(template_name)
                    print(f"   ✅ {html_file.name} - VALIDE")
                except Exception as e:
                    error_msg = str(e)
                    print(f"   ❌ {html_file.name} - ERREUR: {error_msg}")
                    problematic_templates.append((html_file.name, error_msg))
                    
                    # Analyser l'erreur
                    if 'base.html' in error_msg:
                        self.problems.append(f"Template {html_file.name} utilise un template base incorrect")
                        self.solutions.append(f"Corriger l'extends dans {html_file.name}")
                    elif 'medecin/base' in error_msg:
                        self.problems.append(f"Template {html_file.name} ne trouve pas base_medecin.html")
                        self.solutions.append(f"Vérifier que base_medecin.html existe et est accessible")
            
            return problematic_templates
        else:
            print("❌ Dossier templates/medecin non trouvé")
            return []
    
    def check_missing_views(self):
        """Vérifie les vues manquantes"""
        print(f"\n👁️  VÉRIFICATION DES VUES MANQUANTES")
        print("-" * 40)
        
        views_file = self.base_dir / 'medecin' / 'views.py'
        
        if not views_file.exists():
            print("❌ Fichier medecin/views.py non trouvé")
            return
        
        with open(views_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vues importantes à vérifier
        important_views = [
            ('dashboard', 'Vue dashboard principale'),
            ('mes_ordonnances', 'Vue des ordonnances du médecin'),
            ('liste_ordonnances', 'Vue liste des ordonnances'),
            ('creer_ordonnance', 'Vue création ordonnance'),
            ('liste_bons', 'Vue liste des bons'),
        ]
        
        missing_views = []
        for view_name, description in important_views:
            if f'def {view_name}(' not in content:
                print(f"   ❌ {view_name} - MANQUANT")
                missing_views.append((view_name, description))
                self.problems.append(f"Vue manquante: {view_name}")
                self.solutions.append(f"Ajouter la vue {view_name} dans medecin/views.py")
            else:
                print(f"   ✅ {view_name} - PRÉSENTE")
        
        return missing_views
    
    def check_urls_configuration(self):
        """Vérifie la configuration des URLs"""
        print(f"\n🌐 VÉRIFICATION CONFIGURATION URLs")
        print("-" * 40)
        
        try:
            import medecin.urls
            url_count = len(medecin.urls.urlpatterns)
            print(f"✅ {url_count} patterns URL configurés")
            
            # URLs importantes
            important_urls = [
                ('dashboard', 'Dashboard'),
                ('liste_ordonnances', 'Liste ordonnances'),
                ('creer_ordonnance', 'Créer ordonnance'),
                ('liste_bons', 'Liste bons'),
                ('mes_ordonnances', 'Mes ordonnances'),
            ]
            
            for url_name, description in important_urls:
                try:
                    url = reverse(f'medecin:{url_name}')
                    print(f"   ✅ {description}: {url}")
                except NoReverseMatch:
                    print(f"   ❌ {description}: URL non configurée")
                    self.problems.append(f"URL non configurée: {description}")
                    self.solutions.append(f"Ajouter l'URL {url_name} dans medecin/urls.py")
                    
        except ImportError as e:
            print(f"❌ Erreur import URLs: {e}")
            self.problems.append("Fichier medecin/urls.py manquant ou invalide")
    
    def check_template_inheritance(self):
        """Vérifie l'héritage des templates"""
        print(f"\n🔄 VÉRIFICATION HÉRITAGE TEMPLATES")
        print("-" * 40)
        
        template_dir = self.base_dir / 'templates' / 'medecin'
        
        # Vérifier base_medecin.html
        base_template = template_dir / 'base_medecin.html'
        if base_template.exists():
            print("✅ base_medecin.html existe")
            
            # Vérifier le contenu de base_medecin.html
            with open(base_template, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '{% block content %}' in content:
                print("   ✅ Contient block content")
            else:
                print("   ❌ Ne contient pas block content")
                self.problems.append("base_medecin.html ne contient pas block content")
            
            if '{% block title %}' in content:
                print("   ✅ Contient block title")
            else:
                print("   ❌ Ne contient pas block title")
        
        else:
            print("❌ base_medecin.html manquant")
            self.problems.append("Template base_medecin.html manquant")
        
        # Vérifier l'héritage dans les autres templates
        templates_to_check = ['dashboard.html', 'mes_ordonnances.html', 'liste_ordonnances.html']
        
        for template_name in templates_to_check:
            template_path = template_dir / template_name
            if template_path.exists():
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if '{% extends' in content:
                    extends_line = [line for line in content.split('\n') if '{% extends' in line][0]
                    print(f"   ✅ {template_name} extends: {extends_line.strip()}")
                else:
                    print(f"   ❌ {template_name} n'extend pas de template base")
                    self.problems.append(f"{template_name} n'extend pas de template base")
    
    def test_medecin_access(self):
        """Teste l'accès aux pages medecin"""
        print(f"\n🧪 TEST D'ACCÈS MÉDECIN")
        print("-" * 40)
        
        client = Client()
        User = get_user_model()
        
        # Trouver un médecin
        try:
            from medecin.models import Medecin
            medecin = Medecin.objects.first()
            if not medecin:
                print("❌ Aucun médecin trouvé en base")
                self.problems.append("Aucun médecin en base de données")
                return
            
            medecin_user = medecin.user
            print(f"👤 Médecin test: {medecin_user.get_full_name()}")
            
            # Connecter le médecin
            client.force_login(medecin_user)
            
            # URLs à tester
            test_urls = [
                ('medecin:dashboard', 'Dashboard'),
                ('medecin:liste_ordonnances', 'Liste ordonnances'),
                ('medecin:creer_ordonnance', 'Créer ordonnance'),
                ('medecin:liste_bons', 'Liste bons'),
            ]
            
            for url_name, description in test_urls:
                try:
                    url = reverse(url_name)
                    response = client.get(url)
                    
                    if response.status_code == 200:
                        print(f"   ✅ {description}: 200 OK")
                    elif response.status_code == 404:
                        print(f"   ❌ {description}: 404 NOT FOUND")
                        self.problems.append(f"Page 404: {description}")
                    elif response.status_code == 500:
                        print(f"   ❌ {description}: 500 SERVER ERROR")
                        # Essayer d'extraire l'erreur
                        error_content = str(response.content)[:300]
                        if 'TemplateDoesNotExist' in error_content:
                            self.problems.append(f"Template manquant pour {description}")
                        elif 'NameError' in error_content or 'AttributeError' in error_content:
                            self.problems.append(f"Erreur Python dans la vue {description}")
                        else:
                            self.problems.append(f"Erreur serveur pour {description}")
                    else:
                        print(f"   ⚠️  {description}: {response.status_code}")
                        
                except NoReverseMatch:
                    print(f"   ❌ {description}: URL non configurée")
                    self.problems.append(f"URL non configurée: {description}")
                except Exception as e:
                    print(f"   ❌ {description}: Erreur - {e}")
                    self.problems.append(f"Erreur test {description}: {e}")
                    
        except Exception as e:
            print(f"❌ Erreur test accès: {e}")
            self.problems.append(f"Erreur test accès: {e}")
    
    def generate_fix_plan(self):
        """Génère un plan de correction"""
        print(f"\n🔧 PLAN DE CORRECTION")
        print("=" * 70)
        
        if not self.problems:
            print("✅ Aucun problème détecté - L'application medecin devrait fonctionner")
            return
        
        print("📋 PROBLÈMES IDENTIFIÉS:")
        for i, problem in enumerate(self.problems, 1):
            print(f"   {i}. {problem}")
        
        print(f"\n💡 SOLUTIONS:")
        for i, solution in enumerate(self.solutions, 1):
            print(f"   {i}. {solution}")
        
        # Solutions spécifiques
        print(f"\n🎯 ACTIONS IMMÉDIATES:")
        
        if any("Vue manquante" in problem for problem in self.problems):
            print("   1. Créer les vues manquantes dans medecin/views.py")
        
        if any("TemplateDoesNotExist" in problem for problem in self.problems):
            print("   2. Vérifier que tous les templates référencés existent")
        
        if any("URL non configurée" in problem for problem in self.problems):
            print("   3. Ajouter les URLs manquantes dans medecin/urls.py")
        
        print("   4. Redémarrer le serveur Django")
        print("   5. Tester: http://127.0.0.1:8000/medecin/dashboard/")

def main():
    print("🩺 CORRECTEUR FINAL MEDECIN - TEMPLATES EXISTANTS")
    print("=" * 70)
    
    fixer = MedecinFinalFixer()
    fixer.diagnose_real_issues()
    fixer.generate_fix_plan()
    
    print(f"\n📊 RAPPORT FINAL:")
    print(f"Problèmes identifiés: {len(fixer.problems)}")
    print(f"Solutions proposées: {len(fixer.solutions)}")
    
    if fixer.problems:
        print("\n🚨 ACTION REQUISE: Des correctifs sont nécessaires")
    else:
        print("\n✅ SYSTÈME PRÊT: Aucun correctif nécessaire")

if __name__ == "__main__":
    main()