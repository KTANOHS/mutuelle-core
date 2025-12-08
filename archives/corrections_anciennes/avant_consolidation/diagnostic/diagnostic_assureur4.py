#!/usr/bin/env python
"""
Script de diagnostic pour l'application assureur
Vérifie les vues, URLs, templates et leurs correspondances
"""

import os
import sys
import inspect
import django
from django.urls import resolve, Resolver404
from django.core.management import execute_from_command_line
from pathlib import Path

# Configuration Django
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation de Django: {e}")
    sys.exit(1)

# Importations après Django setup
from django.urls import get_resolver
from assureur import views
from assureur import urls as assureur_urls
from django.template.loader import get_template
from django.template import TemplateDoesNotExist

class AssureurDiagnostic:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.template_dir = self.base_dir / 'templates' / 'assureur'
        self.views_module = views
        self.urls_module = assureur_urls
        
    def get_all_views(self):
        """Récupère toutes les vues du module assureur.views"""
        views_list = []
        
        for name, obj in inspect.getmembers(self.views_module):
            if inspect.isfunction(obj) and obj.__module__ == 'assureur.views':
                views_list.append({
                    'name': name,
                    'function': obj,
                    'file': inspect.getfile(obj),
                    'line': inspect.getsourcelines(obj)[1]
                })
            elif hasattr(obj, '__class__') and obj.__class__.__name__ in ['function', 'type']:
                # Pour les classes basées sur View
                views_list.append({
                    'name': name,
                    'class': obj,
                    'type': 'class',
                    'file': inspect.getfile(obj) if hasattr(obj, '__file__') else 'N/A'
                })
        
        return views_list
    
    def get_url_patterns(self):
        """Récupère tous les patterns d'URL de l'application assureur"""
        patterns = []
        
        try:
            for pattern in self.urls_module.urlpatterns:
                pattern_info = {
                    'pattern': str(pattern.pattern),
                    'name': pattern.name,
                    'lookup_str': str(pattern.lookup_str) if hasattr(pattern, 'lookup_str') else '',
                    'callback': pattern.callback if hasattr(pattern, 'callback') else None,
                }
                patterns.append(pattern_info)
        except AttributeError as e:
            print(f"⚠️ Erreur lors de la lecture des URLs: {e}")
        
        return patterns
    
    def get_all_templates(self):
        """Liste tous les templates dans templates/assureur/"""
        templates = []
        
        if not self.template_dir.exists():
            print(f"❌ Le dossier de templates n'existe pas: {self.template_dir}")
            return templates
        
        for root, dirs, files in os.walk(self.template_dir):
            for file in files:
                if file.endswith('.html'):
                    rel_path = os.path.relpath(os.path.join(root, file), self.template_dir)
                    templates.append({
                        'path': f'assureur/{rel_path}',
                        'full_path': os.path.join(root, file),
                        'exists': True
                    })
        
        return templates
    
    def check_view_templates(self):
        """Vérifie les templates utilisés par chaque vue"""
        results = []
        
        for view in self.get_all_views():
            view_name = view['name']
            view_func = view.get('function')
            
            if not view_func:
                continue
            
            # Extraire le template du code source
            try:
                source = inspect.getsource(view_func)
                template_line = None
                
                # Chercher les appels à render()
                for line in source.split('\n'):
                    if 'render(' in line and 'template' in line.lower():
                        template_line = line
                        break
                    elif 'template_name' in line:
                        template_line = line
                        break
                
                if template_line:
                    # Essayer d'extraire le nom du template
                    import re
                    template_match = re.search(r"'([^']+)'", template_line)
                    if not template_match:
                        template_match = re.search(r'"([^"]+)"', template_line)
                    
                    if template_match:
                        template_name = template_match.group(1)
                        
                        # Vérifier si le template existe
                        try:
                            get_template(template_name)
                            template_exists = True
                        except TemplateDoesNotExist:
                            template_exists = False
                        
                        results.append({
                            'view': view_name,
                            'template': template_name,
                            'exists': template_exists,
                            'line': template_line.strip()
                        })
                    else:
                        results.append({
                            'view': view_name,
                            'template': 'NON DÉTECTÉ',
                            'exists': None,
                            'line': template_line.strip()
                        })
                else:
                    results.append({
                        'view': view_name,
                        'template': 'AUCUN (vue API ou redirection)',
                        'exists': None,
                        'line': 'N/A'
                    })
                    
            except Exception as e:
                results.append({
                    'view': view_name,
                    'template': f'ERREUR: {str(e)}',
                    'exists': None,
                    'line': 'N/A'
                })
        
        return results
    
    def check_url_view_mapping(self):
        """Vérifie la correspondance entre URLs et vues"""
        mappings = []
        
        for pattern in self.get_url_patterns():
            if pattern['callback']:
                try:
                    view_name = pattern['callback'].__name__
                    module = pattern['callback'].__module__
                    
                    # Vérifier si la vue existe dans le module assureur.views
                    view_exists = hasattr(self.views_module, view_name)
                    
                    mappings.append({
                        'url': pattern['pattern'],
                        'name': pattern['name'],
                        'view': view_name,
                        'module': module,
                        'exists': view_exists
                    })
                except AttributeError:
                    mappings.append({
                        'url': pattern['pattern'],
                        'name': pattern['name'],
                        'view': 'FONCTION ANONYME OU CLASSE',
                        'module': 'N/A',
                        'exists': True
                    })
        
        return mappings
    
    def find_broken_templates(self):
        """Cherche les templates manquants référencés dans les vues"""
        broken = []
        all_templates = self.get_all_templates()
        template_names = [t['path'] for t in all_templates]
        
        for check in self.check_view_templates():
            if check['template'] not in ['NON DÉTECTÉ', 'AUCUN (vue API ou redirection)', None]:
                if check['template'] not in template_names:
                    broken.append(check)
        
        return broken
    
    def check_template_render(self, template_name):
        """Vérifie si un template peut être rendu sans erreur"""
        try:
            template = get_template(template_name)
            # Essayer de compiler le template
            template.template
            return {
                'template': template_name,
                'status': 'OK',
                'error': None
            }
        except TemplateDoesNotExist:
            return {
                'template': template_name,
                'status': 'MISSING',
                'error': 'Template non trouvé'
            }
        except Exception as e:
            return {
                'template': template_name,
                'status': 'ERROR',
                'error': str(e)
            }
    
    def run_full_diagnostic(self):
        """Exécute un diagnostic complet"""
        print("=" * 80)
        print("🔍 DIAGNOSTIC COMPLET - APPLICATION ASSUREUR")
        print("=" * 80)
        
        # 1. Informations générales
        print("\n📊 INFORMATIONS GÉNÉRALES")
        print("-" * 40)
        print(f"📁 Dossier templates: {self.template_dir}")
        print(f"📁 Existe: {self.template_dir.exists()}")
        print(f"📁 Nombre de fichiers: {len(os.listdir(self.template_dir) if self.template_dir.exists() else [])}")
        
        # 2. Vues détectées
        print("\n👁️ VUES DÉTECTÉES")
        print("-" * 40)
        views = self.get_all_views()
        print(f"Nombre de vues trouvées: {len(views)}")
        for i, view in enumerate(views[:20], 1):  # Limité à 20 pour la lisibilité
            print(f"{i:2d}. {view['name']}")
        if len(views) > 20:
            print(f"... et {len(views) - 20} autres")
        
        # 3. URLs configurées
        print("\n🔗 URLs CONFIGURÉES")
        print("-" * 40)
        url_patterns = self.get_url_patterns()
        print(f"Nombre de patterns d'URL: {len(url_patterns)}")
        for pattern in url_patterns:
            status = "✅" if pattern['callback'] else "⚠️"
            print(f"{status} {pattern['pattern']} -> {pattern.get('name', 'SANS NOM')}")
        
        # 4. Templates disponibles
        print("\n📄 TEMPLATES DISPONIBLES")
        print("-" * 40)
        templates = self.get_all_templates()
        print(f"Nombre de templates HTML: {len(templates)}")
        
        # 5. Vérification templates-vues
        print("\n🔄 CORRESPONDANCE VUES-TEMPLATES")
        print("-" * 40)
        view_templates = self.check_view_templates()
        template_issues = 0
        
        for vt in view_templates:
            if vt['exists'] is False:
                status = "❌ MANQUANT"
                template_issues += 1
            elif vt['exists'] is True:
                status = "✅ OK"
            else:
                status = "⚠️ INCONNU"
            
            print(f"{status} {vt['view']:30} -> {vt['template']}")
        
        # 6. URLs sans vues
        print("\n⚠️ PROBLÈMES DÉTECTÉS")
        print("-" * 40)
        
        # Templates manquants
        broken = self.find_broken_templates()
        if broken:
            print("\n❌ TEMPLATES MANQUANTS (référencés dans les vues):")
            for b in broken:
                print(f"   • Vue: {b['view']}")
                print(f"     Template: {b['template']}")
                print(f"     Ligne: {b['line']}")
                print()
        
        # Vérifier le template générer_cotisations.html spécifiquement
        print("\n🔍 VÉRIFICATION SPÉCIFIQUE: generer_cotisations.html")
        print("-" * 40)
        cotisation_template = self.template_dir / 'cotisations' / 'generer_cotisations.html'
        if cotisation_template.exists():
            print(f"✅ Template trouvé: {cotisation_template}")
            
            # Vérifier le contenu du template
            with open(cotisation_template, 'r') as f:
                content = f.read()
                has_form = 'form' in content.lower()
                has_csrf = 'csrf_token' in content
                has_submit = 'submit' in content.lower()
                
                print(f"   ✓ Contient un formulaire: {has_form}")
                print(f"   ✓ Contient CSRF token: {has_csrf}")
                print(f"   ✓ Contient bouton submit: {has_submit}")
        else:
            print(f"❌ Template MANQUANT: {cotisation_template}")
            
            # Chercher dans d'autres emplacements
            alternative_locations = [
                self.template_dir / 'generer_cotisations.html',
                self.base_dir / 'templates' / 'generer_cotisations.html',
            ]
            
            found = False
            for alt in alternative_locations:
                if alt.exists():
                    print(f"✅ Trouvé à: {alt}")
                    found = True
                    break
            
            if not found:
                print("💡 SUGGESTION: Créez le fichier avec:")
                print(f"   touch {cotisation_template}")
        
        # 7. Résumé
        print("\n" + "=" * 80)
        print("📋 RÉSUMÉ DU DIAGNOSTIC")
        print("=" * 80)
        print(f"✅ Vues détectées: {len(views)}")
        print(f"✅ URLs configurées: {len(url_patterns)}")
        print(f"✅ Templates disponibles: {len(templates)}")
        print(f"⚠️  Problèmes de templates: {len(broken)}")
        
        if len(broken) == 0:
            print("\n🎉 Tous les checks sont passés avec succès!")
        else:
            print(f"\n🔧 {len(broken)} problème(s) à résoudre.")
            
            # Solution rapide pour generer_cotisations.html
            if any('generer_cotisations' in str(b.get('template', '')) for b in broken):
                print("\n💡 SOLUTION RAPIDE pour generer_cotisations.html:")
                print("""
1. Créez le template manquant:
   mkdir -p templates/assureur/cotisations
   touch templates/assureur/cotisations/generer_cotisations.html
   
2. Ajoutez ce contenu minimal: