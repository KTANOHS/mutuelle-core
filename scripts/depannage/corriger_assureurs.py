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

def corriger_probleme_assureur():
    """Corrige les problèmes de profils Assureur"""
    print("🔧 Correction des problèmes d'assureur...")
    
    # Trouver tous les utilisateurs dans le groupe ASSUREUR
    groupe_assureur, _ = Group.objects.get_or_create(name='ASSUREUR')
    utilisateurs_assureurs = groupe_assureur.user_set.all()
    
    print(f"✅ Trouvé {utilisateurs_assureurs.count()} utilisateurs dans le groupe ASSUREUR")
    
    for user in utilisateurs_assureurs:
        print(f"\n--- Traitement de {user.username} ---")
        
        # Vérifier si un profil existe déjà
        try:
            assureur = Assureur.objects.get(user=user)
            print(f"✅ Profil Assureur existant trouvé (ID: {assureur.id})")
        except Assureur.DoesNotExist:
            print("⚠️  Pas de profil Assureur, création...")
            
            try:
                # Créer le profil SANS inclure 'nom'
                assureur = Assureur.objects.create(
                    user=user,
                    numero_employe=user.username,
                    departement="Non spécifié",
                    date_embauche=date.today(),
                    est_actif=True
                )
                print(f"✅ Profil Assureur créé avec succès (ID: {assureur.id})")
            except Exception as e:
                print(f"❌ Erreur création: {e}")
                
                # Méthode alternative: création manuelle
                try:
                    assureur = Assureur()
                    assureur.user = user
                    assureur.numero_employe = user.username
                    assureur.departement = "Non spécifié"
                    assureur.date_embauche = date.today()
                    assureur.est_actif = True
                    assureur.save()
                    print(f"✅ Profil Assureur créé via méthode alternative (ID: {assureur.id})")
                except Exception as e2:
                    print(f"❌ Échec méthode alternative: {e2}")
    
    print("\n✅ Correction terminée")

if __name__ == "__main__":
    corriger_probleme_assureur()