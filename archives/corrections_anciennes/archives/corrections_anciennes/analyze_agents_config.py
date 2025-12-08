#!/usr/bin/env python
"""
Script d'analyse de la configuration des URLs et templates pour l'application agents
"""

import os
import sys
import django
from pathlib import Path
import re

# Configuration Django
sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.urls import get_resolver, URLPattern, URLResolver
from django.template.loader import get_template
from django.conf import settings

class AgentsConfigAnalyzer:
    def __init__(self):
        self.agents_templates = []
        self.agents_urls = []
        self.issues = []
        
    def analyze_templates_structure(self):
        """Analyse la structure des templates agents"""
        print("=" * 80)
        print("ANALYSE DES TEMPLATES AGENTS")
        print("=" * 80)
        
        templates_dirs = []
        for template_dir in settings.TEMPLATES[0].get('DIRS', []):
            if os.path.exists(template_dir):
                templates_dirs.append(template_dir)
        
        # Ajouter les dossiers d'applications
        for app in settings.INSTALLED_APPS:
            if 'agents' in app:
                app_path = sys.modules[app].__path__[0]
                template_path = os.path.join(app_path, 'templates')
                if os.path.exists(template_path):
                    templates_dirs.append(template_path)
        
        # Rechercher les templates agents
        agents_templates_found = []
        for template_dir in templates_dirs:
            agents_dir = os.path.join(template_dir, 'agents')
            if os.path.exists(agents_dir):
                for root, dirs, files in os.walk(agents_dir):
                    for file in files:
                        if file.endswith('.html'):
                            rel_path = os.path.relpath(os.path.join(root, file), template_dir)
                            agents_templates_found.append(rel_path)
                            
                            # Vérifier si le template est accessible
                            try:
                                get_template(rel_path)
                                status = "✅ ACCESSIBLE"
                            except Exception as e:
                                status = f"❌ ERREUR: {str(e)}"
                                self.issues.append(f"Template inaccessible: {rel_path} - {e}")
                            
                            print(f"  {rel_path} - {status}")
        
        self.agents_templates = agents_templates_found
        return agents_templates_found

    def analyze_urls_configuration(self):
        """Analyse la configuration des URLs"""
        print("\n" + "=" * 80)
        print("ANALYSE DES URLs AGENTS")
        print("=" + "=" * 80)
        
        resolver = get_resolver()
        agents_urls = []
        
        def extract_urls(url_patterns, prefix='', namespace=None):
            for pattern in url_patterns:
                if isinstance(pattern, URLPattern):
                    full_path = prefix + str(pattern.pattern)
                    name = pattern.name
                    if namespace:
                        name = f"{namespace}:{name}"
                    
                    # Vérifier si c'est une URL agents
                    if 'agent' in str(full_path).lower() or 'agent' in str(name).lower():
                        agents_urls.append({
                            'path': full_path,
                            'name': name,
                            'callback': pattern.callback,
                            'pattern': pattern
                        })
                        print(f"  {full_path} -> {name}")
                        
                elif isinstance(pattern, URLResolver):
                    new_prefix = prefix + str(pattern.pattern)
                    new_namespace = pattern.namespace
                    if namespace and new_namespace:
                        new_namespace = f"{namespace}:{new_namespace}"
                    elif not new_namespace:
                        new_namespace = namespace
                    
                    extract_urls(pattern.url_patterns, new_prefix, new_namespace)
        
        extract_urls(resolver.url_patterns)
        self.agents_urls = agents_urls
        return agents_urls

    def analyze_views_templates_mapping(self):
        """Analyse la correspondance entre vues et templates"""
        print("\n" + "=" * 80)
        print("CORRESPONDANCE VUES -> TEMPLATES")
        print("=" + "=" * 80)
        
        from agents import views
        
        # Mapping des vues aux templates attendus
        expected_mapping = {
            'dashboard_agent': 'agents/dashboard.html',
            'creer_bon_soin': 'agents/creer_bon_soin.html', 
            'liste_membres': 'agents/liste_membres.html',
            'verification_cotisation': 'agents/verification_cotisation.html',
            'historique_bons_soin': 'agents/historique_bons.html',
            'agents_notifications': 'agents/notifications.html',
            'rapport_performance': 'agents/rapport_performance.html',
        }
        
        for view_name, expected_template in expected_mapping.items():
            view_func = getattr(views, view_name, None)
            if view_func:
                # Essayer de déterminer le template utilisé
                template_used = self._get_view_template(view_func, view_name)
                status = "✅ OK" if template_used == expected_template else f"⚠️ ATTENDU: {expected_template}"
                print(f"  {view_name}: {template_used} - {status}")
                
                if template_used != expected_template:
                    self.issues.append(f"Template mismatch: {view_name} utilise {template_used} au lieu de {expected_template}")
            else:
                print(f"  {view_name}: ❌ VUE NON TROUVÉE")
                self.issues.append(f"Vue manquante: {view_name}")

    def _get_view_template(self, view_func, view_name):
        """Tente de déterminer le template utilisé par une vue"""
        try:
            # Pour les vues fonctionnelles qui utilisent render
            if hasattr(view_func, '__code__'):
                source = view_func.__code__.co_consts
                for const in source:
                    if const and isinstance(const, str) and const.endswith('.html'):
                        return const
            
            # Pour les vues basées sur les classes
            if hasattr(view_func, 'view_class'):
                view_class = view_func.view_class
                if hasattr(view_class, 'template_name'):
                    return view_class.template_name
            
            # Vérifier dans le code source
            import inspect
            source = inspect.getsource(view_func)
            template_match = re.search(r'render\([^,]+,\s*[\'"]([^\'"]+\.html)[\'"]', source)
            if template_match:
                return template_match.group(1)
                
        except Exception as e:
            pass
            
        return "❓ INCONNU"

    def check_template_existence(self):
        """Vérifie l'existence des templates requis"""
        print("\n" + "=" * 80)
        print("VÉRIFICATION DES TEMPLATES REQUIS")
        print("=" + "=" * 80)
        
        required_templates = [
            'agents/base.html',
            'agents/dashboard.html', 
            'agents/creer_bon_soin.html',
            'agents/liste_membres.html',
            'agents/verification_cotisation.html',
            'agents/historique_bons.html',
            'agents/notifications.html',
            'agents/rapport_performance.html',
        ]
        
        for template in required_templates:
            try:
                get_template(template)
                print(f"  {template} - ✅ EXISTE")
            except Exception as e:
                print(f"  {template} - ❌ MANQUANT: {e}")
                self.issues.append(f"Template manquant: {template}")

    def analyze_url_accessibility(self):
        """Teste l'accessibilité des URLs agents"""
        print("\n" + "=" * 80)
        print("TEST D'ACCESSIBILITÉ DES URLs")
        print("=" + "=" * 80)
        
        from django.test import Client
        from django.contrib.auth.models import User
        
        client = Client()
        
        # Créer un utilisateur de test (à adapter selon votre modèle)
        try:
            test_user = User.objects.get(username='test_agent')
        except User.DoesNotExist:
            test_user = User.objects.create_user('test_agent', 'test@example.com', 'testpass')
        
        client.force_login(test_user)
        
        for url_info in self.agents_urls:
            url_path = url_info['path'].replace('^', '').replace('$', '')
            # Nettoyer le chemin
            url_path = re.sub(r'\\[^\\]*', '', url_path)  # Supprimer les groupes regex
            
            try:
                response = client.get(f'/{url_path}')
                status = f"✅ {response.status_code}"
                if response.status_code == 404:
                    status = "❌ 404"
                    self.issues.append(f"URL inaccessible: {url_path}")
                elif response.status_code == 403:
                    status = "🔒 403 (Permission)"
                elif response.status_code == 500:
                    status = "💥 500 (Erreur serveur)"
                    self.issues.append(f"Erreur serveur sur: {url_path}")
                    
            except Exception as e:
                status = f"💥 ERREUR: {str(e)}"
                self.issues.append(f"Exception sur {url_path}: {e}")
            
            print(f"  {url_path} - {status}")

    def generate_report(self):
        """Génère un rapport complet"""
        print("\n" + "=" * 80)
        print("RAPPORT DE DIAGNOSTIC COMPLET")
        print("=" * 80)
        
        # Exécuter toutes les analyses
        self.analyze_templates_structure()
        self.analyze_urls_configuration() 
        self.analyze_views_templates_mapping()
        self.check_template_existence()
        self.analyze_url_accessibility()
        
        # Résumé des problèmes
        print("\n" + "=" * 80)
        print("RÉSUMÉ DES PROBLÈMES IDENTIFIÉS")
        print("=" * 80)
        
        if self.issues:
            for i, issue in enumerate(self.issues, 1):
                print(f"{i}. {issue}")
        else:
            print("✅ Aucun problème identifié !")
        
        # Recommandations
        print("\n" + "=" * 80)
        print("RECOMMANDATIONS")
        print("=" * 80)
        
        if any("dashboard" in issue.lower() for issue in self.issues):
            print("🔧 Problèmes de dashboard détectés:")
            print("   - Vérifiez que l'URL '/dashboard/' est bien configurée")
            print("   - Assurez-vous que le template 'agents/dashboard.html' existe")
            print("   - Vérifiez les permissions de l'utilisateur")
        
        if any("template" in issue.lower() for issue in self.issues):
            print("🔧 Problèmes de templates détectés:")
            print("   - Vérifiez la structure des dossiers de templates")
            print("   - Assurez-vous que APP_DIRS = True dans settings.TEMPLATES")
            print("   - Vérifiez les noms de templates dans les vues")
        
        if any("url" in issue.lower() for issue in self.issues):
            print("🔧 Problèmes d'URLs détectés:")
            print("   - Vérifiez l'inclusion des URLs agents dans urls.py principal")
            print("   - Assurez-vous que les noms d'URLs sont corrects")
            print("   - Vérifiez les patterns regex dans les URLs")

    def check_urls_file(self):
        """Vérifie spécifiquement le fichier urls.py des agents"""
        print("\n" + "=" * 80)
        print("ANALYSE DU FICHIER URLs.PY DES AGENTS")
        print("=" * 80)
        
        try:
            from agents import urls as agents_urls
            print("✅ Fichier agents/urls.py trouvé")
            
            # Analyser les patterns
            if hasattr(agents_urls, 'urlpatterns'):
                print(f"📋 {len(agents_urls.urlpatterns)} patterns d'URL détectés:")
                for pattern in agents_urls.urlpatterns:
                    if hasattr(pattern, 'pattern'):
                        print(f"  - {pattern.pattern} -> {getattr(pattern, 'name', 'Sans nom')}")
            
        except ImportError:
            print("❌ Fichier agents/urls.py non trouvé")
            self.issues.append("Fichier agents/urls.py manquant")
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse: {e}")
            self.issues.append(f"Erreur dans agents/urls.py: {e}")

def main():
    """Fonction principale"""
    analyzer = AgentsConfigAnalyzer()
    
    print("🔍 DÉMARRAGE DE L'ANALYSE DE CONFIGURATION AGENTS")
    print("=" * 80)
    
    # Vérifications de base
    analyzer.check_urls_file()
    
    # Analyse complète
    analyzer.generate_report()
    
    print("\n" + "=" * 80)
    print("ANALYSE TERMINÉE")
    print("=" * 80)

if __name__ == "__main__":
    main()