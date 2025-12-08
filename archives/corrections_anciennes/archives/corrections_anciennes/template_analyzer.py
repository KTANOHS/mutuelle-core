#!/usr/bin/env python
"""
SCRIPT D'ANALYSE DES TEMPLATES DJANGO - VERSION CORRIGÉE
Analyse tous les templates pour détecter les problèmes courants
"""

import os
import re
import sys
from pathlib import Path

# Ajouter le chemin du projet Django
project_path = Path(__file__).parent
sys.path.insert(0, str(project_path))

try:
    import django
    from django.conf import settings
    
    # Configuration Django manuelle
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')  # Remplacez par votre vrai module settings
    
    # Essayez de trouver automatiquement le module settings
    settings_modules = [
        'mutuelle_core.settings',
        
    ]
    
    for settings_module in settings_modules:
        try:
            os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
            django.setup()
            print(f"✅ Configuration Django chargée: {settings_module}")
            break
        except (ImportError, ModuleNotFoundError):
            continue
    else:
        # Si aucun module settings n'est trouvé, essayez une configuration basique
        print("⚠️  Aucun module settings trouvé, tentative de configuration manuelle...")
        settings.configure(
            DEBUG=True,
            TEMPLATES=[{
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(project_path, 'templates')],
                'APP_DIRS': True,
            }],
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
            ],
            USE_I18N=True,
            USE_L10N=True,
            USE_TZ=True,
        )
        django.setup()
        
except Exception as e:
    print(f"❌ Erreur de configuration Django: {e}")
    print("🔍 Tentative d'analyse sans Django...")
    # Continuer sans Django pour l'analyse basique

from django.template import Template, TemplateSyntaxError

class TemplateAnalyzer:
    def __init__(self):
        self.template_dirs = self.get_template_dirs()
        self.issues = {
            'critical': [],
            'warning': [],
            'info': []
        }
        self.stats = {
            'total_templates': 0,
            'templates_analyzed': 0,
            'errors_found': 0
        }

    def get_template_dirs(self):
        """Récupère tous les répertoires de templates configurés"""
        template_dirs = []
        
        # Répertoires par défaut
        default_dirs = [
            'templates',
            'core/templates',
            'membres/templates', 
            'assureur/templates',
            'medecin/templates',
            'pharmacien/templates',
            'soins/templates',
            'paiements/templates',
            'pharmacie_public/templates'
        ]
        
        for dir_name in default_dirs:
            dir_path = os.path.join(project_path, dir_name)
            if os.path.exists(dir_path):
                template_dirs.append(dir_path)
                print(f"📁 Répertoire templates trouvé: {dir_path}")
        
        # Essayer de récupérer depuis les settings Django si disponible
        try:
            from django.conf import settings
            for template_config in getattr(settings, 'TEMPLATES', []):
                if 'DIRS' in template_config:
                    template_dirs.extend(template_config['DIRS'])
            
            # Ajouter les templates des applications installées
            for app in getattr(settings, 'INSTALLED_APPS', []):
                try:
                    app_path = sys.modules[app].__path__[0]
                    app_template_dir = os.path.join(app_path, 'templates')
                    if os.path.exists(app_template_dir):
                        template_dirs.append(app_template_dir)
                except (KeyError, AttributeError):
                    continue
        except:
            pass
        
        # Nettoyer et dédupliquer
        template_dirs = [os.path.abspath(d) for d in template_dirs if os.path.exists(d)]
        template_dirs = list(set(template_dirs))
        
        return template_dirs

    def find_all_templates(self):
        """Trouve tous les fichiers templates dans les répertoires"""
        templates = []
        template_extensions = ('.html', '.htm', '.txt')
        
        for template_dir in self.template_dirs:
            print(f"🔍 Recherche dans: {template_dir}")
            try:
                for root, dirs, files in os.walk(template_dir):
                    for file in files:
                        if file.endswith(template_extensions):
                            full_path = os.path.join(root, file)
                            templates.append(full_path)
            except Exception as e:
                print(f"❌ Erreur lors de la recherche dans {template_dir}: {e}")
        
        return templates

    def analyze_template_syntax(self, template_path):
        """Analyse la syntaxe du template"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Test de compilation basique
            Template(content)
            return True, None
        except TemplateSyntaxError as e:
            return False, f"Erreur de syntaxe: {str(e)}"
        except UnicodeDecodeError:
            # Essayer avec un autre encodage
            try:
                with open(template_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                Template(content)
                return True, None
            except Exception as e:
                return False, f"Erreur d'encodage: {str(e)}"
        except Exception as e:
            return False, f"Erreur inattendue: {str(e)}"

    def check_template_content(self, template_path):
        """Vérifie le contenu du template pour les problèmes courants"""
        issues = []
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(template_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            except Exception as e:
                issues.append(f"❌ Impossible de lire le fichier: {e}")
                return issues
        
        # Vérifications de base
        checks = [
            self.check_missing_endblocks,
            self.check_unclosed_tags,
            self.check_static_files,
            self.check_url_tags,
            self.check_missing_csrf,
            self.check_broken_inheritance,
            self.check_deprecated_tags,
            self.check_missing_translation,
            self.check_hardcoded_urls,
            self.check_missing_alt_images
        ]
        
        for check in checks:
            try:
                result = check(content, template_path)
                if result:
                    issues.extend(result if isinstance(result, list) else [result])
            except Exception as e:
                issues.append(f"⚠️ Erreur lors de la vérification: {e}")
        
        return issues

    def check_missing_endblocks(self, content, template_path):
        """Vérifie les blocs non fermés"""
        issues = []
        blocks = re.findall(r'{%\s*(block|if|for|with)\s+([^%]+)%}', content)
        endblocks = re.findall(r'{%\s*end(block|if|for|with)\s*%}', content)
        
        if len(blocks) != len(endblocks):
            issues.append(f"❌ Blocs non fermés: {len(blocks)} blocs vs {len(endblocks)} endblocks")
        
        return issues

    def check_unclosed_tags(self, content, template_path):
        """Vérifie les balises HTML non fermées"""
        issues = []
        
        # Balises auto-fermantes
        self_closing_tags = ['img', 'br', 'hr', 'input', 'meta', 'link']
        
        # Vérifier les balises courantes
        tags_to_check = ['div', 'p', 'span', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        
        for tag in tags_to_check:
            opening = len(re.findall(f'<{tag}[^>]*>', content, re.IGNORECASE))
            closing = len(re.findall(f'</{tag}>', content, re.IGNORECASE))
            
            if opening != closing:
                issues.append(f"⚠️ Balise <{tag}> non fermée: {opening} ouvertures vs {closing} fermetures")
        
        return issues

    def check_static_files(self, content, template_path):
        """Vérifie l'utilisation des fichiers statiques"""
        issues = []
        
        # Rechercher les URLs de fichiers statiques sans la balise {% static %}
        static_patterns = [
            r'src=["\'](/static/[^"\']*)["\']',
            r'href=["\'](/static/[^"\']*)["\']',
            r'url\(["\']?(/static/[^"\'\)]*)["\']?\)'
        ]
        
        for pattern in static_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                issues.append(f"❌ Fichier static sans balise: {match}")
        
        # Vérifier la présence de {% load static %}
        if 'src="/static/' in content or 'href="/static/' in content:
            if '{% load static' not in content:
                issues.append("❌ Fichiers static détectés mais '{% load static %}' manquant")
        
        return issues

    def check_url_tags(self, content, template_path):
        """Vérifie l'utilisation des URLs"""
        issues = []
        
        # URLs en dur qui devraient utiliser {% url %}
        hardcoded_urls = re.findall(r'href=["\']/[^/][^"\']*["\']', content)
        for url in hardcoded_urls:
            if '/static/' not in url and '/media/' not in url:
                issues.append(f"⚠️ URL en dur détectée: {url}")
        
        return issues

    def check_missing_csrf(self, content, template_path):
        """Vérifie la présence du token CSRF dans les forms"""
        issues = []
        
        forms_without_csrf = re.findall(r'<form[^>]*>(?!(.*{% csrf_token %}))', content, re.DOTALL)
        
        for form_match in forms_without_csrf:
            if 'method="post"' in form_match.lower():
                issues.append("❌ Formulaire POST sans token CSRF")
        
        return issues

    def check_broken_inheritance(self, content, template_path):
        """Vérifie l'héritage de templates"""
        issues = []
        
        # Vérifier les extends sans blocks
        if '{% extends' in content and '{% block' not in content:
            issues.append("⚠️ Template étend un parent mais ne définit aucun bloc")
        
        # Vérifier les blocks sans extends
        if '{% block' in content and '{% extends' not in content:
            issues.append("⚠️ Blocs définis mais pas d'extends (template de base?)")
        
        return issues

    def check_deprecated_tags(self, content, template_path):
        """Vérifie les balises Django dépréciées"""
        issues = []
        
        deprecated = [
            ('{% load staticfiles %}', '{% load static %}'),
            ('{{ block.super|default:"" }}', '{{ block.super }}'),
        ]
        
        for old, new in deprecated:
            if old in content:
                issues.append(f"🚫 Balise dépréciée: '{old}' → utiliser '{new}'")
        
        return issues

    def check_missing_translation(self, content, template_path):
        """Vérifie le texte non traduit"""
        issues = []
        
        # Texte en français détecté (à adapter selon la langue)
        french_text = re.findall(r'>([^<>{}\n]*[a-zA-ZàâäéèêëîïôöùûüÿçÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇ][^<>{}\n]*)<', content)
        
        for text in french_text[:5]:  # Limiter le nombre de résultats
            text = text.strip()
            if len(text) > 10 and '{%' not in text and '{{' not in text:
                issues.append(f"🌍 Texte potentiellement non traduit: '{text}'")
        
        return issues

    def check_hardcoded_urls(self, content, template_path):
        """Vérifie les URLs absolues en dur"""
        issues = []
        
        hardcoded_domains = re.findall(r'https?://[^\s"\']+', content)
        for url in hardcoded_domains:
            if 'localhost' not in url and '127.0.0.1' not in url:
                issues.append(f"🔗 URL absolue en dur: {url}")
        
        return issues

    def check_missing_alt_images(self, content, template_path):
        """Vérifie les images sans attribut alt"""
        issues = []
        
        images_without_alt = re.findall(r'<img[^>]*?(?=\s*alt\s*=)[^>]*>', content)
        images = re.findall(r'<img[^>]*>', content)
        
        if len(images_without_alt) < len(images):
            issues.append(f"🖼️ Images sans attribut alt: {len(images) - len(images_without_alt)}/{len(images)}")
        
        return issues

    def generate_report(self):
        """Génère un rapport complet"""
        print("=" * 80)
        print("📊 RAPPORT D'ANALYSE DES TEMPLATES DJANGO")
        print("=" * 80)
        
        templates = self.find_all_templates()
        self.stats['total_templates'] = len(templates)
        
        if not templates:
            print("❌ Aucun template trouvé!")
            print("📁 Répertoires recherchés:")
            for dir_path in self.template_dirs:
                print(f"  - {dir_path}")
            return self.stats
        
        print(f"\n📁 Templates trouvés: {len(templates)}")
        print(f"📁 Répertoires analysés: {len(self.template_dirs)}")
        
        for template_path in templates:
            print(f"\n🔍 Analyse de: {os.path.relpath(template_path, project_path)}")
            self.stats['templates_analyzed'] += 1
            
            # Vérifier la syntaxe
            syntax_ok, syntax_error = self.analyze_template_syntax(template_path)
            if not syntax_ok:
                self.issues['critical'].append(f"{template_path}: {syntax_error}")
                print(f"  ❌ ERREUR SYNTAXE: {syntax_error}")
                continue
            
            # Vérifier le contenu
            content_issues = self.check_template_content(template_path)
            for issue in content_issues:
                if '❌' in issue:
                    self.issues['critical'].append(f"{template_path}: {issue}")
                elif '⚠️' in issue:
                    self.issues['warning'].append(f"{template_path}: {issue}")
                else:
                    self.issues['info'].append(f"{template_path}: {issue}")
                
                print(f"  {issue}")
            
            if not content_issues:
                print("  ✅ Aucun problème détecté")
        
        # Rapport final
        print("\n" + "=" * 80)
        print("📈 STATISTIQUES FINALES")
        print("=" * 80)
        print(f"📄 Templates analysés: {self.stats['templates_analyzed']}/{self.stats['total_templates']}")
        print(f"🔴 Problèmes critiques: {len(self.issues['critical'])}")
        print(f"🟠 Avertissements: {len(self.issues['warning'])}")
        print(f"🔵 Informations: {len(self.issues['info'])}")
        
        # Afficher les problèmes par catégorie
        if self.issues['critical']:
            print("\n🔴 PROBLÈMES CRITIQUES:")
            for issue in self.issues['critical'][:10]:  # Limiter l'affichage
                print(f"  • {issue}")
        
        if self.issues['warning']:
            print("\n🟠 AVERTISSEMENTS:")
            for issue in self.issues['warning'][:10]:
                print(f"  • {issue}")
        
        if self.issues['info']:
            print("\n🔵 INFORMATIONS:")
            for issue in self.issues['info'][:5]:
                print(f"  • {issue}")
        
        # Recommandations
        print("\n💡 RECOMMANDATIONS:")
        if self.issues['critical']:
            print("  • Corriger les erreurs de syntaxe en priorité")
        if any('CSRF' in issue for issue in self.issues['critical']):
            print("  • Ajouter les tokens CSRF dans tous les formulaires POST")
        if any('static' in issue for issue in self.issues['critical']):
            print("  • Utiliser la balise {% static %} pour les fichiers statiques")
        
        return self.stats

def main():
    """Fonction principale"""
    try:
        analyzer = TemplateAnalyzer()
        stats = analyzer.generate_report()
        
        # Retour code d'erreur pour CI/CD
        if analyzer.issues['critical']:
            print("\n🚨 Des problèmes critiques ont été détectés!")
            exit(1)
        else:
            print("\n🎉 Analyse terminée avec succès!")
            exit(0)
            
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == '__main__':
    main()