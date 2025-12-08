#!/usr/bin/env python3
"""
Script d'analyse et diagnostic pour les problèmes vidéo
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
        # Créer un poster simple avec HTML/CSS en attendant
        test_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { 
                    margin: 0; 
                    background: linear-gradient(135deg, #2c5aa0, #3a7bd5);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    color: white;
                    font-family: Arial, sans-serif;
                }
                .content {
                    text-align: center;
                    padding: 2rem;
                }
                .play-icon {
                    font-size: 4rem;
                    margin-bottom: 1rem;
                }
            </style>
        </head>
        <body>
            <div class="content">
                <div class="play-icon">▶️</div>
                <h1>MaSante Direct</h1>
                <p>Vidéo de présentation</p>
                <p><small>Cliquez pour regarder</small></p>
            </div>
        </body>
        </html>
        """
        print("📝 Création d'un poster de test...")
        # Note: Pour un vrai poster, vous devriez créer une image JPG/PNG
    
    # Créer un fichier vidéo de test minimal
    video_path = Path("static/mutuelle_core/videos/presentation.mp4")
    if not video_path.exists():
        print("📹 Téléchargement d'une vidéo de test...")
        # Vous pouvez télécharger une petite vidéo de test
        test_video_url = "https://sample-videos.com/zip/10/mp4/mp4-10.zip"
        print(f"💡 Téléchargez une vidéo de test depuis: {test_video_url}")
        print("💡 Ou utilisez une vidéo YouTube intégrée")

def suggest_solutions(issues):
    """Propose des solutions basées sur les problèmes détectés"""
    print("\n🚀 SOLUTIONS RECOMMANDÉES:")
    
    if not issues:
        print("✅ Aucun problème détecté! La vidéo devrait fonctionner.")
        return
    
    for issue in issues:
        if "manquant" in issue.lower():
            if "video" in issue.lower():
                print("""
🔧 SOLUTION pour fichier vidéo manquant:
1. Placez votre fichier vidéo dans: static/mutuelle_core/videos/presentation.mp4
2. OU utilisez une vidéo YouTube intégrée:
   ```html
   <iframe src="https://www.youtube.com/embed/VOTRE_ID_VIDEO"></iframe>