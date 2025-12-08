#!/usr/bin/env python3
"""
Script d'analyse complète de l'administration Django
Analyse les modèles, les configurations admin et les performances
"""

import os
import sys
import django
from django.apps import apps
from django.contrib import admin
from django.conf import settings
import inspect
from datetime import datetime
import time

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votre_projet.settings')
try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur configuration Django: {e}")
    sys.exit(1)

class DjangoAdminAnalyzer:
    """Analyseur de l'administration Django"""
    
    def __init__(self):
        self.start_time = time.time()
        self.results = {
            'models': {},
            'admin_configs': {},
            'performance': {},
            'issues': []
        }
    
    def analyze_all(self):
        """Lance toutes les analyses"""
        print("🔍 ANALYSE DE L'ADMINISTRATION DJANGO")
        print("=" * 60)
        
        self.analyze_models()
        self.analyze_admin_configurations()
        self.analyze_admin_performance()
        self.analyze_security()
        self.generate_report()
    
    def analyze_models(self):
        """Analyse tous les modèles Django"""
        print("\n📊 ANALYSE DES MODÈLES")
        print("-" * 40)
        
        all_models = apps.get_models()
        registered_models = [model for model in all_models if model in admin.site._registry]
        
        print(f"📈 Modèles totaux: {len(all_models)}")
        print(f"📈 Modèles enregistrés dans admin: {len(registered_models)}")
        print(f"📈 Modèles non enregistrés: {len(all_models) - len(registered_models)}")
        
        # Détails par modèle
        for model in all_models:
            model_info = {
                'app': model._meta.app_label,
                'registered': model in admin.site._registry,
                'fields_count': len(model._meta.fields),
                'fields': [field.name for field in model._meta.fields],
                'methods': [method for method in dir(model) if not method.startswith('_')],
            }
            
            if model in admin.site._registry:
                model_admin = admin.site._registry[model]
                model_info['admin_class'] = model_admin.__class__.__name__
                model_info['list_display'] = getattr(model_admin, 'list_display', [])
                model_info['search_fields'] = getattr(model_admin, 'search_fields', [])
                model_info['list_filter'] = getattr(model_admin, 'list_filter', [])
            
            self.results['models'][f"{model._meta.app_label}.{model.__name__}"] = model_info
            
            status = "✅" if model_info['registered'] else "❌"
            print(f"{status} {model._meta.app_label}.{model.__name__}: {len(model_info['fields'])} champs")
    
    def analyze_admin_configurations(self):
        """Analyse les configurations d'administration"""
        print("\n⚙️ ANALYSE DES CONFIGURATIONS ADMIN")
        print("-" * 40)
        
        for model, model_admin in admin.site._registry.items():
            config = {
                'list_display': getattr(model_admin, 'list_display', []),
                'list_display_links': getattr(model_admin, 'list_display_links', None),
                'list_filter': getattr(model_admin, 'list_filter', []),
                'search_fields': getattr(model_admin, 'search_fields', []),
                'readonly_fields': getattr(model_admin, 'readonly_fields', []),
                'ordering': getattr(model_admin, 'ordering', []),
                'actions': [action.__name__ for action in getattr(model_admin, 'actions', [])],
                'custom_templates': self._get_custom_templates(model_admin),
            }
            
            self.results['admin_configs'][f"{model._meta.app_label}.{model.__name__}"] = config
            
            # Vérifications de qualité
            issues = self._check_admin_issues(model, model_admin, config)
            if issues:
                self.results['issues'].extend(issues)
            
            print(f"🔧 {model._meta.app_label}.{model.__name__}:")
            print(f"   📋 Display: {len(config['list_display'])} champs")
            print(f"   🔍 Search: {len(config['search_fields'])} champs")
            print(f"   ⚖️ Filter: {len(config['list_filter'])} filtres")
            print(f"   🛠️ Actions: {len(config['actions'])} actions")
    
    def _get_custom_templates(self, model_admin):
        """Récupère les templates personnalisés"""
        templates = {}
        for attr in ['change_form_template', 'change_list_template', 'delete_confirmation_template']:
            template = getattr(model_admin, attr, None)
            if template:
                templates[attr] = template
        return templates
    
    def _check_admin_issues(self, model, model_admin, config):
        """Vérifie les problèmes potentiels"""
        issues = []
        model_name = f"{model._meta.app_label}.{model.__name__}"
        
        # Vérifier list_display
        if not config['list_display']:
            issues.append(f"⚠️  {model_name}: list_display vide - affiche seulement __str__")
        
        # Vérifier les champs de recherche
        if not config['search_fields']:
            issues.append(f"ℹ️  {model_name}: search_fields vide - recherche désactivée")
        
        # Vérifier les filtres
        if not config['list_filter']:
            issues.append(f"ℹ️  {model_name}: list_filter vide - filtrage désactivé")
        
        # Vérifier les performances
        if len(config['list_display']) > 10:
            issues.append(f"🚨 {model_name}: list_display très long ({len(config['list_display'])} champs) - impact performance")
        
        return issues
    
    def analyze_admin_performance(self):
        """Analyse les aspects performance de l'admin"""
        print("\n⚡ ANALYSE DES PERFORMANCES")
        print("-" * 40)
        
        performance_issues = []
        
        for model, model_admin in admin.site._registry.items():
            model_name = f"{model._meta.app_label}.{model.__name__}"
            
            # Vérifier les relations dans list_display
            list_display = getattr(model_admin, 'list_display', [])
            for field in list_display:
                if hasattr(model, field) and hasattr(getattr(model, field), 'field'):
                    field_obj = getattr(model, field).field
                    if hasattr(field_obj, 'related_model'):
                        performance_issues.append(
                            f"⚠️  {model_name}: list_display contient une relation '{field}' - peut ralentir l'affichage"
                        )
            
            # Vérifier les select_related/prefetch_related
            if not hasattr(model_admin, 'list_select_related'):
                performance_issues.append(
                    f"ℹ️  {model_name}: list_select_related non défini - optimisations DB manquantes"
                )
        
        self.results['performance']['issues'] = performance_issues
        
        for issue in performance_issues:
            print(issue)
    
    def analyze_security(self):
        """Analyse les aspects sécurité"""
        print("\n🔒 ANALYSE DE SÉCURITÉ")
        print("-" * 40)
        
        security_issues = []
        
        # Vérifier les permissions
        for model, model_admin in admin.site._registry.items():
            model_name = f"{model._meta.app_label}.{model.__name__}"
            
            # Vérifier has_add_permission, etc.
            if not hasattr(model_admin, 'has_add_permission'):
                security_issues.append(f"ℹ️  {model_name}: pas de contrôle personnalisé des permissions d'ajout")
            
            if not hasattr(model_admin, 'has_change_permission'):
                security_issues.append(f"ℹ️  {model_name}: pas de contrôle personnalisé des permissions de modification")
            
            if not hasattr(model_admin, 'has_delete_permission'):
                security_issues.append(f"ℹ️  {model_name}: pas de contrôle personnalisé des permissions de suppression")
        
        self.results['security'] = security_issues
        
        for issue in security_issues:
            print(issue)
    
    def generate_report(self):
        """Génère un rapport complet"""
        print("\n📋 RAPPORT COMPLET D'ANALYSE")
        print("=" * 60)
        
        # Statistiques générales
        total_models = len(self.results['models'])
        registered_models = len(self.results['admin_configs'])
        unregistered_models = total_models - registered_models
        
        print(f"📊 STATISTIQUES GÉNÉRALES:")
        print(f"   • Modèles totaux: {total_models}")
        print(f"   • Modèles enregistrés: {registered_models}")
        print(f"   • Modèles non enregistrés: {unregistered_models}")
        print(f"   • Problèmes identifiés: {len(self.results['issues'])}")
        print(f"   • Temps d'analyse: {time.time() - self.start_time:.2f}s")
        
        # Modèles non enregistrés
        if unregistered_models > 0:
            print(f"\n❌ MODÈLES NON ENREGISTRÉS DANS L'ADMIN:")
            for model_name, info in self.results['models'].items():
                if not info['registered']:
                    print(f"   • {model_name} ({len(info['fields'])} champs)")
        
        # Problèmes critiques
        critical_issues = [issue for issue in self.results['issues'] if '🚨' in issue]
        if critical_issues:
            print(f"\n🚨 PROBLÈMES CRITIQUES:")
            for issue in critical_issues:
                print(f"   {issue}")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        if unregistered_models > 0:
            print("   1. Enregistrez les modèles manquants dans l'admin")
        if critical_issues:
            print("   2. Résolvez les problèmes de performance identifiés")
        if not self.results['security']:
            print("   3. Implémentez des contrôles de permissions personnalisés")
        
        # Générer un fichier de rapport
        self.generate_report_file()
    
    def generate_report_file(self):
        """Génère un fichier de rapport détaillé"""
        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"admin_analysis_report_{timestamp}.txt"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("RAPPORT D'ANALYSE DE L'ADMINISTRATION DJANGO\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("MODÈLES ENREGISTRÉS:\n")
            f.write("-" * 20 + "\n")
            for model_name, config in self.results['admin_configs'].items():
                f.write(f"{model_name}:\n")
                f.write(f"  - Display: {config['list_display']}\n")
                f.write(f"  - Search: {config['search_fields']}\n")
                f.write(f"  - Filter: {config['list_filter']}\n")
                f.write(f"  - Actions: {config['actions']}\n\n")
            
            f.write("PROBLÈMES IDENTIFIÉS:\n")
            f.write("-" * 20 + "\n")
            for issue in self.results['issues']:
                f.write(f"{issue}\n")
        
        print(f"📄 Rapport détaillé généré: {report_filename}")

def main():
    """Fonction principale"""
    try:
        analyzer = DjangoAdminAnalyzer()
        analyzer.analyze_all()
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        import traceback
from django.utils import timezone
        traceback.print_exc()

if __name__ == "__main__":
    main()