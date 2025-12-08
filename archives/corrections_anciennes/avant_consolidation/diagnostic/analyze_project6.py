#!/usr/bin/env python3
"""
SCRIPT D'ANALYSE DU PROJET DJANGO
Analyse la structure et identifie les modifications nécessaires pour l'implémentation
de la création de membres par les agents avec photos et cartes d'identité.
"""

import os
import sys
import django
from pathlib import Path
import importlib
import inspect

# Configuration de l'environnement Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur lors du setup Django: {e}")
    sys.exit(1)

from django.apps import apps
from django.conf import settings
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class DjangoProjectAnalyzer:
    """Analyseur complet de projet Django"""
    
    def __init__(self):
        self.base_dir = BASE_DIR
        self.analysis = {
            'project_structure': {},
            'apps_analysis': {},
            'models_analysis': {},
            'settings_analysis': {},
            'recommendations': []
        }
    
    def analyze_project_structure(self):
        """Analyse la structure globale du projet"""
        logger.info("🔍 ANALYSE DE LA STRUCTURE DU PROJET")
        logger.info("=" * 60)
        
        structure = {
            'django_version': django.get_version(),
            'project_name': os.path.basename(self.base_dir),
            'apps_installed': [],
            'templates_dirs': [],
            'static_dirs': [],
            'media_config': {},
            'database_config': {}
        }
        
        # Applications installées
        structure['apps_installed'] = list(settings.INSTALLED_APPS)
        
        # Configuration des templates
        for template in settings.TEMPLATES:
            if 'DIRS' in template:
                structure['templates_dirs'].extend(template['DIRS'])
        
        # Configuration des fichiers statiques
        structure['static_dirs'] = settings.STATICFILES_DIRS
        structure['static_root'] = getattr(settings, 'STATIC_ROOT', 'Non configuré')
        
        # Configuration des médias
        structure['media_config'] = {
            'MEDIA_URL': getattr(settings, 'MEDIA_URL', 'Non configuré'),
            'MEDIA_ROOT': getattr(settings, 'MEDIA_ROOT', 'Non configuré')
        }
        
        # Configuration de la base de données
        structure['database_config'] = {
            'engine': settings.DATABASES['default']['ENGINE'],
            'name': settings.DATABASES['default']['NAME']
        }
        
        self.analysis['project_structure'] = structure
        return structure
    
    def analyze_apps(self):
        """Analyse détaillée de chaque application"""
        logger.info("\n📦 ANALYSE DES APPLICATIONS")
        logger.info("=" * 60)
        
        apps_analysis = {}
        
        for app_config in apps.get_app_configs():
            app_name = app_config.name
            app_path = Path(app_config.path)
            
            app_info = {
                'name': app_name,
                'path': str(app_path),
                'has_models': False,
                'has_views': False,
                'has_urls': False,
                'has_templates': False,
                'has_static': False,
                'models_count': 0,
                'models_list': []
            }
            
            # Vérifier les modèles
            try:
                models_module = importlib.import_module(f'{app_name}.models')
                app_info['has_models'] = True
                app_info['models_list'] = [name for name, obj in inspect.getmembers(models_module) 
                                         if inspect.isclass(obj) and issubclass(obj, django.db.models.Model) 
                                         and obj.__module__ == f'{app_name}.models']
                app_info['models_count'] = len(app_info['models_list'])
            except ImportError:
                app_info['has_models'] = False
            
            # Vérifier les vues
            app_info['has_views'] = (app_path / 'views.py').exists()
            
            # Vérifier les URLs
            app_info['has_urls'] = (app_path / 'urls.py').exists()
            
            # Vérifier les templates
            templates_dir = app_path / 'templates'
            app_info['has_templates'] = templates_dir.exists()
            
            # Vérifier les fichiers statiques
            static_dir = app_path / 'static'
            app_info['has_static'] = static_dir.exists()
            
            apps_analysis[app_name] = app_info
            
            # Log des informations de l'application
            status_models = "✅" if app_info['has_models'] else "❌"
            status_views = "✅" if app_info['has_views'] else "❌"
            status_urls = "✅" if app_info['has_urls'] else "❌"
            
            logger.info(f"{app_name}:")
            logger.info(f"  Modèles: {status_models} ({app_info['models_count']} modèles)")
            if app_info['models_list']:
                logger.info(f"    - {', '.join(app_info['models_list'])}")
            logger.info(f"  Vues: {status_views} | URLs: {status_urls}")
            logger.info(f"  Templates: {'✅' if app_info['has_templates'] else '❌'} | Static: {'✅' if app_info['has_static'] else '❌'}")
        
        self.analysis['apps_analysis'] = apps_analysis
        return apps_analysis
    
    def analyze_membre_model(self):
        """Analyse spécifique du modèle Membre"""
        logger.info("\n👤 ANALYSE DU MODÈLE MEMBRE")
        logger.info("=" * 60)
        
        try:
            from membres.models import Membre
            
            model_info = {
                'exists': True,
                'fields': [],
                'photo_field': False,
                'carte_identite_field': False,
                'file_fields': [],
                'required_fields': []
            }
            
            # Analyser tous les champs du modèle
            for field in Membre._meta.get_fields():
                field_info = {
                    'name': field.name,
                    'type': field.get_internal_type(),
                    'blank': getattr(field, 'blank', False),
                    'null': getattr(field, 'null', False),
                    'help_text': getattr(field, 'help_text', ''),
                    'verbose_name': getattr(field, 'verbose_name', field.name)
                }
                
                model_info['fields'].append(field_info)
                
                # Vérifier les champs spécifiques
                if field.name == 'photo':
                    model_info['photo_field'] = True
                    if field.get_internal_type() in ['ImageField', 'FileField']:
                        model_info['file_fields'].append('photo')
                
                if field.name == 'carte_identite':
                    model_info['carte_identite_field'] = True
                    if field.get_internal_type() in ['ImageField', 'FileField']:
                        model_info['file_fields'].append('carte_identite')
                
                # Identifier les champs obligatoires
                if not getattr(field, 'blank', True) and not getattr(field, 'null', True):
                    if hasattr(field, 'primary_key') and not field.primary_key:
                        model_info['required_fields'].append(field.name)
            
            # Affichage des résultats
            logger.info(f"✅ Modèle Membre trouvé")
            logger.info(f"📊 Nombre de champs: {len(model_info['fields'])}")
            logger.info(f"🖼️  Champ photo: {'✅' if model_info['photo_field'] else '❌'}")
            logger.info(f"🆔 Champ carte_identite: {'✅' if model_info['carte_identite_field'] else '❌'}")
            logger.info(f"📎 Champs fichiers: {len(model_info['file_fields'])}")
            
            if not model_info['photo_field'] or not model_info['carte_identite_field']:
                logger.info("\n⚠️  CHAMPS MANQUANTS:")
                if not model_info['photo_field']:
                    logger.info("  - photo (ImageField)")
                if not model_info['carte_identite_field']:
                    logger.info("  - carte_identite (FileField)")
            
            self.analysis['models_analysis']['Membre'] = model_info
            return model_info
            
        except ImportError as e:
            logger.error(f"❌ Modèle Membre non trouvé: {e}")
            return {'exists': False}
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'analyse du modèle Membre: {e}")
            return {'exists': False}
    
    def analyze_agents_app(self):
        """Analyse spécifique de l'application agents"""
        logger.info("\n🛠️ ANALYSE DE L'APPLICATION AGENTS")
        logger.info("=" * 60)
        
        agents_analysis = {
            'exists': False,
            'views': {},
            'urls': {},
            'templates': {},
            'permissions': {}
        }
        
        try:
            # Vérifier si l'application agents existe
            agents_config = apps.get_app_config('agents')
            agents_analysis['exists'] = True
            agents_path = Path(agents_config.path)
            
            logger.info(f"✅ Application agents trouvée: {agents_path}")
            
            # Analyser les vues
            views_file = agents_path / 'views.py'
            if views_file.exists():
                agents_analysis['views']['file_exists'] = True
                
                # Compter les fonctions de vue
                with open(views_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    view_functions = [line for line in content.split('\n') if line.strip().startswith('def ') and '(' in line]
                    agents_analysis['views']['count'] = len(view_functions)
                    agents_analysis['views']['has_member_creation'] = 'creer_membre' in content
                    
                logger.info(f"  Vues: ✅ ({agents_analysis['views']['count']} fonctions)")
                logger.info(f"  Création membre: {'✅' if agents_analysis['views']['has_member_creation'] else '❌'}")
            else:
                agents_analysis['views']['file_exists'] = False
                logger.info("  Vues: ❌")
            
            # Analyser les URLs
            urls_file = agents_path / 'urls.py'
            if urls_file.exists():
                agents_analysis['urls']['file_exists'] = True
                
                with open(urls_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    agents_analysis['urls']['has_member_urls'] = any(pattern in content for pattern in ['creer_membre', 'membres/creer'])
                    
                logger.info(f"  URLs: ✅")
                logger.info(f"  URLs membres: {'✅' if agents_analysis['urls']['has_member_urls'] else '❌'}")
            else:
                agents_analysis['urls']['file_exists'] = False
                logger.info("  URLs: ❌")
            
            # Analyser les templates
            templates_dir = agents_path / 'templates' / 'agents'
            if templates_dir.exists():
                agents_analysis['templates']['exists'] = True
                template_files = list(templates_dir.glob('*.html'))
                agents_analysis['templates']['count'] = len(template_files)
                agents_analysis['templates']['has_member_templates'] = any('membre' in f.name for f in template_files)
                
                logger.info(f"  Templates: ✅ ({agents_analysis['templates']['count']} fichiers)")
                logger.info(f"  Templates membres: {'✅' if agents_analysis['templates']['has_member_templates'] else '❌'}")
            else:
                agents_analysis['templates']['exists'] = False
                logger.info("  Templates: ❌")
            
            # Vérifier les permissions
            try:
                from agents.models import Agent
                agents_analysis['permissions']['agent_model'] = True
                logger.info("  Modèle Agent: ✅")
            except ImportError:
                agents_analysis['permissions']['agent_model'] = False
                logger.info("  Modèle Agent: ❌")
                
        except LookupError:
            logger.error("❌ Application 'agents' non trouvée dans INSTALLED_APPS")
            agents_analysis['exists'] = False
        
        self.analysis['apps_analysis']['agents'] = agents_analysis
        return agents_analysis
    
    def analyze_media_settings(self):
        """Analyse la configuration des médias pour l'upload de fichiers"""
        logger.info("\n📁 ANALYSE DE LA CONFIGURATION MÉDIAS")
        logger.info("=" * 60)
        
        media_analysis = {
            'media_url': getattr(settings, 'MEDIA_URL', None),
            'media_root': getattr(settings, 'MEDIA_ROOT', None),
            'file_upload_permissions': getattr(settings, 'FILE_UPLOAD_PERMISSIONS', None),
            'file_upload_max_memory_size': getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', None),
        }
        
        logger.info(f"📂 MEDIA_URL: {media_analysis['media_url']}")
        logger.info(f"📂 MEDIA_ROOT: {media_analysis['media_root']}")
        
        # Vérifier si MEDIA_ROOT existe
        if media_analysis['media_root'] and os.path.exists(media_analysis['media_root']):
            logger.info("✅ Dossier MEDIA_ROOT existe")
        else:
            logger.warning("⚠️  Dossier MEDIA_ROOT n'existe pas ou n'est pas configuré")
        
        # Vérifier les permissions de fichiers
        if media_analysis['file_upload_permissions']:
            logger.info(f"🔐 Permissions upload: {media_analysis['file_upload_permissions']}")
        else:
            logger.info("🔐 Permissions upload: Défaut (0o644)")
        
        self.analysis['settings_analysis']['media'] = media_analysis
        return media_analysis
    
    def generate_recommendations(self):
        """Génère des recommandations basées sur l'analyse"""
        logger.info("\n💡 RECOMMANDATIONS D'IMPLÉMENTATION")
        logger.info("=" * 60)
        
        recommendations = []
        
        # Vérification du modèle Membre
        membre_model = self.analysis['models_analysis'].get('Membre', {})
        if not membre_model.get('exists'):
            recommendations.append("❌ CRITIQUE: Le modèle Membre n'existe pas")
        else:
            if not membre_model.get('photo_field'):
                recommendations.append("📸 Ajouter le champ 'photo' (ImageField) au modèle Membre")
            if not membre_model.get('carte_identite_field'):
                recommendations.append("🆔 Ajouter le champ 'carte_identite' (FileField) au modèle Membre")
        
        # Vérification de l'application agents
        agents_app = self.analysis['apps_analysis'].get('agents', {})
        if not agents_app.get('exists'):
            recommendations.append("❌ CRITIQUE: L'application 'agents' n'est pas installée")
        else:
            if not agents_app.get('views', {}).get('has_member_creation'):
                recommendations.append("👨‍💼 Ajouter la vue 'creer_membre' dans agents/views.py")
            if not agents_app.get('urls', {}).get('has_member_urls'):
                recommendations.append("🔗 Ajouter les URLs pour la gestion des membres dans agents/urls.py")
            if not agents_app.get('templates', {}).get('has_member_templates'):
                recommendations.append("🎨 Créer les templates pour la création/édition des membres")
        
        # Vérification de la configuration médias
        media_settings = self.analysis['settings_analysis'].get('media', {})
        if not media_settings.get('media_root'):
            recommendations.append("📁 Configurer MEDIA_ROOT dans settings.py")
        if not media_settings.get('media_url'):
            recommendations.append("🌐 Configurer MEDIA_URL dans settings.py")
        
        # Recommandations supplémentaires
        recommendations.extend([
            "✅ Créer un formulaire MembreCreationForm dans agents/forms.py",
            "✅ Ajouter la validation des fichiers (taille, format)",
            "✅ Implémenter la prévisualisation des photos en JavaScript",
            "✅ Ajouter des permissions pour limiter l'accès aux agents",
            "✅ Créer des vues pour lister et éditer les membres",
            "✅ Tester l'upload de fichiers avec différents formats"
        ])
        
        # Afficher les recommandations
        for i, recommendation in enumerate(recommendations, 1):
            logger.info(f"{i}. {recommendation}")
        
        self.analysis['recommendations'] = recommendations
        return recommendations
    
    def generate_implementation_plan(self):
        """Génère un plan d'implémentation détaillé"""
        logger.info("\n📋 PLAN D'IMPLÉMENTATION DÉTAILLÉ")
        logger.info("=" * 60)
        
        plan = [
            "ÉTAPE 1: MODIFICATION DU MODÈLE MEMBRE",
            "  - Ajouter le champ 'photo' (ImageField) dans membres/models.py",
            "  - Ajouter le champ 'carte_identite' (FileField) dans membres/models.py",
            "  - Créer et appliquer les migrations",
            "",
            "ÉTAPE 2: CRÉATION DU FORMULAIRE",
            "  - Créer agents/forms.py avec MembreCreationForm",
            "  - Ajouter la validation des fichiers uploadés",
            "  - Configurer les widgets pour l'interface utilisateur",
            "",
            "ÉTAPE 3: IMPLÉMENTATION DES VUES",
            "  - Ajouter creer_membre() dans agents/views.py",
            "  - Ajouter liste_membres() et detail_membre()",
            "  - Implémenter la gestion des permissions",
            "",
            "ÉTAPE 4: CONFIGURATION DES URLs",
            "  - Ajouter les patterns d'URL dans agents/urls.py",
            "  - Inclure les URLs pour CRUD des membres",
            "",
            "ÉTAPE 5: CRÉATION DES TEMPLATES",
            "  - Créer agents/templates/agents/creer_membre.html",
            "  - Créer agents/templates/agents/liste_membres.html",
            "  - Ajouter JavaScript pour la prévisualisation",
            "",
            "ÉTAPE 6: CONFIGURATION MÉDIAS",
            "  - Vérifier MEDIA_ROOT et MEDIA_URL",
            "  - Configurer le serving des médias en développement",
            "",
            "ÉTAPE 7: TEST ET VALIDATION",
            "  - Tester l'upload de photos et documents",
            "  - Vérifier les permissions d'accès",
            "  - Tester sur différents navigateurs"
        ]
        
        for step in plan:
            logger.info(step)
        
        return plan
    
    def run_complete_analysis(self):
        """Exécute l'analyse complète du projet"""
        logger.info("🚀 DÉBUT DE L'ANALYSE DU PROJET DJANGO")
        logger.info("=" * 60)
        
        try:
            self.analyze_project_structure()
            self.analyze_apps()
            self.analyze_membre_model()
            self.analyze_agents_app()
            self.analyze_media_settings()
            self.generate_recommendations()
            self.generate_implementation_plan()
            
            logger.info("\n" + "=" * 60)
            logger.info("✅ ANALYSE TERMINÉE AVEC SUCCÈS")
            logger.info("=" * 60)
            
            return self.analysis
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'analyse: {e}")
            return None

def main():
    """Fonction principale"""
    analyzer = DjangoProjectAnalyzer()
    analysis_results = analyzer.run_complete_analysis()
    
    if analysis_results:
        print("\n📊 RÉSUMÉ DE L'ANALYSE:")
        print(f"   • Applications analysées: {len(analysis_results['apps_analysis'])}")
        print(f"   • Modèles analysés: {len(analysis_results['models_analysis'])}")
        print(f"   • Recommandations générées: {len(analysis_results['recommendations'])}")
        
        # Sauvegarder le rapport d'analyse
        report_file = BASE_DIR / 'project_analysis_report.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("RAPPORT D'ANALYSE DU PROJET DJANGO\n")
            f.write("=" * 50 + "\n\n")
            
            for key, value in analysis_results.items():
                f.write(f"{key.upper()}:\n")
                f.write(str(value))
                f.write("\n\n")
        
        print(f"\n📄 Rapport détaillé sauvegardé: {report_file}")
    else:
        print("❌ L'analyse a échoué")

if __name__ == "__main__":
    main()