# membres/correction_membres.py
from django.contrib.auth.models import User
from membres.models import Membre
from django.utils import timezone

def corriger_membres_manquants():
    """Corrige les utilisateurs sans profil membre"""
    utilisateurs_sans_membre = User.objects.filter(membre__isnull=True)
    
    for user in utilisateurs_sans_membre:
        try:
            # Vérifier si un membre existe déjà (doublon)
            if not Membre.objects.filter(user=user).exists():
                membre = Membre.objects.create(
                    user=user,
                    nom=user.last_name or "Non défini",
                    prenom=user.first_name or "Non défini",
                    email=user.email,
                    numero_unique=Membre.generer_numero_unique(),
                    statut=Membre.StatutMembre.ACTIF,
                    categorie=Membre.CategorieMembre.STANDARD,
                    date_inscription=timezone.now().date(),
                    date_derniere_cotisation=timezone.now().date()
                )
                print(f"✅ Profil membre créé pour {user.username}: {membre.numero_unique}")
            else:
                print(f"⚠️  Profil existe déjà pour {user.username}")
                
        except Exception as e:
            print(f"❌ Erreur pour {user.username}: {e}")
    
    return f"Correction terminée. {utilisateurs_sans_membre.count()} utilisateurs traités."

# Exécutez cette fonction dans le shell Django
if __name__ == "__main__":
    corriger_membres_manquants()