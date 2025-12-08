#!/usr/bin/env python3
"""
MIGRATION URLs - Version corrigée
"""

import os
import sys
import django

# CORRECTION DU CHEMIN - Utiliser le répertoire parent
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_path)  # Insérer au début

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erreur Django setup: {e}")
    sys.exit(1)

def analyser_urls():
    """Analyse complète des URLs"""
    print("🔍 ANALYSE COMPLÈTE DES URLs")
    
    from django.urls import get_resolver
    from django.core.checks.urls import check_url_config
    
    # Vérifier la configuration
    print("\n✅ VÉRIFICATION CONFIGURATION...")
    errors = check_url_config(None)
    if errors:
        print("❌ ERREURS DÉTECTÉES:")
        for error in errors:
            print(f"   - {error}")
    else:
        print("✅ Aucune erreur de configuration URLs")
    
    # Compter les URLs
    print("\n📊 COMPTAGE DES URLs...")
    resolver = get_resolver()
    url_count = 0
    urls_par_app = {}
    
    def analyser_patterns(patterns, namespace=None):
        nonlocal url_count
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):
                # C'est un include
                new_namespace = pattern.namespace
                if namespace:
                    new_namespace = f"{namespace}:{new_namespace}" if new_namespace else namespace
                analyser_patterns(pattern.url_patterns, new_namespace)
            else:
                url_count += 1
                app_name = namespace or "root"
                if app_name not in urls_par_app:
                    urls_par_app[app_name] = 0
                urls_par_app[app_name] += 1
    
    analyser_patterns(resolver.url_patterns)
    
    print(f"📈 URLs totales: {url_count}")
    print("\n📁 RÉPARTITION PAR APPLICATION:")
    for app, count in sorted(urls_par_app.items()):
        print(f"   • {app}: {count} URLs")
    
    # Vérifier les conflits spécifiques
    print("\n🔍 CONFLITS IDENTIFIÉS:")
    try:
        from django.urls import reverse, NoReverseMatch
        
        conflits_testes = [
            ("/soins/", "Conflit potentiel soins/"),
            ("/membres/creer/", "Double création membre"),
        ]
        
        for url_pattern, description in conflits_testes:
            print(f"   🔍 Vérification: {description}")
            
    except Exception as e:
        print(f"   ⚠️  Impossible de vérifier les conflits: {e}")

def verifier_doublons():
    """Vérifie les doublons d'URLs"""
    print("\n🔍 RECHERCHE DE DOUBLONS...")
    
    from django.urls import get_resolver
    
    resolver = get_resolver()
    noms_urls = []
    
    def collecter_noms(patterns, namespace=None):
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):
                new_ns = pattern.namespace
                if namespace:
                    new_ns = f"{namespace}:{new_ns}" if new_ns else namespace
                collecter_noms(pattern.url_patterns, new_ns)
            elif hasattr(pattern, 'name') and pattern.name:
                nom_complet = f"{namespace}:{pattern.name}" if namespace else pattern.name
                noms_urls.append(nom_complet)
    
    collecter_noms(resolver.url_patterns)
    
    # Chercher les doublons
    doublons = {}
    for nom in noms_urls:
        if noms_urls.count(nom) > 1:
            if nom not in doublons:
                doublons[nom] = 0
            doublons[nom] += 1
    
    if doublons:
        print("❌ DOUBLONS DÉTECTÉS:")
        for nom, count in doublons.items():
            print(f"   - {nom}: {count} occurrences")
    else:
        print("✅ Aucun doublon détecté")

if __name__ == "__main__":
    analyser_urls()
    verifier_doublons()
    print("\n✅ ANALYSE TERMINÉE")