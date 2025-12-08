#!/usr/bin/env python3
"""
Corrige l'erreur 'no such column: p.est_actif'
"""
import os
import sys
import django

sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')

try:
    django.setup()
    
    # Chercher dans les fichiers où il y a une référence à 'est_actif'
    import re
    
    print("Recherche de 'est_actif' dans les fichiers Python...")
    
    files_to_check = [
        'medecin/views.py',
        'pharmacien/views.py', 
        'core/utils.py',
        'membres/models.py',
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                if 'est_actif' in content:
                    print(f"\n📁 {file_path}:")
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'est_actif' in line:
                            print(f"  Ligne {i+1}: {line.strip()}")
                            
except Exception as e:
    print(f"Erreur: {e}")
