#!/usr/bin/env python3
"""
Script d'analyse et diagnostic pour les problèmes vidéo - VERSION CORRIGÉE
"""

import os
import sys
from pathlib import Path

def check_static_structure():
    """Vérifie la structure des fichiers statiques"""
    print("🔍 Vérification de la structure des fichiers...")
    
    base_path = Path("static/mutuelle_core")
    required_dirs = ["images", "videos"]
    required_files = {
        "images": ["logo.jpg", "video-poster.jpg"],
        "videos": ["presentation.mp4"]
    }
    
    issues = []
    
    # Vérifier les dossiers
    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        if not dir_path.exists():
            issues.append(f"❌ Dossier manquant: {dir_path}")
            # Créer le dossier
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Dossier créé: {dir_path}")
        else:
            print(f"✅ Dossier trouvé: {dir_path}")
    
    # Vérifier les fichiers
    for dir_name, files in required_files.items():
        dir_path = base_path / dir_name
        for file_name in files:
            file_path = dir_path / file_name
            if not file_path.exists():
                issues.append(f"❌ Fichier manquant: {file_path}")
            else:
                file_size = file_path.stat().st_size
                print(f"✅ Fichier trouvé: {file_path} ({file_size} bytes)")
    
    return issues

def check_video_file():
    """Vérifie le fichier vidéo spécifique"""
    print("\n🎥 Analyse du fichier vidéo...")
    
    video_path = Path("static/mutuelle_core/videos/presentation.mp4")
    
    if not video_path.exists():
        print("❌ Fichier vidéo non trouvé")
        return False
    
    # Vérifier la taille
    file_size = video_path.stat().st_size
    print(f"📊 Taille du fichier: {file_size} bytes ({file_size / 1024 / 1024:.2f} MB)")
    
    # Vérifications de base
    if file_size == 0:
        print("❌ Fichier vidéo vide")
        return False
    
    if file_size > 100 * 1024 * 1024:  # 100MB
        print("⚠️  Fichier vidéo très volumineux, peut causer des problèmes de chargement")
    
    return True

def check_django_settings():
    """Vérifie la configuration Django"""
    print("\n⚙️ Vérification de la configuration Django...")
    
    try:
        # Ces vérifications supposent que vous êtes dans l'environnement Django
        from django.conf import settings
        
        issues = []
        
        # Vérifier STATIC_URL
        if not hasattr(settings, 'STATIC_URL'):
            issues.append("❌ STATIC_URL non défini")
        else:
            print(f"✅ STATIC_URL: {settings.STATIC_URL}")
        
        # Vérifier STATICFILES_DIRS
        if not hasattr(settings, 'STATICFILES_DIRS'):
            issues.append("❌ STATICFILES_DIRS non défini")
        else:
            print(f"✅ STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
        
        # Vérifier le mode debug
        debug_mode = getattr(settings, 'DEBUG', False)
        print(f"✅ DEBUG mode: {debug_mode}")
        
        return issues
        
    except ImportError:
        print("⚠️  Impossible d'importer Django - vérifiez manuellement votre settings.py")
        return ["Impossible de vérifier automatiquement les settings Django"]

def generate_test_files():
    """Génère des fichiers de test si nécessaires"""
    print("\n🛠️ Génération de fichiers de test...")
    
    # Créer un poster de test
    poster_path = Path("static/mutuelle_core/images/video-poster.jpg")
    if not poster_path.exists():
        print("📝 Création d'un poster de test...")
        # Créer un fichier texte d'instructions
        instructions = """
        POUR CRÉER VOTRE POSTER:
        1. Créez une image 800x450px
        2. Enregistrez-la comme video-poster.jpg
        3. Placez-la dans static/mutuelle_core/images/
        """
        print(instructions)

def suggest_solutions(issues):
    """Propose des solutions basées sur les problèmes détectés"""
    print("\n🚀 SOLUTIONS RECOMMANDÉES:")
    
    if not issues:
        print("✅ Aucun problème détecté! La vidéo devrait fonctionner.")
        return
    
    for issue in issues:
        if "manquant" in issue.lower():
            if "video" in issue.lower():
                print("🔧 SOLUTION pour fichier vidéo manquant:")
                print("1. Placez votre fichier vidéo dans: static/mutuelle_core/videos/presentation.mp4")
                print("2. OU utilisez une vidéo YouTube intégrée:")
                print("   ```html")
                print("   <iframe src=\"https://www.youtube.com/embed/VOTRE_ID_VIDEO\"></iframe>")
                print("   ```")
                print("3. OU utilisez une vidéo de test externe:")
                print("   ```html")
                print("   <source src=\"https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4\">")
                print("   ```")
            
            elif "poster" in issue.lower():
                print("🔧 SOLUTION pour poster manquant:")
                print("1. Créez une image 800x450px nommée video-poster.jpg")
                print("2. Placez-la dans: static/mutuelle_core/images/")
                print("3. OU utilisez un placeholder CSS temporaire")

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🎬 ANALYSEUR DE PROBLÈMES VIDÉO - MaSante Direct")
    print("=" * 60)
    
    all_issues = []
    
    # Vérifications
    all_issues.extend(check_static_structure())
    
    video_ok = check_video_file()
    if not video_ok:
        all_issues.append("Fichier vidéo problématique ou manquant")
    
    all_issues.extend(check_django_settings())
    
    # Générer des fichiers de test si nécessaire
    if all_issues:
        generate_test_files()
    
    # Proposer des solutions
    suggest_solutions(all_issues)
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DU DIAGNOSTIC:")
    print(f"Problèmes détectés: {len(all_issues)}")
    
    if all_issues:
        print("\n❌ Problèmes à résoudre:")
        for issue in all_issues:
            print(f"  - {issue}")
    else:
        print("✅ Aucun problème détecté!")
    
    print("=" * 60)

if __name__ == "__main__":
    main()