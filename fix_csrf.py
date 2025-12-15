#!/usr/bin/env python
import os
import re

print("🔧 Correction des problèmes CSRF pour Railway...")

# Lire le fichier settings.py
with open('mutuelle_core/settings.py', 'r') as f:
    content = f.read()

# Vérifier si CSRF_TRUSTED_ORIGINS existe
if 'CSRF_TRUSTED_ORIGINS' not in content:
    print("⚠️  CSRF_TRUSTED_ORIGINS non trouvé, ajout...")
    
    # Trouver ALLOWED_HOSTS et ajouter après
    pattern = r'(ALLOWED_HOSTS\s*=\s*\[[^\]]+\])'
    match = re.search(pattern, content)
    
    if match:
        new_content = content.replace(
            match.group(0),
            f"""{match.group(0)}

# Configuration CSRF pour Railway
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-555c.up.railway.app',
    'https://*.railway.app',
    'http://web-production-555c.up.railway.app',
    'http://*.railway.app',
]"""
        )
        
        with open('mutuelle_core/settings.py', 'w') as f:
            f.write(new_content)
        print("✅ CSRF_TRUSTED_ORIGINS ajouté")
    else:
        print("❌ Impossible de trouver ALLOWED_HOSTS")
else:
    print("✅ CSRF_TRUSTED_ORIGINS déjà configuré")

print("🎯 Correction terminée !")