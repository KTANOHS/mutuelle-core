#!/usr/bin/env python
"""
Script de maintenance pour nettoyer le projet Django
"""
import os
import sys
import shutil
from datetime import datetime, timedelta

def nettoyer_pycache():
    """Supprimer tous les dossiers __pycache__"""
    count = 0
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(path)
                    print(f"✓ Supprimé: {path}")
                    count += 1
                except Exception as e:
                    print(f"✗ Erreur avec {path}: {e}")
    return count

def nettoyer_logs_vieux(jours=30):
    """Supprimer les vieux fichiers de log"""
    count = 0
    cutoff = datetime.now() - timedelta(days=jours)
    
    for root, dirs, files in os.walk('.'):
        for file_name in files:
            if file_name.endswith('.log'):
                path = os.path.join(root, file_name)
                try:
                    mtime = datetime.fromtimestamp(os.path.getmtime(path))
                    if mtime < cutoff:
                        os.remove(path)
                        print(f"✓ Supprimé (vieux): {path}")
                        count += 1
                except Exception as e:
                    print(f"✗ Erreur avec {path}: {e}")
    return count

def calculer_taille_dossier(chemin='.'):
    """Calculer la taille totale du projet"""
    total = 0
    for root, dirs, files in os.walk(chemin):
        # Ignorer certains dossiers
        ignore_dirs = ['venv', '.git', '__pycache__', 'archives', 'backups']
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for file in files:
            file_path = os.path.join(root, file)
            try:
                total += os.path.getsize(file_path)
            except:
                pass
    
    # Convertir en Mo
    total_mb = total / (1024 * 1024)
    return total_mb

def main():
    print("🔧 Script de maintenance du projet Django")
    print("=" * 50)
    
    # Calculer la taille avant nettoyage
    taille_avant = calculer_taille_dossier()
    print(f"Taille du projet: {taille_avant:.2f} MB")
    
    # Nettoyer
    print("\n🧹 Nettoyage en cours...")
    pycache_supprimes = nettoyer_pycache()
    logs_supprimes = nettoyer_logs_vieux(30)
    
    # Calculer la taille après nettoyage
    taille_apres = calculer_taille_dossier()
    espace_gagne = taille_avant - taille_apres
    
    print("\n📊 Résumé du nettoyage:")
    print(f"- Dossiers __pycache__ supprimés: {pycache_supprimes}")
    print(f"- Fichiers log vieux supprimés: {logs_supprimes}")
    print(f"- Espace libéré: {espace_gagne:.2f} MB")
    print(f"- Nouvelle taille: {taille_apres:.2f} MB")
    
    print("\n✅ Maintenance terminée!")

if __name__ == "__main__":
    main()
