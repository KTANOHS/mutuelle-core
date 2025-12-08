#!/usr/bin/env python
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from assureur.models import Assureur
from datetime import date
import logging

logger = logging.getLogger(__name__)

def corriger_probleme_assureur():
    """Corrige les problèmes de profils Assureur"""
    print("🔧 Correction complète des problèmes d'assureur...")
    
    # Liste des utilisateurs assureurs attendus
    usernames = ['DOUA', 'ktanos', 'DOUA1']
    
    # Vérifier/créer le groupe ASSUREUR
    try:
        groupe_assureur = Group.objects.get(name='ASSUREUR')
        print("✅ Groupe ASSUREUR trouvé")
    except Group.DoesNotExist:
        try:
            groupe_assureur = Group.objects.get(name='Assureur')
            print("✅ Groupe Assureur trouvé (minuscules)")
        except Group.DoesNotExist:
            groupe_assureur = Group.objects.create(name='ASSUREUR')
            print("✅ Groupe ASSUREUR créé")
    
    for username in usernames:
        print(f"\n--- Traitement de {username} ---")
        
        try:
            user = User.objects.get(username=username)
            
            # 1. Ajouter au groupe ASSUREUR
            if not user.groups.filter(name__in=['ASSUREUR', 'Assureur']).exists():
                user.groups.add(groupe_assureur)
                print(f"✅ Ajouté au groupe {groupe_assureur.name}")
            else:
                print(f"✅ Déjà dans le groupe assureur")
            
            # 2. Créer le profil Assureur si inexistant
            try:
                assureur = Assureur.objects.get(user=user)
                print(f"✅ Profil Assureur existant (ID: {assureur.id})")
            except Assureur.DoesNotExist:
                try:
                    assureur = Assureur.objects.create(
                        user=user,
                        numero_employe=user.username,
                        departement="Service Client",
                        date_embauche=date.today(),
                        est_actif=True
                    )
                    print(f"✅ Profil Assureur créé (ID: {assureur.id})")
                except Exception as e:
                    print(f"❌ Erreur création: {e}")
                    # Méthode alternative
                    try:
                        assureur = Assureur()
                        assureur.user = user
                        assureur.numero_employe = user.username
                        assureur.departement = "Service Client"
                        assureur.date_embauche = date.today()
                        assureur.est_actif = True
                        assureur.save()
                        print(f"✅ Profil créé via méthode alternative (ID: {assureur.id})")
                    except Exception as e2:
                        print(f"❌ Échec complet: {e2}")
                        
        except User.DoesNotExist:
            print(f"⚠️  Utilisateur {username} non trouvé - à créer manuellement")
    
    # Afficher le récapitulatif
    print("\n" + "="*50)
    print("RÉCAPITULATIF FINAL")
    print("="*50)
    
    # Tous les utilisateurs dans le groupe
    users_in_group = groupe_assureur.user_set.all()
    print(f"\nUtilisateurs dans le groupe {groupe_assureur.name}: {users_in_group.count()}")
    for user in users_in_group:
        print(f"  - {user.username}")
    
    # Tous les profils Assureur
    assureurs = Assureur.objects.all()
    print(f"\nProfils Assureur dans la base: {assureurs.count()}")
    for assureur in assureurs:
        print(f"  - {assureur.user.username} (ID: {assureur.id})")
    
    print("\n✅ Correction terminée")

if __name__ == "__main__":
    corriger_probleme_assureur()