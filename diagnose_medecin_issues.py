#!/usr/bin/env python3
"""
Script de diagnostic des problèmes medecin - Les templates existent déjà
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

class MedecinProblemDiagnoser:
    def __init__(self):
        self.base_dir = BASE_DIR
        self.problems = []
        self.solutions = []
    
    def check_templates_exist(self):
        """Vérifie que les templates existent réellement"""
        print("📁 VÉRIFICATION DES TEMPLATES EXISTANTS")
        print("-" * 40)
        
        template_dir = self.base_dir / 'templates' / 'medecin'
        if template_dir.exists():
            html_files = list(template_dir.glob('*.html'))
            print(f"✅ Dossier templates/medecin trouvé avec {len(html_files)} fichiers HTML")
            
            # Templates importants
            important_templates = [
                'dashboard.html', 'base_medecin.html', 'mes_ordonnances.html',
                'creer_ordonnance.html', 'liste_ordonnances.html'
            ]
            
            for template in important_templates:
                template_path = template_dir / template
                if template_path.exists():
                    print(f"   ✅ {template}")
                else:
                    print(f"   ❌ {template} - MANQUANT")
                    self.problems.append(f"Template manquant: {template}")
        else:
            print("❌ Dossier templates/medecin non trouvé")
            self.problems.append("Dossier templates/medecin manquant")
    
    def check_template_resolution(self):
        """Vérifie si Django peut résoudre les templates"""
        print(f"\n🔍 RÉSOLUTION DES TEMPLATES PAR DJANGO")
        print("-" * 40)
        
        templates_to_check = [
            'medecin/dashboard.html',
            'medecin/base_medecin.html',
            'medecin/mes_ordonnances.html',
        ]
        
        for template_name in templates_to_check:
            try:
                template = get_template(template_name)
                print(f"   ✅ {template_name} - RÉSOLU")
                # Vérifier l'origine du template
                for loader in template.template.loader_list:
                    try:
                        source, display_name = loader.load_template_source(template_name)
                        print(f"      📍 Chargé depuis: {display_name}")
                        break
                    except:
                        continue
            except Exception as e:
                print(f"   ❌ {template_name} - ERREUR: {e}")
                self.problems.append(f"Template non résolu: {template_name}")
    
    def check_urls_access(self):
        """Vérifie l'accès aux URLs medecin"""
        print(f"\n🌐 TEST D'ACCÈS AUX URLs MEDECIN")
        print("-" * 40)
        
        client = Client()
        User = get_user_model()
        
        # Trouver un utilisateur médecin
        try:
            from medecin.models import Medecin
            medecin_obj = Medecin.objects.first()
            if medecin_obj:
                medecin_user = medecin_obj.user
                print(f"👤 Médecin trouvé: {medecin_user.get_full_name()}")
            else:
                print("❌ Aucun médecin dans la base de données")
                self.problems.append("Aucun médecin en base")
                return
        except Exception as e:
            print(f"❌ Erreur recherche médecin: {e}")
            self.problems.append("Erreur accès modèle Medecin")
            return
        
        # URLs à tester
        test_urls = [
            ('medecin:dashboard', 'Dashboard'),
            ('medecin:liste_ordonnances', 'Liste ordonnances'),
            ('medecin:creer_ordonnance', 'Créer ordonnance'),
            ('medecin:liste_bons', 'Liste bons'),
        ]
        
        # Connecter le médecin
        client.force_login(medecin_user)
        
        for url_name, description in test_urls:
            try:
                url = reverse(url_name)
                response = client.get(url)
                
                if response.status_code == 200:
                    print(f"   ✅ {description}: 200 OK")
                elif response.status_code == 404:
                    print(f"   ❌ {description}: 404 NOT FOUND")
                    self.problems.append(f"URL 404: {description}")
                elif response.status_code == 403:
                    print(f"   ❌ {description}: 403 FORBIDDEN")
                    self.problems.append(f"Accès refusé: {description}")
                elif response.status_code == 500:
                    print(f"   ❌ {description}: 500 SERVER ERROR")
                    # Essayer de récupérer l'erreur
                    try:
                        error_content = str(response.content)[:200]
                        print(f"      Erreur: {error_content}...")
                    except:
                        pass
                    self.problems.append(f"Erreur serveur: {description}")
                else:
                    print(f"   ⚠️  {description}: {response.status_code}")
                    
            except NoReverseMatch:
                print(f"   ❌ {description}: URL NON CONFIGURÉE")
                self.problems.append(f"URL non configurée: {description}")
            except Exception as e:
                print(f"   ❌ {description}: ERREUR - {e}")
                self.problems.append(f"Erreur URL {description}: {e}")
    
    def check_medecin_views(self):
        """Vérifie les vues medecin"""
        print(f"\n👁️  VÉRIFICATION DES VUES MEDECIN")
        print("-" * 40)
        
        try:
            import medecin.views as views
            
            # Vérifier les vues importantes
            important_views = ['dashboard', 'mes_ordonnances', 'creer_ordonnance']
            
            for view_name in important_views:
                if hasattr(views, view_name):
                    view_func = getattr(views, view_name)
                    print(f"   ✅ Vue '{view_name}' trouvée")
                    
                    # Vérifier si c'est une fonction ou une classe
                    if callable(view_func):
                        print(f"      Type: {type(view_func).__name__}")
                    else:
                        print(f"      ⚠️  Non appelable")
                else:
                    print(f"   ❌ Vue '{view_name}' manquante")
                    self.problems.append(f"Vue manquante: {view_name}")
                    
        except ImportError as e:
            print(f"❌ Impossible d'importer medecin.views: {e}")
            self.problems.append("Impossible d'importer les vues medecin")
    
    def check_authentication(self):
        """Vérifie le système d'authentification"""
        print(f"\n🔐 VÉRIFICATION AUTHENTIFICATION")
        print("-" * 40)
        
        try:
            from medecin.models import Medecin
            
            medecin_count = Medecin.objects.count()
            print(f"📊 Médecins en base: {medecin_count}")
            
            if medecin_count > 0:
                for medecin in Medecin.objects.all()[:3]:
                    status = "✅" if medecin.user.is_active else "❌"
                    print(f"   {status} {medecin.user.get_full_name()} - Actif: {medecin.user.is_active}")
            else:
                print("   ⚠️  Aucun médecin en base de données")
                self.problems.append("Aucun médecin en base")
                
        except Exception as e:
            print(f"❌ Erreur vérification authentification: {e}")
            self.problems.append(f"Erreur modèle Medecin: {e}")
    
    def check_migrations(self):
        """Vérifie l'état des migrations"""
        print(f"\n🔄 ÉTAT DES MIGRATIONS MEDECIN")
        print("-" * 40)
        
        try:
            output = StringIO()
            call_command('showmigrations', 'medecin', stdout=output)
            migrations_output = output.getvalue()
            
            if 'medecin' in migrations_output:
                lines = [line for line in migrations_output.split('\n') if 'medecin' in line]
                applied = [line for line in lines if '[X]' in line]
                pending = [line for line in lines if '[ ]' in line]
                
                print(f"   📋 Migrations appliquées: {len(applied)}")
                print(f"   📋 Migrations en attente: {len(pending)}")
                
                if pending:
                    self.problems.append(f"{len(pending)} migration(s) en attente")
                else:
                    print("   ✅ Toutes les migrations sont appliquées")
            else:
                print("   ❌ Aucune migration trouvée pour medecin")
                self.problems.append("Aucune migration medecin")
                
        except Exception as e:
            print(f"❌ Erreur vérification migrations: {e}")
    
    def generate_solutions(self):
        """Génère des solutions basées sur les problèmes identifiés"""
        print(f"\n💡 SOLUTIONS PROPOSÉES")
        print("-" * 40)
        
        if not self.problems:
            print("✅ Aucun problème détecté - L'application medecin devrait fonctionner")
            return
        
        solution_map = {
            "Template manquant": "Créer le template manquant dans templates/medecin/",
            "Template non résolu": "Vérifier la configuration TEMPLATES dans settings.py",
            "Aucun médecin en base": "Créer un profil médecin via l'admin Django",
            "URL non configurée": "Vérifier medecin/urls.py et les patterns d'URL",
            "Vue manquante": "Implémenter la vue manquante dans medecin/views.py",
            "Erreur accès modèle Medecin": "Vérifier que le modèle Medecin est correctement défini",
            "Accès refusé": "Vérifier les permissions et les décorateurs de vue",
            "Erreur serveur": "Consulter les logs Django pour plus de détails",
        }
        
        for problem in self.problems:
            for key, solution in solution_map.items():
                if key in problem:
                    print(f"🔧 {problem}")
                    print(f"   → {solution}")
                    break
            else:
                print(f"🔧 {problem}")
                print(f"   → Vérifier les logs et la configuration")
        
        print(f"\n🎯 COMMANDES DE DÉPANNAGE:")
        print("1. Vérifier les logs: tail -f logs/django.log")
        print("2. Tester en shell: python manage.py shell")
        print("3. Vérifier URLs: python manage.py show_urls | grep medecin")
        print("4. Redémarrer serveur: Ctrl+C puis python manage.py runserver")

def main():
    print("🩺 DIAGNOSTIC COMPLET MEDECIN - TEMPLATES EXISTANTS")
    print("=" * 70)
    
    diagnoser = MedecinProblemDiagnoser()
    
    # Exécuter les vérifications
    diagnoser.check_templates_exist()
    diagnoser.check_template_resolution()
    diagnoser.check_medecin_views()
    diagnoser.check_authentication()
    diagnoser.check_urls_access()
    diagnoser.check_migrations()
    
    # Générer le rapport
    print(f"\n📊 RAPPORT DE DIAGNOSTIC")
    print("=" * 70)
    
    if diagnoser.problems:
        print(f"❌ PROBLÈMES IDENTIFIÉS ({len(diagnoser.problems)}):")
        for problem in diagnoser.problems:
            print(f"   • {problem}")
    else:
        print("✅ AUCUN PROBLÈME IDENTIFIÉ")
    
    diagnoser.generate_solutions()
    
    print(f"\n🎯 PROCHAINES ÉTAPES:")
    print("1. Redémarrez le serveur Django")
    print("2. Testez: http://127.0.0.1:8000/medecin/dashboard/")
    print("3. Consultez les logs en cas d'erreur")

if __name__ == "__main__":
    main()