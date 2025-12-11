#!/usr/bin/env python
"""
VÉRIFICATION FINALE AVANT DÉPLOIEMENT RENDER
"""

import os
import sys
import django

def check_render_readiness():
    """Vérifie que l'application est prête pour Render"""
    print("🔍 VÉRIFICATION FINALE POUR RENDER")
    print("=" * 50)
    
    checks = []
    
    # 1. Vérifier app.py
    if os.path.exists('app.py'):
        with open('app.py', 'r') as f:
            content = f.read()
            if 'migrate' in content and 'RENDER' in content:
                checks.append(('app.py (migrations automatiques)', True))
            else:
                checks.append(('app.py (migrations automatiques)', False))
    else:
        checks.append(('app.py (existe)', False))
    
    # 2. Vérifier ALLOWED_HOSTS
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
    django.setup()
    
    from django.conf import settings
    
    # Tester avec variable Render
    os.environ['RENDER'] = 'true'
    
    # Recharger les settings
    from importlib import reload
    from mutuelle_core import settings as settings_module
    reload(settings_module)
    
    # Vérifier ALLOWED_HOSTS
    allowed_hosts = settings_module.ALLOWED_HOSTS
    has_onrender = any('.onrender.com' in host for host in allowed_hosts)
    checks.append(('ALLOWED_HOSTS (.onrender.com)', has_onrender))
    
    # 3. Vérifier les migrations
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM django_migrations")
        migrations_count = cursor.fetchone()[0]
        checks.append(('Migrations appliquées', migrations_count > 0))
    
    # 4. Vérifier les fichiers essentiels
    essential_files = [
        'requirements.txt',
        'runtime.txt',
        'render.yaml',
        'Procfile',
    ]
    
    for file in essential_files:
        checks.append((f'{file} (existe)', os.path.exists(file)))
    
    # Afficher les résultats
    print("\n📊 RÉSULTATS DES VÉRIFICATIONS:")
    print("-" * 50)
    
    all_passed = True
    for check_name, passed in checks:
        icon = "✅" if passed else "❌"
        print(f"{icon} {check_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 TOUT EST PRÊT POUR LE DÉPLOIEMENT SUR RENDER !")
        print("\nProchaines étapes:")
        print("1. git add .")
        print("2. git commit -m 'Prêt pour Render'")
        print("3. git push origin main")
        print("4. Render déploiera automatiquement")
    else:
        print("🚨 CORRIGEZ LES PROBLÈMES CI-DESSUS AVANT DE DÉPLOYER")
    
    return all_passed

if __name__ == "__main__":
    try:
        success = check_render_readiness()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        sys.exit(1)