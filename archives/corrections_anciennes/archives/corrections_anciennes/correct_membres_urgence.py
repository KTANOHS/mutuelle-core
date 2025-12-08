# correct_membres_urgence.py
import os
import django
import sys

sys.path.append('/Users/koffitanohsoualiho/Documents/VERIFICATION/projet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutuelle_core.settings')
django.setup()

from django.contrib.auth.models import User
from membres.models import Membre

def corriger_relations_membres():
    print("🔧 CORRECTION URGENTE DES RELATIONS MEMBRES")
    print("=" * 50)
    
    users_sans_membre = []
    for user in User.objects.all():
        try:
            # Vérifier si l'user a un membre via la nouvelle relation
            membre = getattr(user, 'membre', None)
            if not membre:
                users_sans_membre.append(user)
                print(f"❌ {user.username} n'a pas de membre")
        except Exception as e:
            users_sans_membre.append(user)
            print(f"❌ {user.username} - erreur: {e}")
    
    if users_sans_membre:
        print(f"\n📊 {len(users_sans_membre)} utilisateurs sans membre")
        print("🔄 Création des membres manquants...")
        
        for user in users_sans_membre:
            try:
                # Créer un membre basique
                membre = Membre.objects.create(
                    user=user,
                    numero_membre=f"MEM{user.id:06d}",
                    nom=user.last_name or "Nom à compléter",
                    prenom=user.first_name or "Prénom à compléter",
                    email=user.email or "",
                    telephone="",
                    statut="actif",
                    categorie="standard"
                )
                print(f"✅ Membre créé pour {user.username} (ID: {membre.id})")
            except Exception as e:
                print(f"❌ Erreur création membre pour {user.username}: {e}")
    else:
        print("✅ Tous les utilisateurs ont un membre!")

if __name__ == "__main__":
    corriger_relations_membres()