#!/usr/bin/env python
"""
CORRECTION DE LA STRUCTURE ASSUREUR
Crée le groupe Assureurs et vérifie la synchronisation
"""

import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def creer_groupe_assureurs():
    """Crée le groupe Assureurs avec les permissions nécessaires"""
    print("🔧 Création du groupe 'Assureurs'...")
    
    try:
        groupe, created = Group.objects.get_or_create(name='Assureurs')
        if created:
            print("✅ Groupe 'Assureurs' créé")
            
            # Ajouter les permissions de base
            permissions_assureur = [
                'view_membre', 'add_membre', 'change_membre',
                'view_bon', 'add_bon', 'change_bon', 
                'view_paiement', 'add_paiement', 'change_paiement',
            ]
            
            for perm_codename in permissions_assureur:
                try:
                    perm = Permission.objects.get(codename=perm_codename)
                    groupe.permissions.add(perm)
                except Permission.DoesNotExist:
                    print(f"⚠️  Permission {perm_codename} non trouvée")
            
            print(f"✅ {groupe.permissions.count()} permissions ajoutées")
        else:
            print("✅ Groupe 'Assureurs' existe déjà")
            
    except Exception as e:
        print(f"❌ Erreur création groupe: {e}")

def verifier_synchronisation_membres():
    """Vérifie la synchronisation des membres"""
    print("\n🔍 Vérification synchronisation membres...")
    
    from membres.models import Membre as MembrePrincipal
    
    total_membres = MembrePrincipal.objects.count()
    print(f"📊 Membres dans modèle principal: {total_membres}")
    
    # Vérifier si des membres ont un agent_createur
    membres_avec_agent = MembrePrincipal.objects.filter(agent_createur__isnull=False).count()
    print(f"📊 Membres avec agent_createur: {membres_avec_agent}")
    
    if membres_avec_agent == 0:
        print("⚠️  Aucun membre n'a d'agent_createur - Vérifiez la création des membres")

def main():
    """Fonction principale"""
    print("🚀 CORRECTION STRUCTURE ASSUREUR")
    
    creer_groupe_assureurs()
    verifier_synchronisation_membres()
    
    print("\n✅ CORRECTIONS TERMINÉES")

if __name__ == "__main__":
    main()