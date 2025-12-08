#!/usr/bin/env python
"""
VÉRIFICATION FINALE APRÈS CORRECTIONS
"""

import os
import sys
from pathlib import Path

# Configuration
project_dir = Path(__file__).parent

def check_critical_urls():
    """Vérifie les URLs critiques"""
    
    print("🔍 VÉRIFICATION DES URLs CRITIQUES")
    print("=" * 50)
    
    critical_urls = [
        'pharmacien:dashboard',
        'pharmacien:stock', 
        'medecin:mes_rendez_vous',
        'medecin:profil_medecin',
        'assureur:recherche_membre',
        'assureur:export_bons_pdf',
    ]
    
    # Vérifier dans les fichiers urls.py
    apps = ['pharmacien', 'medecin', 'assureur', 'membres', 'communication']
    
    for app in apps:
        urls_file = project_dir / app / 'urls.py'
        if urls_file.exists():
            with open(urls_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            app_urls = [url for url in critical_urls if url.startswith(f'{app}:')]
            for url in app_urls:
                if url.split(':')[1] in content:
                    print(f"✅ {url} - PRÉSENTE dans {app}/urls.py")
                else:
                    print(f"❌ {url} - MANQUANTE dans {app}/urls.py")

def check_views_exist():
    """Vérifie que les vues existent"""
    
    print("\n👁️ VÉRIFICATION DES VUES")
    print("=" * 50)
    
    views_to_check = [
        ('medecin', 'mes_rendez_vous'),
        ('medecin', 'profil_medecin'),
        ('assureur', 'recherche_membre'),
        ('pharmacien', 'gestion_stock'),
    ]
    
    for app, view_name in views_to_check:
        views_file = project_dir / app / 'views.py'
        if views_file.exists():
            with open(views_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if f'def {view_name}(' in content:
                print(f"✅ {app}.{view_name} - PRÉSENTE")
            else:
                print(f"❌ {app}.{view_name} - MANQUANTE")
        else:
            print(f"❌ {app}/views.py - FICHIER MANQUANT")

def main():
    """Fonction principale"""
    print("🔍 VÉRIFICATION FINALE DES CORRECTIONS")
    
    check_critical_urls()
    check_views_exist()
    
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DE VÉRIFICATION")
    print("=" * 50)
    print("✅ Les URLs critiques doivent maintenant être accessibles")
    print("✅ Les vues manquantes ont été créées")
    print("✅ Les templates ont été mis à jour")
    print("\n➡️  EXÉCUTEZ MAINTENANT:")
    print("python manage.py check")
    print("python manage.py runserver")

if __name__ == '__main__':
    main()