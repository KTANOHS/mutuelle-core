#!/usr/bin/env python3
"""
Script d'analyse complète des views Django
Analyse les URLs, les views, les permissions et les performances
"""

import os
import sys
import django
import inspect
from urllib.parse import urlparse
from collections import defaultdict, Counter
import time

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

from django.urls import get_resolver
from django.core.handlers.wsgi import WSGIRequest
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.db.models import Model
from django.utils import timezone

class DjangoViewsAnalyzer:
    """Analyseur complet des views Django"""
    
    def __init__(self):
        self.start_time = time.time()
        self.results = {
            'urls': [],
            'views': [],
            'apps': defaultdict(list),
            'issues': [],
            'statistics': {}
        }
    
    def analyze_all(self):
        """Lance toutes les analyses"""
        print("🔍 ANALYSE DES VIEWS DJANGO")
        print("=" * 60)
        
        self.analyze_urls()
        self.analyze_views()
        self.analyze_permissions()
        self.analyze_performance()
        self.generate_report()
    
    def analyze_urls(self):
        """Analyse la structure des URLs"""
        print("\n🌐 ANALYSE DES URLs")
        print("-" * 40)
        
        resolver = get_resolver()
        url_patterns = self._extract_urls(resolver)
        
        self.results['urls'] = url_patterns
        self.results['statistics']['total_urls'] = len(url_patterns)
        
        print(f"📊 URLs totales trouvées: {len(url_patterns)}")
        
        # Grouper par app
        for url_info in url_patterns:
            app_name = url_info.get('app_name', 'core')
            self.results['apps'][app_name].append(url_info)
        
        # Afficher les URLs par app
        for app_name, urls in self.results['apps'].items():
            print(f"\n📱 Application: {app_name}")
            print(f"   📈 URLs: {len(urls)}")
            for url in urls[:5]:  # Afficher les 5 premières
                print(f"   🔗 {url['pattern']} → {url['view_name']}")
            if len(urls) > 5:
                print(f"   ... et {len(urls) - 5} autres URLs")
    
    def _extract_urls(self, resolver, namespace='', prefix=''):
        """Extrait récursivement toutes les URLs"""
        url_patterns = []
        
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'url_patterns'):
                # Sous-URLs (include)
                new_namespace = namespace
                if pattern.namespace:
                    new_namespace = f"{namespace}:{pattern.namespace}" if namespace else pattern.namespace
                
                new_prefix = f"{prefix}{pattern.pattern.regex.pattern}"
                url_patterns.extend(self._extract_urls(pattern, new_namespace, new_prefix))
            else:
                # URL simple
                url_info = {
                    'pattern': f"{prefix}{pattern.pattern.regex.pattern}",
                    'view_name': self._get_view_name(pattern),
                    'view_func': pattern.callback,
                    'app_name': namespace.split(':')[0] if ':' in namespace else 'core',
                    'namespace': namespace,
                    'name': pattern.name,
                }
                url_patterns.append(url_info)
        
        return url_patterns
    
    def _get_view_name(self, pattern):
        """Retourne le nom de la view"""
        if hasattr(pattern.callback, '__name__'):
            return pattern.callback.__name__
        return str(pattern.callback)
    
    def analyze_views(self):
        """Analyse détaillée des views"""
        print("\n👁️ ANALYSE DES VIEWS")
        print("-" * 40)
        
        for url_info in self.results['urls']:
            view_func = url_info['view_func']
            view_info = self._analyze_view(view_func, url_info)
            self.results['views'].append(view_info)
            
            # Afficher les informations basiques
            status = "✅" if not view_info['issues'] else "⚠️"
            print(f"{status} {url_info['pattern']}")
            print(f"   👤 View: {view_info['name']}")
            print(f"   📍 Type: {view_info['type']}")
            print(f"   🔐 Login required: {view_info['login_required']}")
            
            if view_info['issues']:
                for issue in view_info['issues']:
                    print(f"   ❗ {issue}")
    
    def _analyze_view(self, view_func, url_info):
        """Analyse une view spécifique"""
        view_info = {
            'name': url_info['view_name'],
            'url': url_info['pattern'],
            'type': 'Fonction' if hasattr(view_func, '__name__') else 'Classe',
            'module': view_func.__module__ if hasattr(view_func, '__module__') else 'Unknown',
            'login_required': False,
            'permissions': [],
            'decorators': [],
            'issues': [],
            'parameters': [],
        }
        
        # Analyser les décorateurs
        view_info.update(self._analyze_decorators(view_func))
        
        # Analyser les paramètres
        view_info.update(self._analyze_parameters(view_func))
        
        # Vérifier les problèmes communs
        view_info['issues'].extend(self._check_view_issues(view_func, view_info))
        
        return view_info
    
    def _analyze_decorators(self, view_func):
        """Analyse les décorateurs appliqués à la view"""
        result = {
            'login_required': False,
            'permission_required': False,
            'decorators': []
        }
        
        # Vérifier les décorateurs communs
        try:
            from django.contrib.auth.decorators import login_required, permission_required
            from django.views.decorators.http import require_http_methods
            from django.views.decorators.cache import cache_page
            
            # Cette analyse est basique - une analyse plus poussée nécessiterait l'inspection AST
            func_str = str(view_func)
            if 'login_required' in func_str:
                result['login_required'] = True
                result['decorators'].append('login_required')
            
            if 'permission_required' in func_str:
                result['permission_required'] = True
                result['decorators'].append('permission_required')
                
        except ImportError:
            pass
        
        return result
    
    def _analyze_parameters(self, view_func):
        """Analyse les paramètres de la view"""
        result = {'parameters': []}
        
        try:
            if hasattr(view_func, '__code__'):
                param_names = view_func.__code__.co_varnames[:view_func.__code__.co_argcount]
                result['parameters'] = list(param_names)
        except:
            pass
        
        return result
    
    def _check_view_issues(self, view_func, view_info):
        """Vérifie les problèmes potentiels dans les views"""
        issues = []
        
        # Vérifier si c'est une view fonction simple
        if view_info['type'] == 'Fonction':
            # Vérifier le nombre de paramètres
            if len(view_info['parameters']) > 2:
                issues.append(f"Trop de paramètres ({len(view_info['parameters'])})")
            
            # Vérifier la présence de request
            if 'request' not in view_info['parameters']:
                issues.append("Paramètre 'request' manquant")
        
        # Vérifier les noms problématiques
        problematic_names = ['test_', 'debug_', 'temp_']
        for bad_name in problematic_names:
            if view_info['name'].startswith(bad_name):
                issues.append(f"Nom potentiellement problématique: {view_info['name']}")
        
        return issues
    
    def analyze_permissions(self):
        """Analyse les permissions des views"""
        print("\n🔐 ANALYSE DES PERMISSIONS")
        print("-" * 40)
        
        login_required_count = 0
        public_views = 0
        
        for view_info in self.results['views']:
            if view_info['login_required']:
                login_required_count += 1
                print(f"🔒 {view_info['url']} - Login requis")
            else:
                public_views += 1
                print(f"🔓 {view_info['url']} - Public")
        
        self.results['statistics']['login_required'] = login_required_count
        self.results['statistics']['public_views'] = public_views
        
        print(f"\n📊 Résumé permissions:")
        print(f"   🔒 Views protégées: {login_required_count}")
        print(f"   🔓 Views publiques: {public_views}")
        print(f"   📈 Taux de protection: {login_required_count/(login_required_count + public_views)*100:.1f}%")
    
    def analyze_performance(self):
        """Analyse les aspects performance"""
        print("\n⚡ ANALYSE DES PERFORMANCES")
        print("-" * 40)
        
        # Compter les types de views
        view_types = Counter([view['type'] for view in self.results['views']])
        
        print("📊 Types de views:")
        for view_type, count in view_types.items():
            print(f"   {view_type}: {count}")
        
        # Identifier les views complexes
        complex_views = []
        for view_info in self.results['views']:
            if len(view_info.get('parameters', [])) > 3:
                complex_views.append(view_info)
        
        if complex_views:
            print(f"\n⚠️  Views complexes (plus de 3 paramètres): {len(complex_views)}")
            for view in complex_views[:3]:  # Afficher les 3 premières
                print(f"   🔧 {view['name']} - {len(view['parameters'])} paramètres")
    
    def generate_report(self):
        """Génère un rapport complet"""
        print("\n📋 RAPPORT COMPLET D'ANALYSE")
        print("=" * 60)
        
        stats = self.results['statistics']
        
        print(f"📊 STATISTIQUES GÉNÉRALES:")
        print(f"   • URLs totales: {stats['total_urls']}")
        print(f"   • Applications: {len(self.results['apps'])}")
        print(f"   • Views protégées: {stats.get('login_required', 0)}")
        print(f"   • Views publiques: {stats.get('public_views', 0)}")
        print(f"   • Temps d'analyse: {time.time() - self.start_time:.2f}s")
        
        # Applications avec le plus d'URLs
        print(f"\n📱 APPLICATIONS PAR NOMBRE D'URLs:")
        for app_name, urls in sorted(self.results['apps'].items(), 
                                   key=lambda x: len(x[1]), reverse=True):
            print(f"   • {app_name}: {len(urls)} URLs")
        
        # Problèmes identifiés
        all_issues = [issue for view in self.results['views'] for issue in view['issues']]
        if all_issues:
            print(f"\n🚨 PROBLÈMES IDENTIFIÉS ({len(all_issues)}):")
            for issue in set(all_issues)[:10]:  # Afficher les 10 premiers uniques
                print(f"   • {issue}")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        if stats.get('public_views', 0) > stats.get('login_required', 0):
            print("   1. Vérifiez la sécurité des views publiques")
        if len(all_issues) > 0:
            print("   2. Corrigez les problèmes identifiés")
        
        # Générer un fichier de rapport
        self.generate_report_file()
    
    def generate_report_file(self):
        """Génère un fichier de rapport détaillé"""
        import datetime
        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"views_analysis_report_{timestamp}.txt"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("RAPPORT D'ANALYSE DES VIEWS DJANGO\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("APPLICATIONS ET URLs:\n")
            f.write("-" * 30 + "\n")
            for app_name, urls in self.results['apps'].items():
                f.write(f"\n{app_name.upper()} ({len(urls)} URLs):\n")
                for url in urls:
                    f.write(f"  {url['pattern']} → {url['view_name']}\n")
            
            f.write("\nPROBLÈMES IDENTIFIÉS:\n")
            f.write("-" * 30 + "\n")
            all_issues = [issue for view in self.results['views'] for issue in view['issues']]
            for issue in set(all_issues):
                f.write(f"- {issue}\n")
        
        print(f"📄 Rapport détaillé généré: {report_filename}")

def main():
    """Fonction principale"""
    try:
        analyzer = DjangoViewsAnalyzer()
        analyzer.analyze_all()
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()