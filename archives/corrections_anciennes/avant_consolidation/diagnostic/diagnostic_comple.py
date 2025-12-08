
#!/usr/bin/env python
"""
SCRIPT DE DIAGNOSTIC COMPLET POUR PROJET DJANGO
Vérifie : URLs, vues, templates, modèles et configurations
"""

import os
import sys
import django
import traceback
from pathlib import Path

# ============================================================================
# CONFIGURATION INITIALE
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent
print(f"📁 Répertoire de base: {BASE_DIR}")

# Ajouter le répertoire du projet au path
sys.path.insert(0, str(BASE_DIR))

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()
except Exception as e:
    print(f"❌ Erreur Django setup: {e}")
    sys.exit(1)

from django.urls import get_resolver, reverse, NoReverseMatch
from django.template.loader import get_template
from django.apps import apps
from django.conf import settings

# ============================================================================
# FONCTIONS DE DIAGNOSTIC
# ============================================================================

def verifier_urls_app(app_name='assureur'):
    """Vérifie les URLs de l'application"""
    print(f"\n🔗 VÉRIFICATION DES URLs DE L'APP: {app_name}")
    print("-" * 50)
    
    resolver = get_resolver()
    urls_trouvees = []
    erreurs = []
    
    # Parcourir toutes les URLs
    for pattern in resolver.url_patterns:
        if hasattr(pattern, 'app_name') and pattern.app_name == app_name:
            for url_pattern in pattern.url_patterns:
                urls_trouvees.append({
                    'pattern': str(url_pattern.pattern),
                    'name': url_pattern.name,
                    'callback': url_pattern.callback.__name__ if callable(url_pattern.callback) else str(url_pattern.callback)
                })
    
    if urls_trouvees:
        print(f"✅ {len(urls_trouvees)} URLs trouvées pour '{app_name}':")
        for url in urls_trouvees:
            print(f"   📍 {url['pattern']} -> {url['name']} (vue: {url['callback']})")
            
            # Vérifier que la vue existe
            if not hasattr(url['callback'], '__call__'):
                try:
                    module_name = url['callback'].split('.')[0]
                    func_name = url['callback'].split('.')[-1]
                    module = __import__(f'{app_name}.views', fromlist=[func_name])
                    if not hasattr(module, func_name):
                        erreurs.append(f"⚠️  Vue '{url['callback']}' n'existe pas pour l'URL '{url['name']}'")
                except:
                    erreurs.append(f"⚠️  Impossible de vérifier la vue pour '{url['name']}'")
    else:
        print(f"❌ Aucune URL trouvée pour l'app '{app_name}'")
    
    return urls_trouvees, erreurs

def verifier_vues_app(app_name='assureur'):
    """Vérifie les vues de l'application"""
    print(f"\n👁️ VÉRIFICATION DES VUES DE L'APP: {app_name}")
    print("-" * 50)
    
    try:
        views_module = __import__(f'{app_name}.views', fromlist=['*'])
        vues = [attr for attr in dir(views_module) if not attr.startswith('_') and callable(getattr(views_module, attr))]
        
        print(f"✅ {len(vues)} vues trouvées:")
        for i, vue in enumerate(sorted(vues), 1):
            print(f"   {i:2d}. {vue}")
        
        return vues
    except Exception as e:
        print(f"❌ Erreur lors de l'import des vues: {e}")
        return []

def verifier_templates():
    """Vérifie les templates et leurs liens"""
    print(f"\n📄 VÉRIFICATION DES TEMPLATES")
    print("-" * 50)
    
    templates_dir = BASE_DIR / 'templates'
    templates_assureur_dir = templates_dir / 'assureur'
    
    # Vérifier l'existence des répertoires
    print(f"📁 Templates directory: {templates_dir}")
    print(f"📁 Templates assureur: {templates_assureur_dir}")
    
    if templates_dir.exists():
        templates = list(templates_dir.rglob('*.html'))
        print(f"✅ {len(templates)} templates trouvés au total")
        
        # Templates spécifiques à assureur
        if templates_assureur_dir.exists():
            templates_assureur = list(templates_assureur_dir.glob('*.html'))
            print(f"✅ {len(templates_assureur)} templates dans assureur/")
            
            for template in templates_assureur:
                print(f"   📄 {template.relative_to(templates_dir)}")
                
                # Vérifier le contenu
                try:
                    with open(template, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Chercher les URLs Django
                        if '{% url' in content:
                            lines = content.split('\n')
                            for line_num, line in enumerate(lines, 1):
                                if '{% url' in line:
                                    print(f"      Ligne {line_num}: {line.strip()}")
                except Exception as e:
                    print(f"      ❌ Erreur lecture: {e}")
    
    return templates_assureur_dir.exists()

def verifier_urls_dans_templates(app_name='assureur'):
    """Vérifie les URLs problématiques dans les templates"""
    print(f"\n🔍 RECHERCHE D'URLS PROBLÉMATIQUES DANS LES TEMPLATES")
    print("-" * 50)
    
    templates_dir = BASE_DIR / 'templates'
    templates_assureur_dir = templates_dir / 'assureur'
    
    problemes = []
    
    if templates_assureur_dir.exists():
        for template_file in templates_assureur_dir.glob('*.html'):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Extraire toutes les URLs
                    import re
                    url_patterns = re.findall(r'\{%\s*url\s+[\'"]([^\'"]+)[\'"]([^%]*?)%\}', content)
                    
                    for url_name, args in url_patterns:
                        try:
                            # Essayer de résoudre l'URL
                            if args.strip():
                                # URL avec arguments
                                args_list = [arg.strip() for arg in args.strip().split() if arg.strip()]
                                try:
                                    reverse(f'{app_name}:{url_name}', args=args_list)
                                except:
                                    try:
                                        reverse(url_name, args=args_list)
                                    except:
                                        problemes.append({
                                            'template': template_file.name,
                                            'url': url_name,
                                            'args': args_list,
                                            'erreur': 'URL non trouvée'
                                        })
                            else:
                                # URL sans arguments
                                try:
                                    reverse(f'{app_name}:{url_name}')
                                except:
                                    try:
                                        reverse(url_name)
                                    except:
                                        problemes.append({
                                            'template': template_file.name,
                                            'url': url_name,
                                            'args': [],
                                            'erreur': 'URL non trouvée'
                                        })
                        except Exception as e:
                            problemes.append({
                                'template': template_file.name,
                                'url': url_name,
                                'args': args,
                                'erreur': str(e)
                            })
            except Exception as e:
                print(f"❌ Erreur lecture {template_file}: {e}")
    
    if problemes:
        print(f"⚠️  {len(problemes)} URL(s) problématique(s) trouvée(s):")
        for pb in problemes:
            print(f"   📄 {pb['template']}:")
            print(f"      URL: {pb['url']}")
            if pb['args']:
                print(f"      Arguments: {pb['args']}")
            print(f"      Erreur: {pb['erreur']}")
            print()
    else:
        print("✅ Aucune URL problématique trouvée dans les templates")
    
    return problemes

def verifier_modeles():
    """Vérifie les modèles disponibles"""
    print(f"\n🗄️ VÉRIFICATION DES MODÈLES")
    print("-" * 50)
    
    modeles = apps.get_models()
    
    print(f"✅ {len(modeles)} modèles trouvés:")
    for modele in modeles[:20]:  # Limiter l'affichage
        print(f"   📦 {modele.__name__} ({modele._meta.app_label})")
    
    # Modèles spécifiques importants
    modeles_importants = ['Membre', 'Bon', 'Paiement', 'Cotisation']
    for nom_modele in modeles_importants:
        try:
            modele = apps.get_model('agents', nom_modele)
            print(f"   ✅ Modèle '{nom_modele}' trouvé dans 'agents'")
        except:
            try:
                modele = apps.get_model('assureur', nom_modele)
                print(f"   ✅ Modèle '{nom_modele}' trouvé dans 'assureur'")
            except:
                print(f"   ❌ Modèle '{nom_modele}' non trouvé")

def verifier_configuration():
    """Vérifie la configuration Django"""
    print(f"\n⚙️ VÉRIFICATION DE LA CONFIGURATION")
    print("-" * 50)
    
    print(f"📁 BASE_DIR: {settings.BASE_DIR}")
    print(f"📁 Templates DIRS: {settings.TEMPLATES[0]['DIRS']}")
    print(f"✅ DEBUG: {settings.DEBUG}")
    print(f"✅ INSTALLED_APPS: {len(settings.INSTALLED_APPS)} apps")
    
    # Vérifier si assureur est dans INSTALLED_APPS
    if 'assureur' in settings.INSTALLED_APPS:
        print("✅ 'assureur' dans INSTALLED_APPS")
    else:
        print("❌ 'assureur' PAS dans INSTALLED_APPS")

def verifier_conflits_urls(app_name='assureur'):
    """Vérifie les conflits d'URLs"""
    print(f"\n⚠️ RECHERCHE DE CONFLITS D'URLs")
    print("-" * 50)
    
    from assureur import urls as assureur_urls
    
    urls_par_nom = {}
    conflits = []
    
    # Collecter toutes les URLs par nom
    for pattern in assureur_urls.urlpatterns:
        if hasattr(pattern, 'name') and pattern.name:
            if pattern.name in urls_par_nom:
                conflits.append(pattern.name)
            urls_par_nom[pattern.name] = pattern
    
    if conflits:
        print(f"❌ {len(conflits)} conflit(s) d'URLs trouvé(s):")
        for conflit in conflits:
            print(f"   ⚠️  Le nom '{conflit}' est utilisé plusieurs fois")
    else:
        print("✅ Aucun conflit d'URLs trouvé")
    
    return conflits

def generer_rapport_corrections(problemes, conflits):
    """Génère un rapport de corrections"""
    print(f"\n🔧 RAPPORT DE CORRECTIONS RECOMMANDÉES")
    print("=" * 50)
    
    if not problemes and not conflits:
        print("✅ Aucune correction nécessaire")
        return
    
    print("\n1. CORRECTIONS D'URLs DANS TEMPLATES:")
    if problemes:
        for pb in problemes:
            print(f"\n   📄 {pb['template']}:")
            print(f"      ❌ Problème: {pb['url']} -> {pb['erreur']}")
            print(f"      💡 Solution: Utiliser 'assureur:{pb['url']}' ou créer l'URL manquante")
    else:
        print("   ✅ Aucun problème d'URL dans les templates")
    
    print("\n2. CORRECTIONS DE CONFLITS D'URLs:")
    if conflits:
        for conflit in conflits:
            print(f"\n   ⚠️  Conflit: '{conflit}'")
            print(f"      💡 Solution: Renommer l'une des URLs en conflict")
    else:
        print("   ✅ Aucun conflit d'URLs")
    
    print("\n3. ACTIONS RECOMMANDÉES:")
    print("""
   🔹 1. Vérifiez que toutes les vues référencées dans urls.py existent
   🔹 2. Assurez-vous que les templates étendent les bons fichiers de base
   🔹 3. Utilisez toujours le namespace 'assureur:' dans les templates
   🔹 4. Vérifiez qu'aucun nom d'URL n'est dupliqué
   🔹 5. Redémarrez le serveur après corrections
    """)

# ============================================================================
# EXÉCUTION DU DIAGNOSTIC
# ============================================================================

def main():
    print("=" * 60)
    print("🔍 DIAGNOSTIC COMPLET DU PROJET DJANGO")
    print("=" * 60)
    
    try:
        # 1. Configuration
        verifier_configuration()
        
        # 2. URLs
        urls, erreurs_urls = verifier_urls_app('assureur')
        
        # 3. Vues
        vues = verifier_vues_app('assureur')
        
        # 4. Modèles
        verifier_modeles()
        
        # 5. Templates
        verifier_templates()
        
        # 6. URLs problématiques dans templates
        problemes = verifier_urls_dans_templates('assureur')
        
        # 7. Conflits d'URLs
        conflits = verifier_conflits_urls('assureur')
        
        # 8. Rapport de corrections
        generer_rapport_corrections(problemes, conflits)
        
        # 9. Résumé
        print(f"\n📊 RÉSUMÉ DU DIAGNOSTIC")
        print("-" * 50)
        print(f"✅ URLs trouvées: {len(urls)}")
        print(f"✅ Vues trouvées: {len(vues)}")
        print(f"⚠️  Problèmes d'URLs: {len(problemes)}")
        print(f"⚠️  Conflits d'URLs: {len(conflits)}")
        
        if erreurs_urls:
            print(f"\n❌ ERREURS CRITIQUES:")
            for erreur in erreurs_urls:
                print(f"   {erreur}")
        
        print(f"\n🎉 Diagnostic terminé!")
        
    except Exception as e:
        print(f"\n💥 ERREUR CRITIQUE DANS LE DIAGNOSTIC:")
        print(f"   {str(e)}")
        print(f"\n📋 Traceback complet:")
        traceback.print_exc()

if __name__ == '__main__':
    main()


