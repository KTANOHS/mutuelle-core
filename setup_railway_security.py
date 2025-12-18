#!/usr/bin/env python3
"""
SCRIPT DE CONFIGURATION DE SÉCURITÉ POUR RAILWAY
"""

import subprocess
import sys
from django.core.management.utils import get_random_secret_key

def run_command(cmd, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Succès: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Erreur: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    print("="*70)
    print("🔐 CONFIGURATION DE SÉCURITÉ RAILWAY")
    print("="*70)
    
    # Générer une nouvelle SECRET_KEY
    new_secret_key = get_random_secret_key()
    print(f"\n🔑 NOUVELLE SECRET_KEY générée:")
    print("-"*50)
    print(new_secret_key)
    print("-"*50)
    
    # Liste des variables à définir
    variables = {
        'SECRET_KEY': new_secret_key,
        'DEBUG': 'false',
        'CSRF_TRUSTED_ORIGINS': 'https://web-production-abe5.up.railway.app,https://*.railway.app',
        'CSRF_COOKIE_SECURE': 'true',
        'SESSION_COOKIE_SECURE': 'true',
        'SECURE_HSTS_SECONDS': '31536000',
        'SECURE_HSTS_INCLUDE_SUBDOMAINS': 'true',
        'SECURE_HSTS_PRELOAD': 'true',
        'SECURE_SSL_REDIRECT': 'true',
        'ALLOWED_HOSTS': '.railway.app,localhost,127.0.0.1,web-production-abe5.up.railway.app',
    }
    
    # Demander confirmation
    print("\n📋 VARIABLES À DÉFINIR:")
    for key, value in variables.items():
        print(f"  {key} = {value[:50]}{'...' if len(str(value)) > 50 else ''}")
    
    response = input("\n⚠️  Continuer avec la configuration ? (oui/non): ").lower()
    if response not in ['oui', 'o', 'yes', 'y']:
        print("\n❌ Opération annulée.")
        return
    
    # Définir chaque variable
    success_count = 0
    for key, value in variables.items():
        cmd = f'railway variables set {key} "{value}"'
        if run_command(cmd, f"Définition de {key}"):
            success_count += 1
    
    # Résumé
    print("\n" + "="*70)
    print("📊 RÉSUMÉ DE LA CONFIGURATION")
    print("="*70)
    print(f"✅ {success_count}/{len(variables)} variables définies avec succès")
    
    if success_count == len(variables):
        print("\n🎉 TOUT EST CONFIGURÉ !")
        print("\n📝 PROCHAINES ÉTAPES:")
        print("1. Redéployez l'application:")
        print("   railway up")
        print("\n2. Vérifiez le déploiement:")
        print("   railway logs --follow")
        print("\n3. Testez l'application:")
        print("   open https://web-production-abe5.up.railway.app/")
        print("   open https://web-production-abe5.up.railway.app/admin/")
    else:
        print(f"\n⚠️  {len(variables) - success_count} variables n'ont pas pu être définies")
        print("Vérifiez que vous êtes connecté à Railway:")
        print("  railway login")
        print("\nPuis réessayez les commandes manuellement.")

if __name__ == "__main__":
    main()