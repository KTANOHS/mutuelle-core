#!/usr/bin/env python3
"""
Script d'analyse des views Django - Version corrigée
"""

import os
import sys
import django
import inspect
import time
from collections import defaultdict, Counter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

from django.urls import get_resolver

class DjangoViewsAnalyzerFixed:
    """Analyseur corrigé des views Django"""
    
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
        print("🔍 ANALYSE DES VIEWS DJANGO - RAPPORT CORRIGÉ")
        print("=" * 70)
        
        self.analyze_urls()
        self.analyze_views()
        self.analyze_permissions()
        self.analyze_performance()
        self.generate_report()
    
    def analyze_urls(self):
        """Analyse la structure des URLs"""
        print("\n🌐 ANALYSE DES URLs")
        print("-" * 50)
        
        resolver = get_resolver()
        url_patterns = self._extract_urls(resolver)
        
        self.results['urls'] = url_patterns
        self.results['statistics']['total_urls'] = len(url_patterns)
        
        print(f"📊 URLs totales trouvées: {len(url_patterns)}")
        
        # Grouper par app réelle
        app_patterns = {
            'admin': [],
            'assureur': [],
            'medecin': [],
            'pharmacien': [],
            'membres': [],
            'core': [],
            'api': []
        }
        
        for url_info in url_patterns:
            url_path = url_info['pattern']
            if 'admin' in url_path:
                app_patterns['admin'].append(url_info)
            elif 'assureur' in url_path:
                app_patterns['assureur'].append(url_info)
            elif 'medecin' in url_path:
                app_patterns['medecin'].append(url_info)
            elif 'pharmacien' in url_path:
                app_patterns['pharmacien'].append(url_info)
            elif 'membres' in url_path and 'admin' not in url_path:
                app_patterns['membres'].append(url_info)
            elif 'api' in url_path:
                app_patterns['api'].append(url_info)
            else:
                app_patterns['core'].append(url_info)
        
        for app_name, urls in app_patterns.items():
            if urls:
                print(f"\n📱 {app_name.upper()}: {len(urls)} URLs")
                for url in urls[:3]:
                    print(f"   🔗 {url['pattern']} → {url['view_name']}")
                if len(urls) > 3:
                    print(f"   ... et {len(urls) - 3} autres")
    
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
                    'namespace': namespace,
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
        print("-" * 50)
        
        admin_views = 0
        custom_views = 0
        
        for url_info in self.results['urls']:
            view_func = url_info['view_func']
            view_info = self._analyze_view(view_func, url_info)
            self.results['views'].append(view_info)
            
            # Compter les types de views
            if 'admin' in url_info['pattern'] and any(x in view_info['name'] for x in ['changelist', 'add', 'change', 'delete']):
                admin_views += 1
            else:
                custom_views += 1
        
        self.results['statistics']['admin_views'] = admin_views
        self.results['statistics']['custom_views'] = custom_views
        
        print(f"📊 Vue d'ensemble:")
        print(f"   👑 Views Admin Django: {admin_views}")
        print(f"   🛠️  Views personnalisées: {custom_views}")
        print(f"   📈 Ratio personnalisées: {custom_views/(admin_views + custom_views)*100:.1f}%")
    
    def _analyze_view(self, view_func, url_info):
        """Analyse une view spécifique"""
        view_info = {
            'name': url_info['view_name'],
            'url': url_info['pattern'],
            'type': 'Fonction' if hasattr(view_func, '__name__') else 'Classe',
            'module': view_func.__module__ if hasattr(view_func, '__module__') else 'Unknown',
        }
        
        return view_info
    
    def analyze_permissions(self):
        """Analyse les permissions des views"""
        print("\n🔐 ANALYSE DE SÉCURITÉ")
        print("-" * 50)
        
        # Compter les vues par type de protection
        public_count = 0
        protected_count = 0
        admin_protected = 0
        
        for view_info in self.results['views']:
            url = view_info['url']
            if 'admin' in url:
                admin_protected += 1  # Admin a sa propre protection
            elif any(x in view_info['name'] for x in ['login_required', 'assureur_required', 'medecin_required']):
                protected_count += 1
            else:
                public_count += 1
        
        print(f"📊 Répartition sécurité:")
        print(f"   🔒 Protégées par Django Admin: {admin_protected}")
        print(f"   🔐 Protégées par décorateurs: {protected_count}")
        print(f"   🔓 Publiques: {public_count}")
        
        # Alertes de sécurité
        if public_count > protected_count + admin_protected:
            print(f"🚨 ALERTE: Trop de views publiques ({public_count}) vs protégées ({protected_count + admin_protected})")
        
        self.results['statistics']['security'] = {
            'admin_protected': admin_protected,
            'custom_protected': protected_count,
            'public': public_count
        }
    
    def analyze_performance(self):
        """Analyse les aspects performance"""
        print("\n⚡ ANALYSE DES PERFORMANCES")
        print("-" * 50)
        
        # Analyser la complexité des URLs
        complex_urls = []
        for url_info in self.results['urls']:
            pattern = url_info['pattern']
            complexity = pattern.count('(') + pattern.count(')') + pattern.count('/')
            if complexity > 10:  # Seuil de complexité
                complex_urls.append((url_info['pattern'], complexity))
        
        if complex_urls:
            print(f"⚠️  URLs complexes détectées: {len(complex_urls)}")
            for url, complexity in complex_urls[:3]:
                print(f"   🔧 {url} (complexité: {complexity})")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS PERFORMANCE:")
        if len(self.results['urls']) > 50:
            print("   • Considérez la pagination pour les grandes listes")
        if complex_urls:
            print("   • Simplifiez les URLs complexes")
    
    def generate_report(self):
        """Génère un rapport complet"""
        print("\n📋 RAPPORT FINAL D'ANALYSE")
        print("=" * 70)
        
        stats = self.results['statistics']
        security = stats.get('security', {})
        
        print(f"🎯 SYNTHÈSE DU PROJET:")
        print(f"   • 📊 URLs totales: {stats['total_urls']}")
        print(f"   • 👑 Views Admin: {stats.get('admin_views', 0)}")
        print(f"   • 🛠️  Views personnalisées: {stats.get('custom_views', 0)}")
        print(f"   • 🔐 Niveau de sécurité: {self._get_security_level(security)}")
        print(f"   • ⏱️  Temps d'analyse: {time.time() - self.start_time:.2f}s")
        
        # Analyse par application
        print(f"\n📱 RÉPARTITION PAR MODULE:")
        modules = {
            'Admin Django': stats.get('admin_views', 0),
            'Assureur': len([u for u in self.results['urls'] if 'assureur' in u['pattern'] and 'admin' not in u['pattern']]),
            'Médecin': len([u for u in self.results['urls'] if 'medecin' in u['pattern']]),
            'Pharmacien': len([u for u in self.results['urls'] if 'pharmacien' in u['pattern']]),
            'Membres': len([u for u in self.results['urls'] if 'membres' in u['pattern'] and 'admin' not in u['pattern']]),
            'API': len([u for u in self.results['urls'] if 'api' in u['pattern']]),
            'Core': len([u for u in self.results['urls'] if not any(x in u['pattern'] for x in ['admin', 'assureur', 'medecin', 'pharmacien', 'api'])]),
        }
        
        for module, count in modules.items():
            if count > 0:
                percentage = (count / stats['total_urls']) * 100
                print(f"   • {module}: {count} URLs ({percentage:.1f}%)")
        
        # Recommandations finales
        print(f"\n🚀 RECOMMANDATIONS STRATÉGIQUES:")
        
        if stats.get('custom_views', 0) < 20:
            print("   1. ✅ Architecture bien équilibrée")
        else:
            print("   1. 📈 Beaucoup de fonctionnalités personnalisées")
        
        if security.get('public', 0) > security.get('custom_protected', 0):
            print("   2. 🔒 Renforcez la sécurité des views publiques")
        else:
            print("   2. ✅ Bon niveau de sécurité")
        
        if modules['Admin Django'] > modules['Assureur'] + modules['Médecin'] + modules['Pharmacien']:
            print("   3. 🎯 Pensez à migrer certaines fonctionnalités de l'admin vers des interfaces métier")
        else:
            print("   3. ✅ Bonne répartition admin/interfaces métier")
    
    def _get_security_level(self, security):
        """Évalue le niveau de sécurité"""
        total = security.get('admin_protected', 0) + security.get('custom_protected', 0) + security.get('public', 0)
        if total == 0:
            return "❓ Inconnu"
        
        protected_ratio = (security.get('admin_protected', 0) + security.get('custom_protected', 0)) / total
        
        if protected_ratio > 0.8:
            return "🛡️ Excellente"
        elif protected_ratio > 0.5:
            return "✅ Bonne"
        else:
            return "⚠️  À améliorer"

def main():
    """Fonction principale"""
    try:
        analyzer = DjangoViewsAnalyzerFixed()
        analyzer.analyze_all()
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()