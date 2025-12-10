# final_check.py
#!/usr/bin/env python3
"""
Vérification finale avant déploiement Render
"""

import os
import sys
from pathlib import Path

def check_deployment():
    """Vérifie que tout est prêt pour le déploiement"""
    base_dir = Path.cwd()
    errors = []
    warnings = []
    
    print("🔍 VÉRIFICATION FINALE POUR RENDER")
    print("=" * 80)
    
    # 1. Fichiers obligatoires
    required_files = [
        'manage.py',
        'requirements.txt',
        'runtime.txt',
        'Procfile',
        'render.yaml',
        'gunicorn_config.py',
        '.gitignore',
        '.env.example'
    ]
    
    for file in required_files:
        if (base_dir / file).exists():
            print(f"✅ {file}")
        else:
            errors.append(f"❌ {file} manquant")
    
    # 2. Vérifier settings.py
    settings_path = base_dir / 'mutuelle_core' / 'settings.py'
    if settings_path.exists():
        with open(settings_path, 'r') as f:
            content = f.read()
            
        checks = [
            ('DEBUG = False', 'DEBUG=False en production'),
            ('ALLOWED_HOSTS', 'ALLOWED_HOSTS configuré'),
            ('whitenoise', 'WhiteNoise configuré'),
            ('SECURE_SSL_REDIRECT', 'HTSSL activé'),
        ]
        
        for check, message in checks:
            if check in content:
                print(f"✅ {message}")
            else:
                warnings.append(f"⚠️  {message} manquant")
    
    # 3. Vérifier .env n'est pas commité
    if (base_dir / '.env').exists():
        # Lire .gitignore
        gitignore_path = base_dir / '.gitignore'
        if gitignore_path.exists():
            with open(gitignore_path, 'r') as f:
                gitignore = f.read()
                if '.env' not in gitignore:
                    errors.append("❌ .env n'est pas dans .gitignore")
                else:
                    print("✅ .env est bien ignoré par Git")
        else:
            errors.append("❌ .gitignore manquant")
    else:
        warnings.append("⚠️  .env manquant (créer à partir de .env.example)")
    
    # 4. Vérifier les doublons
    duplicate_apps = []
    for app_dir in base_dir.iterdir():
        if app_dir.is_dir() and (app_dir / 'apps.py').exists():
            if app_dir.name == 'apps':
                # Vérifier le contenu de apps/
                for sub_app in app_dir.iterdir():
                    if sub_app.is_dir() and (sub_app / 'apps.py').exists():
                        main_app = base_dir / sub_app.name
                        if main_app.exists():
                            duplicate_apps.append(str(sub_app))
    
    if duplicate_apps:
        for dup in duplicate_apps:
            warnings.append(f"⚠️  Application en double: {dup}")
    
    # 5. Résumé
    print("\n" + "=" * 80)
    print("📊 RAPPORT FINAL:")
    print(f"✅ Fichiers requis: {len(required_files) - len(errors)}/{len(required_files)}")
    
    if errors:
        print("\n❌ ERREURS CRITIQUES:")
        for error in errors:
            print(f"  {error}")
    
    if warnings:
        print("\n⚠️  AVERTISSEMENTS:")
        for warning in warnings:
            print(f"  {warning}")
    
    if not errors and not warnings:
        print("\n🎉 TOUT EST PRÊT POUR LE DÉPLOIEMENT!")
        print("Commandes pour déployer:")
        print("1. git add .")
        print("2. git commit -m 'Prêt pour déploiement Render'")
        print("3. git push origin main")
        print("4. Aller sur https://render.com pour connecter le repository")
        return True
    else:
        return False

if __name__ == "__main__":
    if check_deployment():
        sys.exit(0)
    else:
        sys.exit(1)