# fix_nom_complet.py
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

def fix_nom_complet():
    """Corriger le problème du nom complet vide"""
    print("👤 CORRECTION DU NOM COMPLET...")
    
    from membres.models import Membre
    from django.contrib.auth.models import User
    
    try:
        # Trouver le membre problématique
        membre = Membre.objects.first()
        if membre:
            print(f"📊 Avant correction:")
            print(f"   - Membre: {membre}")
            print(f"   - User: {membre.user}")
            print(f"   - First name: '{membre.user.first_name}'")
            print(f"   - Last name: '{membre.user.last_name}'")
            print(f"   - Username: '{membre.user.username}'")
            print(f"   - Nom complet: '{membre.nom_complet}'")
            
            # Corriger les données de test
            if membre.nom_complet.strip() == "":
                membre.user.first_name = "John"
                membre.user.last_name = "Doe"
                membre.user.save()
                print("✅ Données utilisateur corrigées")
            
            print(f"📊 Après correction:")
            print(f"   - Nom complet: '{membre.nom_complet}'")
            
        else:
            print("❌ Aucun membre trouvé")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    fix_nom_complet()